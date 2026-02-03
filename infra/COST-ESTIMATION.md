# Azure Infrastructure Cost Estimation Report

**Generated from Bicep files in `/infra` folder**

## Summary

- Total Resources: 119
- Resource Types: 39
- Files Scanned: 38

## Resources by Type

### Microsoft.ApiManagement/service (1)

- **apimService** (`core/apim/apim.bicep`)
  - SKU: apimSku, Capacity: 1

### Microsoft.ApiManagement/service/apis (2)

- **oauthApi** (`app/apim-oauth/oauth.bicep`)
- **mcpApi** (`app/apim-mcp/mcp-api.bicep`)

### Microsoft.ApiManagement/service/apis/operations (11)

- **oauthAuthorizeOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthTokenOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthCallbackOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthRegisterOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthRegisterOptionsOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthMetadataOptionsOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthMetadataGetOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthConsentGetOperation** (`app/apim-oauth/oauth.bicep`)
- **oauthConsentPostOperation** (`app/apim-oauth/oauth.bicep`)
- **mcpSseOperation** (`app/apim-mcp/mcp-api.bicep`)
- **mcpMessageOperation** (`app/apim-mcp/mcp-api.bicep`)

### Microsoft.ApiManagement/service/apis/operations/policies (9)

- **oauthAuthorizePolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthTokenPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthCallbackPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthRegisterPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthRegisterOptionsPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthMetadataOptionsPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthMetadataGetPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthConsentGetPolicy** (`app/apim-oauth/oauth.bicep`)
- **oauthConsentPostPolicy** (`app/apim-oauth/oauth.bicep`)

### Microsoft.ApiManagement/service/apis/policies (1)

- **mcpApiPolicy** (`app/apim-mcp/mcp-api.bicep`)

### Microsoft.ApiManagement/service/namedValues (10)

- **encryptionKeyNamedValue** (`app/apim-oauth/oauth.bicep`)
- **encryptionIVNamedValue** (`app/apim-oauth/oauth.bicep`)
- **EntraIDTenantIdNamedValue** (`app/apim-oauth/oauth.bicep`)
- **EntraIDClientIdNamedValue** (`app/apim-oauth/oauth.bicep`)
- **EntraIdFicClientIdNamedValue** (`app/apim-oauth/oauth.bicep`)
- **OAuthCallbackUriNamedValue** (`app/apim-oauth/oauth.bicep`)
- **OAuthScopesNamedValue** (`app/apim-oauth/oauth.bicep`)
- **McpClientIdNamedValue** (`app/apim-oauth/oauth.bicep`)
- **APIMGatewayURLNamedValue** (`app/apim-oauth/oauth.bicep`)
- **MCPServerNamedValue** (`app/apim-oauth/oauth.bicep`)

### Microsoft.Authorization/roleAssignments (11)

- **storageRoleAssignment** (`app/storage-Access.bicep`)
- **searchIndexDataContributorAgent** (`app/agent-RoleAssignments.bicep`)
- **searchServiceContributorAgent** (`app/agent-RoleAssignments.bicep`)
- **storageBlobDataOwnerAgent** (`app/agent-RoleAssignments.bicep`)
- **storageQueueDataContributorAgent** (`app/agent-RoleAssignments.bicep`)
- **openAIUserAgent** (`app/agent-RoleAssignments.bicep`)
- **openAIContributorAgent** (`app/agent-RoleAssignments.bicep`)
- **roleAssignment** (`app/foundry-RoleAssignment.bicep`)
- **acrRoleAssignment** (`core/acr/acr-role-assignment.bicep`)
- **roleAssignment** (`core/search/search-role-assignment.bicep`)
- **appInsightsRoleAssignment** (`core/monitor/appinsights-access.bicep`)

### Microsoft.Bing/accounts (1)

- **bingGrounding** (`core/ai/foundry.bicep`)
  - SKU: G1

### Microsoft.CognitiveServices/accounts (1)

- **foundryAccount** (`core/ai/foundry.bicep`)
  - SKU: S0

### Microsoft.CognitiveServices/accounts/capabilityHosts (1)

- **agentsCapabilityHost** (`core/ai/foundry.bicep`)

### Microsoft.CognitiveServices/accounts/deployments (2)

- **modelDeployment** (`core/ai/foundry.bicep`)
  - SKU: GlobalStandard, Capacity: modelCapacity
- **embeddingModelDeployment** (`core/ai/foundry.bicep`)
  - SKU: Standard, Capacity: embeddingModelCapacity

### Microsoft.CognitiveServices/accounts/projects (1)

- **defaultProject** (`core/ai/foundry.bicep`)

### Microsoft.CognitiveServices/accounts/projects/connections (1)

- **bingConnection** (`core/ai/foundry.bicep`)

### Microsoft.ContainerRegistry/registries (1)

- **containerRegistry** (`core/acr/container-registry.bicep`)
  - SKU: sku

### Microsoft.ContainerService/managedClusters (1)

- **aksCluster** (`core/aks/aks-cluster.bicep`)
  - SKU: Base, Tier: skuTier

### Microsoft.DocumentDB/databaseAccounts (1)

- **account** (`core/cosmos-db/account.bicep`)

### Microsoft.DocumentDB/databaseAccounts/sqlDatabases (2)

- **lightningDatabase** (`app/lightning-cosmos.bicep`)
- **database** (`core/cosmos-db/nosql/database.bicep`)

### Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers (7)

- **approvalsContainer** (`app/agents-approval-logicapp.bicep`)
- **episodesContainer** (`app/lightning-cosmos.bicep`)
- **rewardsContainer** (`app/lightning-cosmos.bicep`)
- **datasetsContainer** (`app/lightning-cosmos.bicep`)
- **trainingRunsContainer** (`app/lightning-cosmos.bicep`)
- **deploymentsContainer** (`app/lightning-cosmos.bicep`)
- **container** (`core/cosmos-db/nosql/container.bicep`)

### Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments (4)

- **cosmosRoleAssignmentLogicApp** (`app/agents-approval-logicapp.bicep`)
- **cosmosRoleAssignment** (`app/cosmos-RoleAssignment.bicep`)
- **cosmosRoleAssignmentAgent** (`app/agent-RoleAssignments.bicep`)
- **assignment** (`core/cosmos-db/nosql/role/assignment.bicep`)

### Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions (1)

- **definition** (`core/cosmos-db/nosql/role/definition.bicep`)

### Microsoft.Fabric/capacities (1)

- **fabricCapacity** (`core/fabric/fabric-capacity.bicep`)
  - SKU: skuName, Tier: Fabric

### Microsoft.Insights/components (1)

- **applicationInsights** (`core/monitor/applicationinsights.bicep`)

### Microsoft.Logic/workflows (1)

- **logicApp** (`app/agents-approval-logicapp.bicep`)

### Microsoft.ManagedIdentity/userAssignedIdentities (2)

- **userAssignedIdentity** (`core/identity/userAssignedIdentity.bicep`)
- **entraAppUserAssignedIdentity** (`core/apim/apim.bicep`)

### Microsoft.Network/privateDnsZones (10)

- **cognitiveServicesPrivateDnsZone** (`app/foundry-PrivateEndpoint.bicep`)
- **openAIPrivateDnsZone** (`app/foundry-PrivateEndpoint.bicep`)
- **servicesAIPrivateDnsZone** (`app/foundry-PrivateEndpoint.bicep`)
- **blobPrivateDnsZone** (`app/storage-PrivateEndpoint.bicep`)
- **queuePrivateDnsZone** (`app/storage-PrivateEndpoint.bicep`)
- **cosmosPrivateDnsZone** (`app/cosmos-PrivateEndpoint.bicep`)
- **fabricDfsPrivateDnsZone** (`app/fabric-PrivateEndpoint.bicep`)
- **fabricBlobPrivateDnsZone** (`app/fabric-PrivateEndpoint.bicep`)
- **fabricApiPrivateDnsZone** (`app/fabric-PrivateEndpoint.bicep`)
- **onelakeDfsPrivateDnsZone** (`app/fabric-PrivateEndpoint.bicep`)

### Microsoft.Network/privateDnsZones/A (2)

- **onelakeDfsARecord** (`app/fabric-PrivateEndpoint.bicep`)
- **onelakeBlobARecord** (`app/fabric-PrivateEndpoint.bicep`)

### Microsoft.Network/privateDnsZones/virtualNetworkLinks (10)

- **cognitiveServicesPrivateDnsZoneVirtualNetworkLink** (`app/foundry-PrivateEndpoint.bicep`)
- **openAIPrivateDnsZoneVirtualNetworkLink** (`app/foundry-PrivateEndpoint.bicep`)
- **servicesAIPrivateDnsZoneVirtualNetworkLink** (`app/foundry-PrivateEndpoint.bicep`)
- **blobPrivateDnsZoneVirtualNetworkLink** (`app/storage-PrivateEndpoint.bicep`)
- **queuePrivateDnsZoneVirtualNetworkLink** (`app/storage-PrivateEndpoint.bicep`)
- **cosmosPrivateDnsZoneVirtualNetworkLink** (`app/cosmos-PrivateEndpoint.bicep`)
- **fabricDfsPrivateDnsZoneVirtualNetworkLink** (`app/fabric-PrivateEndpoint.bicep`)
- **fabricBlobPrivateDnsZoneVirtualNetworkLink** (`app/fabric-PrivateEndpoint.bicep`)
- **fabricApiPrivateDnsZoneVirtualNetworkLink** (`app/fabric-PrivateEndpoint.bicep`)
- **onelakeDfsPrivateDnsZoneVirtualNetworkLink** (`app/fabric-PrivateEndpoint.bicep`)

### Microsoft.Network/privateEndpoints (5)

- **foundryPrivateEndpoint** (`app/foundry-PrivateEndpoint.bicep`)
- **blobPrivateEndpoint** (`app/storage-PrivateEndpoint.bicep`)
- **queuePrivateEndpoint** (`app/storage-PrivateEndpoint.bicep`)
- **cosmosPrivateEndpoint** (`app/cosmos-PrivateEndpoint.bicep`)
- **onelakePrivateEndpoint** (`app/fabric-PrivateEndpoint.bicep`)

### Microsoft.Network/privateEndpoints/privateDnsZoneGroups (5)

- **foundryPrivateEndpointDnsZoneGroup** (`app/foundry-PrivateEndpoint.bicep`)
- **blobPrivateDnsZoneGroupName** (`app/storage-PrivateEndpoint.bicep`)
- **queuePrivateDnsZoneGroupName** (`app/storage-PrivateEndpoint.bicep`)
- **cosmosPrivateDnsZoneGroup** (`app/cosmos-PrivateEndpoint.bicep`)
- **onelakePrivateEndpointDnsZoneGroup** (`app/fabric-PrivateEndpoint.bicep`)

### Microsoft.Network/publicIPAddresses (1)

- **publicIp** (`core/network/public-ip.bicep`)
  - SKU: sku, Tier: Regional

### Microsoft.Network/virtualNetworks (1)

- **virtualNetwork** (`app/vnet.bicep`)

### Microsoft.OperationalInsights/workspaces (1)

- **logAnalytics** (`core/monitor/loganalytics.bicep`)
  - SKU: PerGB2018

### Microsoft.Resources/deploymentScripts (3)

- **agentIdentityScript** (`core/identity/agentIdentity.bicep`)
- **federatedCredentialScript** (`core/identity/aksFederatedCredential.bicep`)
- **agentBlueprintScript** (`core/identity/agentIdentityBlueprint.bicep`)

### Microsoft.Resources/resourceGroups (1)

- **rg** (`main.bicep`)

### Microsoft.Search/searchServices (1)

- **searchService** (`core/search/search-service.bicep`)
  - SKU: sku

### Microsoft.Storage/storageAccounts (1)

- **storage** (`core/storage/storage-account.bicep`)

### Microsoft.Web/connections (2)

- **cosmosDbConnection** (`app/agents-approval-logicapp.bicep`)
- **teamsConnection** (`app/agents-approval-logicapp.bicep`)

### Microsoft.Web/serverfarms (1)

- **appServicePlan** (`core/host/appserviceplan.bicep`)

### Microsoft.Web/sites (1)

- **functions** (`core/host/functions-flexconsumption.bicep`)

## Key Cost-Related Parameters

- **embeddingModelCapacity** (int)
  - Default: `10`

- **fabricSkuName** (string)
  - Default: `F2`
  - Allowed: `F2`, `F4`, `F8`, `F16`, `F32`, `F64`, `F128`, `F256`, `F512`, `F1024`, `F2048`
