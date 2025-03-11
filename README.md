# Ragaman

A RAG (Retrieval-Augmented Generation) system for notes with support for REST API and Model Context Protocol (MCP).

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `DB_PATH` | Database file path | notes.db |
| `EMBEDDING_MODEL` | OpenAI embedding model | text-embedding-3-small |
| `MCP_NAME` | MCP server name | ragaman |
| `MCP_TRANSPORT` | MCP transport mode (stdio/http) | stdio |
| `MCP_HTTP_PORT` | MCP HTTP server port | 8080 |

