#!/usr/bin/env python3
'''
Encodes an agentcore arn so that it can be accessed as an MCP endpoint. Requires cognito bearer token to access.

Usage: `python encode_arn.py <arn>`
'''

import sys

if len(sys.argv) != 2:
    print("Usage: python encode_arn.py <arn>")
    sys.exit(1)

arn = sys.argv[1]
encoded_arn = arn.replace(':', '%3A').replace('/', '%2F')
encoded_url = f"https://bedrock-agentcore.us-west-2.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
print(encoded_url)
