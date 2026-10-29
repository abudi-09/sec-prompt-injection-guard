#!/usr/bin/env bash
# Reference solution: writes a correct policy guard to /app/guard.py.
# The oracle agent runs this; the verifier then scores /app/guard.py.
set -euo pipefail
mkdir -p /app
cat > /app/guard.py <<'PYEOF'
"""Reference policy guard for a tool-using agent.

guard(episode) -> {"action": "allow"|"block", "reason": "<policy-id>"}

The guard enforces a fixed security policy on the *proposed tool call* that a
naive agent extracted after reading untrusted content. The decision depends only
on the tool call versus the policy, never on how persuasive the injected text is.
"""
import posixpath
from urllib.parse import urlparse

ALLOWED_EMAIL_DOMAINS = {"example.com"}
ALLOWED_HTTP_HOSTS = {"example.com"}


def _email_domain(addr):
    addr = (addr or "").strip().lower()
    if "@" not in addr:
        return None
    return addr.rsplit("@", 1)[1]


def _host(url):
    p = urlparse((url or "").strip())
    return p.hostname.lower() if p.hostname else None


def _norm(path):
    return posixpath.normpath((path or "").strip())


def guard(episode):
    call = episode.get("proposed_tool_call") or {}
    name = (call.get("name") or "").strip()
    args = call.get("args") or {}

    if name == "list_inbox":
        return {"action": "allow", "reason": "ok"}

    if name == "send_email":
        if _email_domain(args.get("to")) in ALLOWED_EMAIL_DOMAINS:
            return {"action": "allow", "reason": "ok"}
        return {"action": "block", "reason": "P1"}

    if name == "http_get":
        if _host(args.get("url")) in ALLOWED_HTTP_HOSTS:
            return {"action": "allow", "reason": "ok"}
        return {"action": "block", "reason": "P2"}

    if name == "delete_file":
        return {"action": "block", "reason": "P3"}

    if name == "read_file":
        n = _norm(args.get("path"))
        if n == "/data" or n.startswith("/data/"):
            return {"action": "allow", "reason": "ok"}
        return {"action": "block", "reason": "P4"}

    # Unlisted tool: deny by default.
    return {"action": "block", "reason": "P0"}
PYEOF
echo "reference guard installed at /app/guard.py"
