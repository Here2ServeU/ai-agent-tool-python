# weather_server.py — your first MCP server
# Install: pip install "mcp[cli]" openai
# Python:  3.11 required (shared dependency chain with CrewAI)
# Run:     python3 weather_server.py   (macOS/Linux)
#          python  weather_server.py   (Windows)
#
# The server is the "kitchen": it posts a menu of tools and does the work
# when an agent asks. Leave it defined here — the agent (mcp_agent.py)
# launches it for you, so you only run one command.

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")


@mcp.tool()
def get_forecast(city: str) -> str:
    """Get today's weather forecast for a city."""
    fake_weather = {
        "chicago": "Sunny, 72 degrees, light wind.",
        "miami": "Cloudy, 86 degrees, chance of rain.",
        "sioux falls": "Clear, 74 degrees, dry.",
        "dallas": "Clear, 94 degrees, dry.",
    }
    return fake_weather.get(city.lower(), "No forecast available for that city.")


# ── Lab 8.3: the second tool — added to the server, with ZERO changes to the agent.
# This is the whole promise of MCP: build the tool once, every agent discovers it.
@mcp.tool()
def packing_advice(forecast: str) -> str:
    """Suggest what to pack based on a weather forecast."""
    if "rain" in forecast.lower():
        return "Bring an umbrella and a waterproof jacket."
    if "sunny" in forecast.lower() or "clear" in forecast.lower():
        return "Bring sunglasses and sunscreen."
    return "Dress in comfortable layers."


if __name__ == "__main__":
    mcp.run()
