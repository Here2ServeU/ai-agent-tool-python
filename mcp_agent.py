# mcp_agent.py — the client (the "waiter") that connects to weather_server.py
# Install: pip install "mcp[cli]" openai
# Python:  3.11 required
# Key:     export OPENAI_API_KEY='sk-...'  (macOS/Linux)
#          set OPENAI_API_KEY=sk-...        (Windows CMD)
# Run:     python3 mcp_agent.py   (macOS/Linux)
#          python  mcp_agent.py   (Windows)
#
# You only run THIS file. It launches weather_server.py for you (one command,
# no second terminal). The agent asks the server what tools it has
# (list_tools) — you never write the tool schema by hand like in Module 4 —
# then GPT-4o decides which tool to call (call_tool).

import asyncio, json
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = OpenAI()
# On Windows, if "python3" is not recognized, change command to "python".
server = StdioServerParameters(command="python3", args=["weather_server.py"])


async def run_agent(goal):
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tool_list = await session.list_tools()
            tools = [{
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                }
            } for t in tool_list.tools]

            messages = [{"role": "user", "content": goal}]
            while True:
                r = client.chat.completions.create(
                    model="gpt-4o", messages=messages, tools=tools)
                m = r.choices[0].message
                if not m.tool_calls:
                    print(m.content)
                    return
                messages.append(m)
                for tc in m.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = await session.call_tool(tc.function.name, args)
                    text = result.content[0].text
                    print(f"TOOL: {tc.function.name} | RESULT: {text}")
                    messages.append({"role": "tool",
                        "tool_call_id": tc.id, "content": text})


# Lab 8.2 goal: one tool.
#   asyncio.run(run_agent("What is the weather in Chicago today?"))
# Lab 8.3 goal: two tools — same agent file, no edits, it discovers
# packing_advice on the server automatically and calls both in order.
asyncio.run(run_agent(
    "What is the weather in Miami today, and what should I pack?"))
