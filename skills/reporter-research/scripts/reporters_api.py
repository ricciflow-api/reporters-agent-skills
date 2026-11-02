"""One bounded Reporters.io request per command; explicit contact reveal only."""
import argparse
import json
from reporters_client import request


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ["search-reporters", "search-outlets"]:
        command = commands.add_parser(name)
        command.add_argument("--query", required=True)
        command.add_argument("--limit", type=int, default=10, choices=range(1, 101))
        command.add_argument("--region")
        command.add_argument("--country")
        command.add_argument("--cursor")
        if name == "search-reporters":
            command.add_argument("--state")
            command.add_argument("--beat", action="append", dest="beats")
    for name in ["reporter", "reporter-articles", "outlet", "outlet-reporters", "outlet-articles", "reveal-reporter", "reveal-outlet"]:
        command = commands.add_parser(name)
        command.add_argument("--id", required=True)
        if name.startswith("reveal-"):
            command.add_argument("--confirm-contact-reveal", action="store_true", required=True)
            command.add_argument("--idempotency-key", required=True)
        elif name.endswith("articles") or name == "outlet-reporters":
            command.add_argument("--cursor")
    commands.add_parser("account")
    commands.add_parser("filters")
    args = parser.parse_args(argv)
    if args.command.startswith("search-"):
        body = {name: getattr(args, name, None) for name in ["query", "limit", "region", "country", "cursor", "state", "beats"]}
        body = {name: value for name, value in body.items() if value is not None}
        return request("/" + args.command.removeprefix("search-") + "/search", method="POST", body=body)
    if args.command in ("account", "filters"):
        return request("/account" if args.command == "account" else "/metadata/search-filters")
    if args.command.startswith("reveal-"):
        entity = "reporters" if args.command == "reveal-reporter" else "outlets"
        return request(f"/{entity}/{args.id}/contacts/reveal", method="POST", body={}, confirm_contact_reveal=args.confirm_contact_reveal, idempotency_key=args.idempotency_key)
    entity = "reporters" if args.command.startswith("reporter") else "outlets"
    suffix = "/articles" if args.command.endswith("articles") else "/reporters" if args.command == "outlet-reporters" else ""
    params = {"cursor": getattr(args, "cursor", None)}
    return request(f"/{entity}/{args.id}{suffix}", params={name: value for name, value in params.items() if value is not None})


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
