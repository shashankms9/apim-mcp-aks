#!/usr/bin/env python3
"""
Extract resources and SKU information from Bicep files for cost estimation.

This script scans all Bicep files in the /infra folder and extracts:
- Resource types (Microsoft.*/*)
- SKU information (tier, name, capacity)
- Resource names and locations
- Configuration parameters that affect cost

The output can be used to estimate Azure deployment costs.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class BicepResourceExtractor:
    """Extract Azure resource information from Bicep files."""

    def __init__(self, infra_dir: str):
        """Initialize the extractor with the infrastructure directory path."""
        self.infra_dir = Path(infra_dir)
        self.resources = []
        self.parameters = {}

    def find_bicep_files(self) -> List[Path]:
        """Find all .bicep files in the infrastructure directory."""
        return list(self.infra_dir.rglob("*.bicep"))

    def extract_resources_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract resource definitions from a single Bicep file."""
        resources = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract resource definitions using a better approach
            # Find all "resource" declarations and extract their full body
            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i]
                # Look for resource declaration
                resource_match = re.match(r"resource\s+(\w+)\s+'([^']+)'\s*=\s*\{", line)
                if resource_match:
                    resource_name = resource_match.group(1)
                    resource_type_version = resource_match.group(2)
                    
                    # Parse resource type and API version
                    type_parts = resource_type_version.split('@')
                    resource_type = type_parts[0] if len(type_parts) > 0 else ''
                    api_version = type_parts[1] if len(type_parts) > 1 else ''
                    
                    # Extract the full resource body (handle nested braces)
                    resource_body = self._extract_block_body(lines, i)
                    
                    resource_info = {
                        'file': str(file_path.relative_to(self.infra_dir)),
                        'name': resource_name,
                        'type': resource_type,
                        'api_version': api_version,
                        'sku': self._extract_sku(resource_body),
                        'properties': self._extract_key_properties(resource_body)
                    }
                    
                    resources.append(resource_info)
                    
                i += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
        return resources
    
    def _extract_block_body(self, lines: List[str], start_index: int) -> str:
        """Extract a block body handling nested braces."""
        body_lines = []
        brace_count = 0
        started = False
        
        for i in range(start_index, len(lines)):
            line = lines[i]
            
            # Count opening and closing braces
            for char in line:
                if char == '{':
                    brace_count += 1
                    started = True
                elif char == '}':
                    brace_count -= 1
                    
            body_lines.append(line)
            
            # If we've closed all braces, we're done
            if started and brace_count == 0:
                break
                
        return '\n'.join(body_lines)

    def _extract_sku(self, resource_body: str) -> Dict[str, Any]:
        """Extract SKU information from resource body."""
        sku_info = {}
        
        # Look for sku block: sku: { name: 'xxx', tier: 'xxx', capacity: N }
        sku_pattern = r"sku:\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}"
        sku_match = re.search(sku_pattern, resource_body, re.DOTALL)
        
        if sku_match:
            sku_block = sku_match.group(1)
            
            # Extract name (handle both string literals and parameter references)
            name_patterns = [
                r"name:\s*['\"]([^'\"]+)['\"]",  # String literal
                r"name:\s*(\w+)",  # Parameter reference
            ]
            for pattern in name_patterns:
                name_match = re.search(pattern, sku_block)
                if name_match:
                    name_value = name_match.group(1).strip()
                    # Keep parameter references for documentation
                    sku_info['name'] = name_value
                    break
                
            # Extract tier (handle both string literals and parameter references)
            tier_patterns = [
                r"tier:\s*['\"]([^'\"]+)['\"]",  # String literal
                r"tier:\s*(\w+)",  # Parameter reference
            ]
            for pattern in tier_patterns:
                tier_match = re.search(pattern, sku_block)
                if tier_match:
                    tier_value = tier_match.group(1).strip()
                    sku_info['tier'] = tier_value
                    break
                
            # Extract capacity
            capacity_match = re.search(r"capacity:\s*(\d+|\w+)", sku_block)
            if capacity_match:
                capacity_value = capacity_match.group(1)
                try:
                    sku_info['capacity'] = int(capacity_value)
                except ValueError:
                    # It's a parameter reference
                    sku_info['capacity'] = capacity_value
                
        return sku_info

    def _extract_key_properties(self, resource_body: str) -> Dict[str, Any]:
        """Extract key properties that affect cost."""
        props = {}
        
        # Extract location
        location_match = re.search(r"location:\s*['\"]?([^'\"\n,}]+)['\"]?", resource_body)
        if location_match:
            location = location_match.group(1).strip()
            # Skip if it's a function call
            if not location.startswith('resourceGroup()'):
                props['location'] = location
                
        # Extract VM size for AKS/VMs
        vm_size_patterns = [
            r"vmSize:\s*['\"]([^'\"]+)['\"]",
            r"systemNodePoolVmSize:\s*['\"]([^'\"]+)['\"]"
        ]
        for pattern in vm_size_patterns:
            vm_match = re.search(pattern, resource_body)
            if vm_match:
                props['vm_size'] = vm_match.group(1)
                break
                
        # Extract node count for AKS
        count_patterns = [
            r"count:\s*(\d+)",
            r"systemNodePoolCount:\s*(\d+)"
        ]
        for pattern in count_patterns:
            count_match = re.search(pattern, resource_body)
            if count_match:
                props['node_count'] = int(count_match.group(1))
                break
                
        # Extract model capacity for AI services
        model_capacity_match = re.search(r"modelCapacity:\s*(\d+)", resource_body)
        if model_capacity_match:
            props['model_capacity'] = int(model_capacity_match.group(1))
            
        return props

    def extract_parameters_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract parameter definitions from a Bicep file."""
        params = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract parameter definitions
            # Pattern: param <name> <type> = <default>
            param_pattern = r"param\s+(\w+)\s+(\w+)(?:\s*=\s*['\"]?([^'\"\n]+)['\"]?)?"
            
            for match in re.finditer(param_pattern, content):
                param_name = match.group(1)
                param_type = match.group(2)
                default_value = match.group(3) if match.group(3) else None
                
                # Look for @allowed decorator before the param
                allowed_pattern = rf"@allowed\(\[([^\]]+)\]\)\s*(?:@[^\n]+\s*)*param\s+{param_name}\s"
                allowed_match = re.search(allowed_pattern, content)
                
                params[param_name] = {
                    'type': param_type,
                    'default': default_value
                }
                
                if allowed_match:
                    allowed_values = [v.strip().strip("'\"") for v in allowed_match.group(1).split(',')]
                    params[param_name]['allowed_values'] = allowed_values
                    
        except Exception as e:
            print(f"Error extracting parameters from {file_path}: {e}")
            
        return params

    def scan_all_files(self):
        """Scan all Bicep files and extract resource information."""
        bicep_files = self.find_bicep_files()
        print(f"Found {len(bicep_files)} Bicep files")
        
        for file_path in bicep_files:
            resources = self.extract_resources_from_file(file_path)
            self.resources.extend(resources)
            
            # Extract parameters from main.bicep
            if file_path.name == 'main.bicep':
                self.parameters.update(self.extract_parameters_from_file(file_path))

    def generate_cost_report(self) -> Dict[str, Any]:
        """Generate a cost estimation report."""
        # Group resources by type
        resources_by_type = defaultdict(list)
        for resource in self.resources:
            resources_by_type[resource['type']].append(resource)
            
        # Create summary
        report = {
            'summary': {
                'total_resources': len(self.resources),
                'resource_types': len(resources_by_type),
                'files_scanned': len(set(r['file'] for r in self.resources))
            },
            'resources_by_type': {},
            'key_parameters': {}
        }
        
        # Add resources grouped by type
        for resource_type, resources in sorted(resources_by_type.items()):
            report['resources_by_type'][resource_type] = {
                'count': len(resources),
                'instances': []
            }
            
            for resource in resources:
                instance = {
                    'file': resource['file'],
                    'name': resource['name']
                }
                
                if resource['sku']:
                    instance['sku'] = resource['sku']
                    
                if resource['properties']:
                    instance['properties'] = resource['properties']
                    
                report['resources_by_type'][resource_type]['instances'].append(instance)
                
        # Add key cost-related parameters
        cost_related_params = ['fabricSkuName', 'apimSku', 'systemNodePoolVmSize', 
                               'systemNodePoolCount', 'modelCapacity', 'embeddingModelCapacity',
                               'skuTier']
        for param_name in cost_related_params:
            if param_name in self.parameters:
                report['key_parameters'][param_name] = self.parameters[param_name]
                
        return report

    def generate_markdown_report(self) -> str:
        """Generate a markdown formatted cost report."""
        report = self.generate_cost_report()
        
        md = ["# Azure Infrastructure Cost Estimation Report\n"]
        md.append(f"**Generated from Bicep files in `/infra` folder**\n")
        md.append(f"## Summary\n")
        md.append(f"- Total Resources: {report['summary']['total_resources']}")
        md.append(f"- Resource Types: {report['summary']['resource_types']}")
        md.append(f"- Files Scanned: {report['summary']['files_scanned']}\n")
        
        md.append(f"## Resources by Type\n")
        
        for resource_type, info in sorted(report['resources_by_type'].items()):
            md.append(f"### {resource_type} ({info['count']})\n")
            
            for instance in info['instances']:
                md.append(f"- **{instance['name']}** (`{instance['file']}`)")
                
                if 'sku' in instance and instance['sku']:
                    sku_parts = []
                    if 'name' in instance['sku']:
                        sku_parts.append(f"SKU: {instance['sku']['name']}")
                    if 'tier' in instance['sku']:
                        sku_parts.append(f"Tier: {instance['sku']['tier']}")
                    if 'capacity' in instance['sku']:
                        sku_parts.append(f"Capacity: {instance['sku']['capacity']}")
                    if sku_parts:
                        md.append(f"  - {', '.join(sku_parts)}")
                        
                if 'properties' in instance and instance['properties']:
                    props = instance['properties']
                    if 'vm_size' in props:
                        md.append(f"  - VM Size: {props['vm_size']}")
                    if 'node_count' in props:
                        md.append(f"  - Node Count: {props['node_count']}")
                    if 'model_capacity' in props:
                        md.append(f"  - Model Capacity: {props['model_capacity']}")
                        
            md.append("")
            
        if report['key_parameters']:
            md.append(f"## Key Cost-Related Parameters\n")
            for param_name, param_info in sorted(report['key_parameters'].items()):
                md.append(f"- **{param_name}** ({param_info['type']})")
                if param_info.get('default'):
                    md.append(f"  - Default: `{param_info['default']}`")
                if param_info.get('allowed_values'):
                    md.append(f"  - Allowed: {', '.join(f'`{v}`' for v in param_info['allowed_values'])}")
                md.append("")
                
        return '\n'.join(md)


def main():
    """Main entry point."""
    # Determine infrastructure directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    infra_dir = repo_root / 'infra'
    
    if not infra_dir.exists():
        print(f"Error: Infrastructure directory not found at {infra_dir}")
        sys.exit(1)
        
    # Extract resources
    extractor = BicepResourceExtractor(str(infra_dir))
    extractor.scan_all_files()
    
    # Generate reports
    json_report = extractor.generate_cost_report()
    markdown_report = extractor.generate_markdown_report()
    
    # Output JSON report
    json_output = repo_root / 'infra' / 'cost-estimation.json'
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2)
    print(f"JSON report saved to: {json_output}")
    
    # Output Markdown report
    md_output = repo_root / 'infra' / 'COST-ESTIMATION.md'
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    print(f"Markdown report saved to: {md_output}")
    
    # Print summary to console
    print("\n" + "="*60)
    print("COST ESTIMATION SUMMARY")
    print("="*60)
    print(f"Total Resources: {json_report['summary']['total_resources']}")
    print(f"Resource Types: {json_report['summary']['resource_types']}")
    print(f"\nResource Types Found:")
    for resource_type, info in sorted(json_report['resources_by_type'].items()):
        print(f"  - {resource_type}: {info['count']}")


if __name__ == '__main__':
    main()
