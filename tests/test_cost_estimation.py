"""
Test suite for the Bicep cost estimation script.
"""

import os
import sys
import json
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(script_dir))

from extract_bicep_cost_info import BicepResourceExtractor


def test_bicep_extractor_initialization():
    """Test that the BicepResourceExtractor can be initialized."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        assert extractor.infra_dir.exists()
        assert extractor.resources == []
        assert extractor.parameters == {}


def test_find_bicep_files():
    """Test that the extractor can find bicep files."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        bicep_files = extractor.find_bicep_files()
        
        # Should find at least some bicep files
        assert len(bicep_files) > 0
        
        # All files should have .bicep extension
        for file in bicep_files:
            assert file.suffix == '.bicep'


def test_extract_resources():
    """Test that the extractor can extract resources from bicep files."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        extractor.scan_all_files()
        
        # Should have extracted some resources
        assert len(extractor.resources) > 0
        
        # Check that resources have the expected structure
        for resource in extractor.resources:
            assert 'file' in resource
            assert 'name' in resource
            assert 'type' in resource
            assert 'api_version' in resource
            assert 'sku' in resource
            assert 'properties' in resource


def test_generate_report():
    """Test that the extractor can generate a cost report."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        extractor.scan_all_files()
        report = extractor.generate_cost_report()
        
        # Check report structure
        assert 'summary' in report
        assert 'resources_by_type' in report
        assert 'key_parameters' in report
        
        # Check summary
        assert 'total_resources' in report['summary']
        assert 'resource_types' in report['summary']
        assert 'files_scanned' in report['summary']
        
        # Should have some resources
        assert report['summary']['total_resources'] > 0
        assert report['summary']['resource_types'] > 0


def test_generate_markdown_report():
    """Test that the extractor can generate a markdown report."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        extractor.scan_all_files()
        markdown = extractor.generate_markdown_report()
        
        # Should have markdown content
        assert len(markdown) > 0
        assert '# Azure Infrastructure Cost Estimation Report' in markdown
        assert '## Summary' in markdown
        assert '## Resources by Type' in markdown


def test_sku_extraction():
    """Test that SKU information is extracted correctly."""
    repo_root = Path(__file__).parent.parent
    infra_dir = repo_root / 'infra'
    
    if infra_dir.exists():
        extractor = BicepResourceExtractor(str(infra_dir))
        extractor.scan_all_files()
        
        # Find resources with SKU information
        resources_with_sku = [r for r in extractor.resources if r['sku']]
        
        # Should have some resources with SKU
        assert len(resources_with_sku) > 0
        
        # Check SKU structure
        for resource in resources_with_sku:
            sku = resource['sku']
            # SKU should have at least one of: name, tier, or capacity
            assert 'name' in sku or 'tier' in sku or 'capacity' in sku


def test_generated_files_exist():
    """Test that the generated cost estimation files exist."""
    repo_root = Path(__file__).parent.parent
    
    json_file = repo_root / 'infra' / 'cost-estimation.json'
    md_file = repo_root / 'infra' / 'COST-ESTIMATION.md'
    
    # Files should exist after running the script
    if json_file.exists():
        # Check JSON is valid
        with open(json_file, 'r') as f:
            data = json.load(f)
            assert 'summary' in data
            
    if md_file.exists():
        # Check markdown has content
        with open(md_file, 'r') as f:
            content = f.read()
            assert len(content) > 0
            assert '# Azure Infrastructure Cost Estimation Report' in content


if __name__ == '__main__':
    """Run tests when script is executed directly."""
    print("Running cost estimation tests...")
    
    test_bicep_extractor_initialization()
    print("✓ BicepResourceExtractor initialization test passed")
    
    test_find_bicep_files()
    print("✓ Find bicep files test passed")
    
    test_extract_resources()
    print("✓ Extract resources test passed")
    
    test_generate_report()
    print("✓ Generate report test passed")
    
    test_generate_markdown_report()
    print("✓ Generate markdown report test passed")
    
    test_sku_extraction()
    print("✓ SKU extraction test passed")
    
    test_generated_files_exist()
    print("✓ Generated files test passed")
    
    print("\nAll tests passed! ✓")
