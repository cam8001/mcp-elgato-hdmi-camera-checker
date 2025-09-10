# Bedrock AgentCore MCP Server Authentication

## Authentication Overview

Bedrock AgentCore MCP servers use **dual authentication**:

1. **IAM Execution Role** (for runtime)
2. **OAuth/Cognito** (for client access)

## Authentication Methods

### 1. IAM Execution Role (Runtime)
- Used by the AgentCore Runtime for AWS service access
- Configured during deployment via `agentcore configure`
- Uses MicroVM Metadata Service (MMDS) similar to EC2 IMDS
- Follows principle of least privilege

### 2. OAuth/Cognito (Client Access)
- **Required** for invoking deployed MCP servers
- Must set up Cognito user pool for authentication
- Clients need Bearer tokens to access the server
- **Cannot use raw AWS IAM credentials for client invocation**

## Deployment Process

```bash
# 1. Configure with IAM execution role
agentcore configure -e my_mcp_server.py --protocol MCP

# 2. Deploy (uses IAM role for runtime)
agentcore launch

# 3. Invoke (requires Bearer token)
export BEARER_TOKEN="your_oauth_token"
export AGENT_ARN="arn:aws:bedrock-agentcore:us-west-2:account:runtime/name"
```

## Client Invocation Example

```python
# Requires Bearer token, not IAM credentials
headers = {
    "authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

encoded_arn = agent_arn.replace(':', '%3A').replace('/', '%2F')
mcp_url = f"https://bedrock-agentcore.us-west-2.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
```

## Key Limitations

- **No direct IAM credential access** for clients
- **Cognito OAuth is mandatory** for client authentication
- Runtime uses IAM internally but clients cannot bypass OAuth

## Best Practices

- Use least privilege for IAM execution role
- Secure Cognito user pool configuration
- Rotate Bearer tokens regularly
- Avoid privilege escalation in execution role
