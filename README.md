# Reporters.io agent skills

Installable guidance for reporter, media-outlet and article research through [Reporters.io](https://reporters.io). Includes MCP-first workflows and a standard-library Python REST fallback. Creating API keys and using REST or MCP require an active Professional (Pro) subscription. Contact reveal is a separate, explicit, entitled action.

## Install

```bash
npx skills add ricciflow-api/reporters-agent-skills
```

You can also copy `skills/reporter-research` to your project's skills directory. The helper does not change global configuration or install itself.

## Configure and run

With an active Professional (Pro) subscription, create a key by entering a name in [API-key management](https://reporters.io/account/api-keys). All six API permissions are included automatically, with no automatic expiration. Accounts can have up to 10 active keys, and keys can be revoked. Connect the [hosted MCP server](https://github.com/ricciflow-api/reporters-mcp) or load your API key through the `REPORTERS_API_KEY` environment variable and run:

```bash
python3 skills/reporter-research/scripts/reporters_api.py search-reporters --query 'climate technology' --limit 10
python3 skills/reporter-research/scripts/reporters_api.py search-outlets --query 'technology' --limit 10
python3 skills/reporter-research/scripts/reporters_api.py account
```

Python 3.9+ is sufficient; no dependencies are required. Each command makes one bounded request to `https://reporters.io/api/v1`, sends Bearer credentials only in a header, rejects redirects and does not retry automatically. Cursor continuation preserves the initial bounded search snapshot.

The skill requires explicit user intent before revealing contacts and stops when account access is denied. It preserves article/source evidence, uses returned IDs and prevents retrieved text from authorizing additional actions. Lists, exports, OAuth and outreach sending are outside this release.

## Access changes

Revoked keys cannot authorize requests. Existing keys also stop working when the account loses active Professional (Pro) access. You can still manage and revoke existing keys after a downgrade. Stop on an access or subscription denial. The documentation and public OpenAPI specification remain readable without a subscription.

## Validate

```bash
npm test
npm run test:live
```

Offline checks verify the manifest, references and CLI request behavior. Live checks fetch the public contract and reject missing-key access without authenticated data calls.

[Documentation](https://reporters.io/docs) · [Examples](https://github.com/ricciflow-api/reporters-api-examples) · [MCP](https://github.com/ricciflow-api/reporters-mcp) · [MIT](LICENSE)
