"""
LLM Agent, implemented with Bedrock Agentcore, for checking HDMI camera compability.
"""

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

from mcp.server.fastmcp import FastMCP

# Agentcore expects MCP server containers to be available at the path 0.0.0.0:8000/mcp
# @see https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp.html#runtime-mcp-how-it-works
mcp = FastMCP(host="0.0.0.0", stateless_http=True)

AGENT_ID = "elgato-hdmi-camera-check"
BEDROCK_MODEL = "amazon.nova-micro-v1:0"


def init_agent():
    """Initialize the agent."""
    # read cameras.json into a string
    with open("cameras.json", "r", encoding="utf-8") as f:
        cameras = f.read()
    this_agent = Agent(
        model=BEDROCK_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": """
                        You are an assistant that helps users identify whether a given camera model supports realtime HDMI output. You use a list provided by Elgato, a company that makes devices for streamers, to check.

                        "The user will provde one or more camera models or brands and you will report back on whether they support HDMI put and any extra detail that might be relevant.
                        """
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"text": "Here is the list of cameras that Elgato has tested. When referring to results from the list, refer to the list as 'the list of Elgato Tested Devices': " + cameras}],
            },
        ],
    )

    return this_agent


# Keep agent in global namespace, so we don't need to pass it to our MCP tool.
# MCP decorators do not expect complex types in paramters.
agent = init_agent()


@mcp.tool()
def check_camera(camera_name: str) -> str:
    """Check if a camera supports HDMI output."""
    print("Checking camera: " + camera_name)
    print("Using model: " + BEDROCK_MODEL)
    result = agent(camera_name)
    # Return text if available, blank string if not
    print(result)
    return str(result.message["content"][0].get("text", ""))


app = BedrockAgentCoreApp()


@app.entrypoint
def my_agent(payload):
    """Entrypoint for the agentcore agent."""
    print(payload)
    prompt = payload.get("prompt")
    result = check_camera(prompt)

    return {"result": result}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
