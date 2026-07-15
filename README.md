# AI Agent Tool (Python) — Give Your Agent Superpowers with MCP

Build your own **MCP server**, then connect an AI agent to it. MCP — the **Model Context
Protocol** — is the universal plug that lets any agent connect to any tool (a database, a file
system, a calendar, a company service) without you writing custom glue code for each one.

This is a small, self-contained project you can clone, run, and extend on its own. No course
enrollment required.

> Want the full, guided path from zero to shipping agents? This project is a companion to the
> **Agentic AI Systems Engineer** course by Emmanuel Naweji —
> **[www.emmanuelnaweji.com/courses](https://www.emmanuelnaweji.com/courses)**.

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

> *The server offers; the client asks.* Without MCP you wire every tool yourself: you write the
> function, **and** the description of it, **and** the loop. With MCP, the server hands the agent
> its tools automatically. You stop writing connection code by hand.

## Requirements

* **Python 3.11** (required — read below)
* An **OpenAI API key**

### Why Python 3.11 specifically

The MCP Python kit shares a dependency chain with common agent frameworks (e.g. CrewAI), which
depend on `tiktoken`. `tiktoken` uses a Rust component that does **not** build cleanly on Python
3.12, 3.13, or 3.14. Use Python **3.11** to avoid install headaches.

## Setup

```bash
# 1. Clone the project
git clone https://github.com/Here2ServeU/ai-agent-tool-python.git
cd ai-agent-tool-python

# 2. Make and open a Python 3.11 virtual environment
python3.11 -m venv venv
source venv/bin/activate          # Windows CMD: venv\Scripts\activate
                                  # Windows PS:  .\venv\Scripts\Activate.ps1

# 3. Check the version. It MUST say 3.11.x
python --version

# 4. Install the pieces
pip install -r requirements.txt   # or: pip install "mcp[cli]" openai

# 5. Set your OpenAI key. It is the only key you need
export OPENAI_API_KEY='sk-...'    # Windows CMD: set OPENAI_API_KEY=sk-...
                                  # Windows PS:  $env:OPENAI_API_KEY='sk-...'
```

> **Every new terminal, do this checklist:** go into this folder, open the venv, confirm
> `python --version` shows 3.11.x, then run your code.

## What's in this project

Two files, on purpose: one is the kitchen, one is the waiter. Keeping them separate is the
whole point — it shows that a tool and an agent are two independent things that only meet
through the MCP plug.

* [`weather_server.py`](weather_server.py): the **server** (the kitchen). It defines tools
  using `@mcp.tool()`. It starts with `get_forecast`, and also includes a second tool,
  `packing_advice`. It's written this way to prove the big promise of MCP: you can add a second
  tool to the server without touching the agent at all. The agent discovers it on its own.
* [`mcp_agent.py`](mcp_agent.py): the **client** (the waiter). This is the only file you run.
  It quietly launches the server for you, asks it "what tools do you have?" (`list_tools`),
  and lets the model decide which tool to call (`call_tool`). Notice what's missing: you never
  write a tool description by hand. The server provides it. That missing work is exactly the
  point of MCP.

## Run it

```bash
python3 mcp_agent.py        # Windows: python mcp_agent.py
```

> On **Windows**, if `python3` is not recognized, change `command="python3"` to
> `command="python"` in `mcp_agent.py`.

## Try these exercises

1. **Build the server:** [`weather_server.py`](weather_server.py). Run it once on its own to
   watch it start and wait quietly: `python3 weather_server.py`. With no server, there is no
   tool. Press `Ctrl+C` to stop it.
2. **Run the agent:** [`mcp_agent.py`](mcp_agent.py). You only run **this** file; it launches
   the server for you. Watch the `TOOL:` line appear, then the final answer.
3. **Add a tool without touching the agent** (the most important exercise). The server already
   has `packing_advice` next to `get_forecast`. Run a goal that needs both, and watch the agent
   discover and call them in order, with **zero** edits to `mcp_agent.py`. That is
   *build once, use everywhere.*
4. **Design a tool for your own world.** Add a third `@mcp.tool()` for a money or health use
   case. The agent reads the little description you write above the tool to decide when to use
   it, so write it clearly.

## Why it matters

You never typed a tool description; the server handed it over through `list_tools`. You never
wired the tool into the loop by hand; the protocol did it. To give the agent a tenth tool, you
don't touch the agent file at all. You add the tool to the server, and the agent finds it the
next time it connects. That is the whole gift of MCP.

## Words to know

| Word | What it means in plain English |
| --- | --- |
| **MCP** | Model Context Protocol. One agreed plug shape; USB-C for AI agents. |
| **Server** | The program that offers tools (the kitchen). |
| **Client** | The program that connects and uses tools (the waiter). |
| **FastMCP** | The easy Python builder; it handles the protocol so you just describe your tools. |
| **`@mcp.tool()`** | A tag that turns a normal function into a tool the server offers. |
| **`list_tools`** | The client asking the server what it can do; this replaces the hand-written description. |
| **`call_tool`** | The client asking the server to actually run a tool. |
| **`initialize`** | The opening handshake where both sides confirm they speak MCP. |
| **stdio** | The simple channel used to launch and talk to a local server. |

## Learn the whole system

This project shows one piece — connecting an agent to a tool over MCP. The
**Agentic AI Systems Engineer** course walks you through the full journey: what an agent is,
your first real agent, memory and multi-step reasoning, RAG, multi-agent teams, MCP,
observability, and a production-grade capstone.

👉 **[www.emmanuelnaweji.com/courses](https://www.emmanuelnaweji.com/courses)** — Agentic AI
Systems Engineer, by Emmanuel Naweji.

## License

Released under the terms in [`LICENSE`](LICENSE). Use it, fork it, build on it.
