# SERPdive Dify Plugin

Official [Dify](https://dify.ai) plugin for [SERPdive](https://serpdive.com), the AI Search API: web search that returns clean, answer-ready content extracted from live pages instead of a list of links. Same speed as Tavily, 20.2% fewer tokens, 60.7% of decided quality duels won on a [public benchmark](https://github.com/edendalexis/serpdive-benchmark).

The plugin source lives in [`serpdive/`](serpdive/), see its [README](serpdive/README.md) for setup and usage. It is distributed through the [Dify Marketplace](https://marketplace.dify.ai).

## Development

```bash
cd serpdive
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # fill in a remote-debug key from a Dify instance
.venv/bin/python -m main
```

Package for the marketplace with the [Dify plugin CLI](https://github.com/langgenius/dify-plugin-daemon/releases):

```bash
dify plugin package ./serpdive
```

## Contact

contact@serpdive.com
