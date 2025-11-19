# Backstage MCP Server

A MCP (Model Context Protocol) server that provides tools to interact with your instance of [Backstage](https://backstage.io/) software catalog. This server allows you to list entities, get entity details, and view ancestry information from your Backstage instance.

## Features

- **List Entities**: Query Backstage entities with optional filtering by kind and namespace
- **Get Entity**: Retrieve detailed information about a specific entity
- **Get Entity Ancestry**: View the ancestry chain for any entity
- **Bearer Token Authentication**: Secure authentication support for Backstage API

## Installation

This MCP server is designed to run in a Docker container. You can use it through the [Docker MCP Registry](https://github.com/docker/mcp-registry) or run it locally.

### Prerequisites

- Docker Desktop
- Python 3.11+ (for local development)

### Running with Docker

```bash
docker build -t backstage-mcp .
docker run -e BACKSTAGE_BEARER_TOKEN=your_token_here -e BACKSTAGE_API_BASE=https://backstage.example.com/API/catalog backstage-mcp
```

## Configuration

The server requires the following environment variables:

- `BACKSTAGE_API_BASE` (optional): Base URL for your Backstage API catalog endpoint. Defaults to `https://backstage.mintel.cloud/API/catalog`
- `BACKSTAGE_BEARER_TOKEN` (optional): Bearer token for Backstage API authentication

## Tools

### `list_entities`

List entities in Backstage, optionally filtered by kind and namespace.

**Parameters:**
- `kind` (optional): Entity kind filter (e.g., 'Component', 'API', 'System')
- `namespace` (optional): Namespace filter
- `limit` (optional): Maximum number of entities to return (default: 10)

### `get_entity`

Get a Backstage entity by kind, namespace, and name.

**Parameters:**
- `kind` (required): Entity kind (e.g., 'Component', 'API', 'System')
- `namespace` (required): Entity namespace
- `name` (required): Entity name

### `get_entity_ancestry`

Get ancestry information for a Backstage entity.

**Parameters:**
- `kind` (required): Entity kind
- `namespace` (required): Entity namespace
- `name` (required): Entity name

### `set_bearer_token`

Set the bearer token for Backstage API requests at runtime.

**Parameters:**
- `token` (required): Bearer token for Backstage API authentication

## Development

### Local Setup

1. Clone this repository:
```bash
git clone https://github.com/timinter/backstage-mcp-server.git
cd backstage-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python backstage.py
```

### Building the Docker Image

```bash
docker build -t backstage-mcp .
```

## Contributing

This project is part of the [Docker MCP Registry](https://github.com/docker/mcp-registry). To contribute:

1. Fork the MCP Registry repository
2. Follow the [contributing guidelines](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)
3. Submit a pull request

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## Related Links

- [Backstage Documentation](https://backstage.io/docs)
- [Backstage API Documentation](https://backstage.io/docs/features/software-catalog/software-catalog-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Docker MCP Registry](https://github.com/docker/mcp-registry)

