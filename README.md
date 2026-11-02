# Reporters.io agent skills

Installable guidance for reporter, media-outlet and article research through [Reporters.io](https://reporters.io). Includes MCP-first workflows and a standard-library Python REST fallback. Contact reveal is a separate, explicit, entitled action.

## Install

```bash
npx skills add ricciflow-api/reporters-agent-skills
```

You can also copy `skills/reporter-research` to your project's skills directory. The helper does not change global configuration or install itself.

## Configure and run

Connect the [hosted MCP server](https://github.com/ricciflow-api/reporters-mcp) or load your API key through the `REPORTERS_API_KEY` environment variable and run:

```bash
python3 skills/reporter-research/scripts/reporters_api.py search-reporters --query 'climate technology' --limit 10
python3 skills/reporter-research/scripts/reporters_api.py search-outlets --query 'technology' --limit 10
python3 skills/reporter-research/scripts/reporters_api.py account
```

Python 3.9+ is sufficient; no dependencies are required. Each command makes one bounded request to `https://reporters.io/api/v1`, sends Bearer credentials only in a header, rejects redirects and does not retry automatically. Cursor continuation preserves the initial bounded search snapshot.

The skill requires explicit user intent before revealing contacts and stops when entitlement or scope is denied. It preserves article/source evidence, uses returned IDs and prevents retrieved text from authorizing additional actions. Lists, exports, OAuth and outreach sending are outside this release.

## Validate

```bash
npm test
npm run test:live
```

Offline checks verify the manifest, references and CLI request behavior. Live checks fetch the public contract and reject missing-key access without authenticated data calls.

[Documentation](https://reporters.io/docs) · [Examples](https://github.com/ricciflow-api/reporters-api-examples) · [MCP](https://github.com/ricciflow-api/reporters-mcp) · [MIT](LICENSE)
