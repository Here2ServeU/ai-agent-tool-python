# Module 8 · Giving Agents Superpowers with MCP

*Build your own MCP server, then connect an agent to it. MCP, the Model Context Protocol, is
the universal plug that lets any agent connect to any tool (a database, a file system, a
calendar, a company service) without you writing custom glue code for each one.*

## MCP is like USB-C for AI agents

Remember when every phone and gadget had its own charger, and none of them fit each other?
Then USB-C came along: one plug shape that fits everything. You stopped worrying about which
cable went with which device.

**MCP is that one plug shape, but for AI tools.** Any tool that speaks MCP can plug into any
agent that speaks MCP. No custom glue. You build a tool once, and every agent can use it.

There are only two sides to it:

* **Server:** the tool itself. Think of it as the *kitchen*. It posts a menu of what it can
  do (`list_tools`) and does the work when an agent asks (`call_tool`).
* **Client:** the agent, or the program speaking for it. Think of it as the *waiter*. It
  reads the menu and carries the order to the kitchen.

> *The server offers; the client asks.* Back in Module 4 you hand wired every tool yourself:
> you wrote the function, **and** the description of it, **and** the loop. With MCP, the
> server hands the agent its tools automatically. You stop writing connection code by hand.

## Important: you must use Python 3.11 (read this before you install)

The MCP Python kit shares the same chain of dependencies as CrewAI. CrewAI depends on
`tiktoken`, which uses a Rust piece that does **not** work with Python 3.12, 3.13, or 3.14.
Use Python **3.11**. You can even reuse the same venv from Module 7.

## Setup

```bash
# 1. Make and open a Python 3.11 lunchbox (or reuse Module 7's)
python3.11 -m venv venv
source venv/bin/activate          # Windows CMD: venv\Scripts\activate
                                  # Windows PS:  .\venv\Scripts\Activate.ps1

# 2. Check the version. It MUST say 3.11.x
python --version

# 3. Install the pieces
pip install "mcp[cli]" openai     # or: pip install -r requirements.txt

# 4. Set your OpenAI key. It is the only key you need
export OPENAI_API_KEY='sk-...'    # Windows CMD: set OPENAI_API_KEY=sk-...
                                  # Windows PS:  $env:OPENAI_API_KEY='sk-...'
```

> **Every new terminal, do this checklist:** go into this folder, open the venv, confirm
> `python --version` shows 3.11.x, then run your code.

## Why the files in this folder look the way they do

This module has two files on purpose: one is the kitchen, one is the waiter. Keeping them
separate is the whole point, because it shows that a tool and an agent are two independent
things that only meet through the MCP plug.

* [`weather_server.py`](weather_server.py): the **server** (the kitchen). It defines tools
  using `@mcp.tool()`. It starts with `get_forecast`, and it also includes a second tool,
  `packing_advice`. It is written this way to prove the big promise of MCP: you can add a
  second tool to the server without touching the agent at all. The agent will discover it on
  its own.
* [`mcp_agent.py`](mcp_agent.py): the **client** (the waiter). This is the only file you run.
  It quietly launches the server for you, asks it "what tools do you have?" (`list_tools`),
  and lets GPT-4o decide which tool to call (`call_tool`). Notice what is missing compared to
  Module 4: you never write a tool description by hand. The server provides it. That missing
  work is exactly the point of MCP.

## Lab

1. **Build the server:** [`weather_server.py`](weather_server.py). Run it once on its own to
   watch it start and wait quietly: `python3 weather_server.py`. With no server, there is no
   tool. Press `Ctrl+C` to stop it.
2. **Build the agent:** [`mcp_agent.py`](mcp_agent.py). You only run **this** file; it launches
   the server for you. Watch the `TOOL:` line appear, then the final answer.
3. **Add a second tool without touching the agent** (this is the most important lab). The
   server already has `packing_advice` next to `get_forecast`. Run a goal that needs both, and
   watch the agent discover and call them in order, with **zero** edits to `mcp_agent.py`.
   That is *build once, use everywhere.*
4. **Design a tool for your own world.** Add a third `@mcp.tool()` for a money or health use
   case. The agent reads the little description you write above the tool to decide when to use
   it, so write it clearly.

```bash
python3 mcp_agent.py        # Windows: python mcp_agent.py
```

> On **Windows**, if `python3` is not recognized, change `command="python3"` to
> `command="python"` in `mcp_agent.py`.

## Why it matters

You never typed a tool description; the server handed it over through `list_tools`. You never
wired the tool into the loop by hand; the protocol did it. To give the agent a tenth tool, you
do not touch the agent file at all. You add the tool to the server, and the agent finds it the
next time it connects. That is the whole gift of MCP.

## Words to know

| Word | What it means in plain English |
| --- | --- |
| **MCP** | Model Context Protocol. One agreed plug shape; USB-C for AI agents. |
| **Server** | The program that offers tools (the kitchen). |
| **Client** | The program that connects and uses tools (the waiter). |
| **FastMCP** | The easy Python builder; it handles the protocol so you just describe your tools. |
| **`@mcp.tool()`** | A tag that turns a normal function into a tool the server offers. |
| **`list_tools`** | The client asking the server what it can do; this replaces the hand written description. |
| **`call_tool`** | The client asking the server to actually run a tool. |
| **`initialize`** | The opening handshake where both sides confirm they speak MCP. |
| **stdio** | The simple channel used to launch and talk to a local server. |
