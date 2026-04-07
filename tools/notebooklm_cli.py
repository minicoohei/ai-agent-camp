#!/usr/bin/env python3
"""NotebookLM Enterprise API CLI."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env

load_runtime_env()



DEFAULT_ENDPOINT_LOCATION = "global-"
DEFAULT_LOCATION = "global"


def normalize_endpoint_location(value: str) -> str:
    if not value:
        return value
    return value if value.endswith("-") else f"{value}-"


def resolve_param(
    arg_value: Optional[str],
    env_name: str,
    *,
    default: Optional[str] = None,
    required: bool = False,
    label: str,
) -> str:
    value = arg_value or os.getenv(env_name) or default
    if required and not value:
        flag = label.replace("_", "-")
        raise SystemExit(
            f"Missing required {label}. Use --{flag} or set {env_name}."
        )
    return value


def resolve_access_token(cli_token: Optional[str]) -> str:
    if cli_token:
        return cli_token

    env_token = os.getenv("NOTEBOOKLM_ACCESS_TOKEN")
    if env_token:
        return env_token

    try:
        result = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit(
            "gcloud not found. Install it or set NOTEBOOKLM_ACCESS_TOKEN."
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise SystemExit(
            f"Failed to get access token via gcloud. {detail}".strip()
        ) from exc

    token = result.stdout.strip()
    if not token:
        raise SystemExit(
            "Empty access token from gcloud. Re-authenticate or set "
            "NOTEBOOKLM_ACCESS_TOKEN."
        )
    return token


def build_base_url(
    endpoint_location: str, project_number: str, location: str
) -> str:
    endpoint_location = normalize_endpoint_location(endpoint_location)
    return (
        f"https://{endpoint_location}"
        "discoveryengine.googleapis.com/v1alpha/"
        f"projects/{project_number}/locations/{location}"
    )


def make_headers(access_token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def print_response(response: requests.Response, *, raw: bool) -> None:
    content_type = response.headers.get("content-type", "")
    body_text = response.text or ""

    output = body_text
    if not raw and "application/json" in content_type:
        try:
            output = json.dumps(
                response.json(), indent=2, ensure_ascii=False
            )
        except json.JSONDecodeError:
            output = body_text

    if response.ok:
        print(output)
        return

    sys.stderr.write(f"HTTP {response.status_code} error\n")
    if output:
        sys.stderr.write(output + "\n")
    raise SystemExit(1)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-number", dest="project_number")
    parser.add_argument("--location")
    parser.add_argument("--endpoint-location", dest="endpoint_location")
    parser.add_argument("--access-token", dest="access_token")
    parser.add_argument("--raw", action="store_true")


def handle_create(args: argparse.Namespace) -> None:
    project_number = resolve_param(
        args.project_number,
        "NOTEBOOKLM_PROJECT_NUMBER",
        required=True,
        label="project_number",
    )
    location = resolve_param(
        args.location,
        "NOTEBOOKLM_LOCATION",
        default=DEFAULT_LOCATION,
        label="location",
    )
    endpoint_location = resolve_param(
        args.endpoint_location,
        "NOTEBOOKLM_ENDPOINT_LOCATION",
        default=DEFAULT_ENDPOINT_LOCATION,
        label="endpoint_location",
    )
    access_token = resolve_access_token(args.access_token)

    url = f"{build_base_url(endpoint_location, project_number, location)}/notebooks"
    payload = {"title": args.title}
    response = requests.post(
        url,
        headers=make_headers(access_token),
        json=payload,
        timeout=30,
    )
    print_response(response, raw=args.raw)


def handle_get(args: argparse.Namespace) -> None:
    project_number = resolve_param(
        args.project_number,
        "NOTEBOOKLM_PROJECT_NUMBER",
        required=True,
        label="project_number",
    )
    location = resolve_param(
        args.location,
        "NOTEBOOKLM_LOCATION",
        default=DEFAULT_LOCATION,
        label="location",
    )
    endpoint_location = resolve_param(
        args.endpoint_location,
        "NOTEBOOKLM_ENDPOINT_LOCATION",
        default=DEFAULT_ENDPOINT_LOCATION,
        label="endpoint_location",
    )
    access_token = resolve_access_token(args.access_token)

    url = (
        f"{build_base_url(endpoint_location, project_number, location)}"
        f"/notebooks/{args.notebook_id}"
    )
    response = requests.get(
        url,
        headers=make_headers(access_token),
        timeout=30,
    )
    print_response(response, raw=args.raw)


def handle_list_recent(args: argparse.Namespace) -> None:
    project_number = resolve_param(
        args.project_number,
        "NOTEBOOKLM_PROJECT_NUMBER",
        required=True,
        label="project_number",
    )
    location = resolve_param(
        args.location,
        "NOTEBOOKLM_LOCATION",
        default=DEFAULT_LOCATION,
        label="location",
    )
    endpoint_location = resolve_param(
        args.endpoint_location,
        "NOTEBOOKLM_ENDPOINT_LOCATION",
        default=DEFAULT_ENDPOINT_LOCATION,
        label="endpoint_location",
    )
    access_token = resolve_access_token(args.access_token)

    url = (
        f"{build_base_url(endpoint_location, project_number, location)}"
        "/notebooks:listRecentlyViewed"
    )
    params: Dict[str, Any] = {}
    if args.page_size is not None:
        params["pageSize"] = args.page_size
    response = requests.get(
        url,
        headers=make_headers(access_token),
        params=params or None,
        timeout=30,
    )
    print_response(response, raw=args.raw)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NotebookLM Enterprise API CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create notebook")
    add_common_args(create_parser)
    create_parser.add_argument("--title", required=True)
    create_parser.set_defaults(func=handle_create)

    get_parser = subparsers.add_parser("get", help="Get notebook")
    add_common_args(get_parser)
    get_parser.add_argument("--notebook-id", required=True)
    get_parser.set_defaults(func=handle_get)

    list_parser = subparsers.add_parser(
        "list-recent", help="List recently viewed notebooks"
    )
    add_common_args(list_parser)
    list_parser.add_argument("--page-size", type=int, dest="page_size")
    list_parser.set_defaults(func=handle_list_recent)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
