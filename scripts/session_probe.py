"""Check whether a stored Adobe IMS session cookie still mints access tokens.

Usage:
    session_probe.py <credentials.json> [--refresh] [--log <file>]

Without --refresh the stored cookie is never replaced, which measures the raw
server-side lifetime of one cookie. With --refresh the rotated cookie returned
by IMS is written back, which measures whether regular use keeps a session alive.
Each run appends one line to the log: timestamp, mode, age of the stored cookie, result.
"""

import argparse
import datetime
import json
import sys

import httpx

TOKEN_URL = "https://adobeid-na1.services.adobe.com/ims/check/v6/token"
HEADERS = {
    "origin": "https://acrobat.adobe.com",
    "referer": "https://acrobat.adobe.com/",
    "x-api-app-info": "dc-web-app",
    "x-api-client-id": "api_browser",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--log", default=None)
    args = parser.parse_args()

    with open(args.path) as f:
        data = json.load(f)

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    captured = datetime.datetime.fromisoformat(data.get("captured_at", now.isoformat()))

    with httpx.Client(headers=HEADERS, cookies={"ims_sid": data["ims_sid"]}) as client:
        resp = client.post(TOKEN_URL, data={"client_id": "dc-prod-virgoweb", "scope": "AdobeID,openid,DCAPI"})
        body = resp.json()
        ok = resp.status_code == 200 and "access_token" in body
        rotated = resp.cookies.get("ims_sid")

    if ok and args.refresh and rotated:
        data["ims_sid"] = rotated
        data["refreshed_at"] = now.isoformat()
        with open(args.path, "w") as f:
            json.dump(data, f, indent=2)

    line = f"{now.isoformat()} mode={'refresh' if args.refresh else 'static'} age_days={(now - captured).days} ok={ok} error={body.get('error')}"
    print(line)
    if args.log:
        with open(args.log, "a") as f:
            f.write(line + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
