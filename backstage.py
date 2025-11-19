from typing import Any, Optional
import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("backstage")

# Constants
BACKSTAGE_API_BASE = os.getenv("BACKSTAGE_API_BASE")
USER_AGENT = "backstage-mcp/1.0"

# Bearer token for authentication (from environment variable)
BACKSTAGE_BEARER_TOKEN: Optional[str] = os.getenv("BACKSTAGE_BEARER_TOKEN")

@mcp.tool()
def set_bearer_token(token: str) -> str:
    """Set the bearer token for Backstage API requests."""
    global BACKSTAGE_BEARER_TOKEN
    BACKSTAGE_BEARER_TOKEN = token
    return "Bearer token set."

async def make_backstage_request(
    method: str, url: str, params: Optional[dict] = None, json: Optional[dict] = None
) -> dict[str, Any] | None:
    """Make a request to the Backstage API with error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    if BACKSTAGE_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {BACKSTAGE_BEARER_TOKEN}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, headers=headers, params=params, json=json, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_entity(entity: dict) -> str:
    """Format a Backstage entity into a readable string."""
    meta = entity.get("metadata", {})
    kind = entity.get("kind", "Unknown")
    name = meta.get("name", "Unknown")
    namespace = meta.get("namespace", "default")
    desc = meta.get("description", "")
    return f"{kind}:{namespace}/{name}\nDescription: {desc}"

@mcp.tool()
async def list_entities(kind: Optional[str] = None, namespace: Optional[str] = None, limit: int = 10) -> str:
    """List entities in Backstage, optionally filtered by kind and namespace."""
    params: dict[str, Any] = {"limit": limit}
    if kind or namespace:
        filters = []
        if kind:
            filters.append(f"kind={kind}")
        if namespace:
            filters.append(f"metadata.namespace={namespace}")
        params["filter"] = ",".join(filters)
    url = f"{BACKSTAGE_API_BASE}/entities"
    data = await make_backstage_request("GET", url, params=params)
    if not data:
        return "Unable to fetch entities."
    entities_list = data.get("items", data) if isinstance(data, dict) else data
    if not isinstance(entities_list, list):
        return "No entities found."
    entities = [format_entity(e) for e in entities_list if isinstance(e, dict)]
    return "\n---\n".join(entities) if entities else "No entities found."

@mcp.tool()
async def get_entity(kind: str, namespace: str, name: str) -> str:
    """Get a Backstage entity by kind, namespace, and name."""
    url = f"{BACKSTAGE_API_BASE}/entities/by-name/{kind}/{namespace}/{name}"
    entity = await make_backstage_request("GET", url)
    if not entity:
        return "Entity not found."
    return format_entity(entity)

@mcp.tool()
async def get_entity_ancestry(kind: str, namespace: str, name: str) -> str:
    """Get ancestry information for a Backstage entity."""
    url = f"{BACKSTAGE_API_BASE}/entities/by-name/{kind}/{namespace}/{name}/ancestry"
    data = await make_backstage_request("GET", url)
    if not data or "items" not in data:
        return "Unable to fetch ancestry."
    ancestry = []
    for item in data["items"]:
        entity = item.get("entity", {})
        ancestry.append(format_entity(entity))
    return "\n---\n".join(ancestry) if ancestry else "No ancestry found."

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')