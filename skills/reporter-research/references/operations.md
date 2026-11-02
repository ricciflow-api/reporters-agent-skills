# Public operations

Creating API keys and all REST API and MCP use require an active Professional (Pro) subscription. Public documentation and OpenAPI remain readable without a subscription.

REST base: `https://reporters.io/api/v1`. Use one `Authorization: Bearer` header loaded from `REPORTERS_API_KEY`. API keys do not go in URL query parameters.

| REST operation | MCP tool | Scope |
| --- | --- | --- |
| `GET /account` | `get_account` | `account:read` |
| `POST /reporters/search` | `search_reporters` | `reporters:read` |
| `GET /reporters/{reporter_id}` | `get_reporter` | `reporters:read` |
| `GET /reporters/{reporter_id}/articles` | `list_reporter_articles` | `articles:read` |
| `POST /reporters/{reporter_id}/contacts/reveal` | `reveal_reporter_contacts` | `contacts:read` plus current entitlement |
| `POST /outlets/search` | `search_outlets` | `outlets:read` |
| `GET /outlets/{outlet_id}` | `get_outlet` | `outlets:read` |
| `GET /outlets/{outlet_id}/reporters` | `list_outlet_reporters` | `outlets:read` |
| `GET /outlets/{outlet_id}/articles` | `list_outlet_articles` | `articles:read` |
| `POST /outlets/{outlet_id}/contacts/reveal` | `reveal_outlet_contacts` | `contacts:read` plus current entitlement |
| `GET /metadata/search-filters` | `get_search_filters` | `metadata:read` |

Search JSON accepts `query`, `region`, `country`, `limit`, `cursor`; reporter search also accepts `beats` (array) and `state`. Use supported values from search filters. Query and geography identify the research target; contacts remain separate. Contact reveal sends `{}` and requires explicit intent. The server applies current plan, scope, contact availability and suppression checks.

Profile objects expose `id`; use that value as the corresponding `reporter_id` or `outlet_id` input. Reporter article lists have a fixed page size of 20; outlet reporter/article lists have a fixed page size of 25 and accept `cursor`, not `limit`. Full article text is excluded. All operations, including country/state filtering, contact reveal and content lists, require active Professional (Pro) access in addition to the listed key scope. `/account` returns plan, capabilities and key scopes.

Search/list results are nested in `data` and include `items`, `next_cursor`, `has_more`, `total` and `limit`; search may include `snapshot_expires_at`. Repeat the same filter set and limit when continuing a cursor. Do not reuse another account's cursor or change filters mid-snapshot. An expired cursor requires a deliberate new search rather than an automatic unbounded restart.

Do not retry automatically. For a deliberate reveal retry, send the same `Idempotency-Key` with identical inputs. The receipt window is 24 hours; reuse identifies the same operation while the server rechecks entitlement and contact suppression. Do not cache private contact responses as a substitute for current authorization.

A 401 requires valid credentials, 403 requires the appropriate scope and active Professional (Pro) access, and 429 requires respecting the reported retry interval. Revoked or expired keys cannot authorize requests; keys also stop working when an account loses active Pro access. The user can still manage and revoke existing keys after a downgrade. Stop on access denial instead of trying another account or interface. Do not interpret errors as an empty result. Keep returned request IDs for support without exposing key values or contact bodies in logs. Lists, exports and OAuth are deferred.
