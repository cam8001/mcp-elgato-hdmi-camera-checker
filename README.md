# Elgato HDMI Camera Check

An AI-powered assistant built with **Amazon Bedrock AgentCore** that helps users identify whether camera models support real-time HDMI output using Elgato's tested device database.

## Overview

This project is built using the **Amazon Bedrock AgentCore framework**, which provides a streamlined way to develop, test, and deploy AI agents. The agent answers questions about camera HDMI compatibility based on Elgato's comprehensive list of tested devices.

## Built with Bedrock AgentCore

This project leverages the **Amazon Bedrock AgentCore Starter Toolkit** for:

- **Local Development & Testing**: Run and test the agent locally before deployment
- **Automated Build Process**: Containerization and deployment handled by the toolkit
- **AWS Integration**: Seamless deployment to AgentCore Runtime with automatic IAM role creation
- **Observability**: Built-in CloudWatch integration for monitoring and debugging

### AgentCore Architecture

The application follows the Bedrock AgentCore pattern:
- Uses `BedrockAgentCoreApp()` as the main application framework
- Implements the `@app.entrypoint` decorator for the main agent function
- Integrates with Strands Agents for AI model interaction
- Follows containerized deployment standards

## Features

- Query camera HDMI compatibility from Elgato's tested device database
- Get detailed information about connection types, power requirements, and setup guides
- Powered by Amazon Bedrock Nova Lite model
- Built-in observability and monitoring via AgentCore
- Production-ready containerized deployment

## Prerequisites

- **AWS Account** with credentials configured
- **Python 3.10+** installed
- **Boto3** installed
- **AWS Permissions**: AgentCore deployment permissions (see [AgentCore permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html))
- **Model Access**: Amazon Bedrock Nova Lite model enabled

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd elgato-hdmi-camera-check
```

2. Install Bedrock AgentCore and dependencies:
```bash
# create a virtual environment
python3 -m venv .venv-elgato-agent
pip install --upgrade pip
# install the dependencies needed to run the agent
pip install -r requirements.txt
# ... and a toolkit which includes the 'agentcore' cli.
pip install bedrock-agentcore-starter-toolkit
```

## Development & Testing with AgentCore

### Local Testing

1. **Start the agent locally**:
```bash
source elgato-agent/bin/activate
python elgato_mcp.py
```

2. **Test with curl**:
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Does the Sony a6000 support HDMI output?"}'
```

### AgentCore Toolkit Commands

The project includes a `.bedrock_agentcore.yaml` configuration file for the AgentCore toolkit.

**Configure the agent** (if needed):
```bash
agentcore configure -e elgato_mcp.py
```

**Deploy to AgentCore Runtime**:
```bash
agentcore launch
```

**Test deployed agent**:
```bash
agentcore invoke '{"prompt": "What cameras from Canon work with HDMI streaming?"}'
```

**View logs and monitoring**:
The toolkit automatically sets up CloudWatch logging. Check the output from `agentcore launch` for log locations.

## Deployment Options

### Option 1: AgentCore Toolkit (Recommended)
Uses the Bedrock AgentCore Starter Toolkit for automated deployment:
- Automatic IAM role creation
- Container image building via CodeBuild
- ECR repository management
- AgentCore Runtime provisioning

### Option 2: Manual Docker Deployment
For custom deployment scenarios:
```bash
docker build -t elgato-hdmi-camera-check .
docker run -p 8080:8080 -p 8000:8000 elgato-hdmi-camera-check
```

## Usage Examples

### Query Examples
- "Does the Sony a6000 support HDMI output?"
- "What cameras from Canon work with HDMI streaming?"
- "Tell me about the HDMI compatibility of the Panasonic GH5"
- "Which Nikon cameras have clean HDMI output?"

### SDK Integration
```python
import json
import boto3

# Initialize the AgentCore client
agent_core_client = boto3.client('bedrock-agentcore')

# Prepare the payload
payload = json.dumps({"prompt": "Does the Sony a7III support HDMI?"}).encode()

# Invoke the agent (replace with your agent ARN)
response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn="your-agent-arn",
    payload=payload
)

# Process response
content = []
for chunk in response.get("response", []):
    content.append(chunk.decode('utf-8'))
print(json.loads(''.join(content)))
```

## Project Structure

```
├── elgato_mcp.py              # Main AgentCore application
├── cameras.json               # Elgato's tested camera database
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── .bedrock_agentcore.yaml    # AgentCore toolkit configuration
├── .dockerignore              # Docker ignore rules
└── elgatomcp/                 # Virtual environment directory
```

## Camera Database

The `cameras.json` file contains Elgato's comprehensive list of tested cameras with:
- Manufacturer and model information
- Maximum resolution support
- Clean HDMI output capability
- Unlimited runtime support
- Connection type details
- Power requirements
- Setup guides and quality samples

## Configuration

### Environment Variables
- `AWS_REGION`: AWS region (default: ap-southeast-2)
- `AWS_DEFAULT_REGION`: Default AWS region
- `DOCKER_CONTAINER`: Set to 1 when running in Docker

### AgentCore Configuration
The `.bedrock_agentcore.yaml` file contains AgentCore-specific settings managed by the toolkit.

## Observability

This project includes built-in observability through Bedrock AgentCore:
- **CloudWatch Logs**: Automatic log aggregation
- **Transaction Search**: Trace agent interactions
- **Performance Monitoring**: Built-in metrics collection

Enable observability by following the [AgentCore observability guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html).

## Dependencies

- `bedrock-agentcore`: Amazon Bedrock AgentCore SDK for building AI agents
- `strands-agents`: Agent orchestration library
- `aws-opentelemetry-distro`: AWS observability instrumentation
- `bedrock-agentcore-starter-toolkit`: CLI toolkit for deployment (development only)

## Troubleshooting

### Common Issues
- **Permission denied**: Verify AWS credentials with `aws sts get-caller-identity`
- **Model access**: Ensure Nova Lite model is enabled in Bedrock console
- **Docker warnings**: Can be ignored when using CodeBuild deployment

For detailed troubleshooting, see the [AgentCore troubleshooting guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html).

## Learn More

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [AgentCore Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)
- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/docs/)

## License

[Add your license information here]
