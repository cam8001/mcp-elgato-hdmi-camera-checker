"""
LLM Agent, implemented with Bedrock Agentcore, for checking HDMI camera compability.
"""

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

AGENT_ID = "elgato-hdmi-camera-check"
BEDROCK_MODEL = "amazon.nova-lite-v1:0"

app = BedrockAgentCoreApp()


@app.entrypoint
def my_agent(payload):
    """Main agent entrypoint for HDMI camera compatibility checking."""
    # read cameras.json into a string
    with open("cameras.json", "r", encoding="utf-8") as f:
        cameras = f.read()
    agent = Agent(
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

    prompt = payload.get("prompt")

    result = agent(prompt)

    return {"result": result}


if __name__ == "__main__":
    app.run()
