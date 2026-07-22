# SERPdive

The SERPdive tool connects your Dify agents and workflows to a web search API built for AI: one call returns clean, answer-ready content extracted from live pages instead of a list of links to fetch.

Quality is measured, not asserted: on a public 1,000-question benchmark judged blind by an independent model, SERPdive won 60.7% of decided quality duels against Tavily's default search while returning 20.2% fewer tokens at the same speed. The methodology and per-question results are open, so anyone can replay the run: [serpdive-benchmark](https://github.com/edendalexis/serpdive-benchmark).

## Available Actions

| Action | Description | Best For |
| --- | --- | --- |
| **Search** | Web search that returns extracted, answer-ready page content, best sources first | Real-time information, fact-checking, RAG, research agents |

Two retrieval depths:

- **Mako** (1 credit): fast, returns the fact-carrying sentences of each source.
- **Moby** (1.5 credits): returns the full readable content of every page, for when whole-page context is needed.

Optionally, the API also writes an answer built from the sources (`answer: true`, no extra credits): concise with Mako, detailed with numbered citations with Moby.

## Configuration

### 1. Get Your API Key

Sign up at [serpdive.com](https://serpdive.com) and create a key in the [dashboard](https://serpdive.com/dashboard/keys).

Every account gets **1,000 free credits every month**, no card required.

### 2. Install from Plugin Marketplace

Navigate to **Plugin Marketplace** in Dify and search for "SERPdive". Click **Install**.

### 3. Add Your API Key

Go to **Tools → SERPdive → Authentication** and paste your API key. Validating the key never spends credits.

### 4. Add a Tool node to your flow

Add a Node → Tool → SERPdive Search, or enable it as a tool in an Agent application.

## Common Patterns

**Fact-checking workflow:**
User question → SERPdive Search (answer: true) → LLM validates and responds

**Research agent:**
Topic → SERPdive Search (model: moby) → LLM synthesizes from full-page content

**Lean RAG:**
Query → SERPdive Search (max_results: 3) → LLM answers from the extracted content, with a smaller token bill

## Resources

- [SERPdive Docs](https://serpdive.com/docs)
- [Dashboard](https://serpdive.com/dashboard)
- [Public benchmark](https://github.com/edendalexis/serpdive-benchmark)
- Source repository: [github.com/serpdive/serpdive-dify-plugin](https://github.com/serpdive/serpdive-dify-plugin)
- Contact: contact@serpdive.com
