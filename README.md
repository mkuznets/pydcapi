# pydcapi: Unofficial Python library for Adobe Document Cloud

[![PyPI - Version](https://img.shields.io/pypi/v/pydcapi)](https://pypi.org/project/pydcapi/)

`pydcapi` is a typed client for the private API behind [Acrobat web](https://acrobat.adobe.com)
(`dc-api-v2.adobe.io`): folders, assets, uploads, PDF operations, jobs, user info.
It is generated from Adobe's own discovery document and JSON schemas, so every
operation returns a pydantic model.

It is **unofficial**. It uses the same session mechanism as the web app, so it
can break without notice and it is your responsibility to stay within Adobe's terms.

## Install

```
pip install pydcapi
```

Python 3.10+. Dependencies: `httpx2`, `pydantic>=2`, `uritemplate`.

## Quickstart

```python
import pydcapi
from pydcapi import credentials

client = pydcapi.Client(credentials.JSONFileCredentialsProvider("credentials.json"))

me = client.users.get_user(fields="identity")
print(me.identity.email)

root = client.folders.get_system_folders().roots.document_cloud.root_uri
listing = client.folders.list(folder_uri=str(root), order_by="name", sort_order="ascending")
for member in listing.members:
    print(member.name)
```

## Authentication

There is no public OAuth client for this API. Authentication piggybacks on the
browser session of a logged-in Acrobat web user:

| Credential | Lifetime | Where it comes from |
|---|---|---|
| `ims_sid` | long-lived session cookie | your browser, after logging in to acrobat.adobe.com |
| `aux_sid` | long-lived session cookie | same; **optional**, `ims_sid` alone is enough |
| `token` | 24 hours | minted automatically from `ims_sid` via Adobe IMS |
| `expiry` | hours | schema expiry timestamp, fetched automatically |

You only ever need to supply `ims_sid`. The client obtains and renews the
access token on its own, and hands renewed values back to your
`CredentialsProvider`, so a provider that persists (`JSONFileCredentialsProvider`)
keeps itself up to date.

Treat `ims_sid` like a password: it is a full login to your Adobe account.

### Getting `ims_sid` from the browser

1. Open https://acrobat.adobe.com/link/home/ in Chrome and sign in.
2. Open DevTools (Cmd+Opt+I), go to **Application > Storage > Cookies**.
3. Select `https://acrobat.adobe.com`, find the cookie named `ims_sid`
   (domain `.services.adobe.com`). It is a ~770 character opaque string.
4. Copy its value. Optionally also copy `aux_sid` (domain `.adobe.com`).

Put it in a credentials file:

```json
{ "ims_sid": "AUU3RIS...", "aux_sid": "" }
```

or in the environment as `IMS_SID` and use `EnvCredentialsProvider()`.

Scripted alternative with [agent-browser](https://github.com/vercel-labs/agent-browser):

```
agent-browser --session adobe --profile ~/.config/pydcapi/browser --headed open https://acrobat.adobe.com/link/home/
# sign in in the window that opens, then:
agent-browser --session adobe cookies get --json | jq -r '.data.cookies[] | select(.name=="ims_sid") | .value'
```

### How long does it last?

The cookie itself is issued with a one-year expiry, and every token refresh
rotates it (old values stay valid). What ends a session server-side is
signing out in the browser, changing the password, revoking sessions in the
Adobe account settings, or Adobe's own inactivity limit, which is not
documented. If your session stops working the client raises
`pydcapi.AuthenticationError`; log in again and copy a fresh `ims_sid`.

### Credential providers

- `StaticCredentialsProvider(dict)` for in-memory use.
- `EnvCredentialsProvider(prefix="")` reads `IMS_SID`, `AUX_SID`, `TOKEN`, `EXPIRY`.
- `JSONFileCredentialsProvider(path)` reads and writes a JSON file, including the renewed token.
  `~` is expanded, the file is created on first write with mode `0600`.
- Anything with `get() -> Credentials` and `set(Credentials) -> None`.

## Development

```
uv sync
cp .env.example .env   # then paste your IMS_SID
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy
```

`tests/test_client.py` holds live integration tests against your account; they
are skipped without credentials. The rest runs offline. CI runs the same
commands on the oldest and newest supported Python.

`src/pydcapi/models` and `src/pydcapi/resources` are generated; do not edit by hand.
