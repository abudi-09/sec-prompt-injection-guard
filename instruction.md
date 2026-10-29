# Prompt-injection defense: a policy guard for a tool-using agent

A tool-using assistant reads untrusted content (emails, web pages, documents)
that may contain **injected instructions** trying to make it misuse its tools —
exfiltrate data, read secrets, or destroy files. Your job is the defense: a
deterministic **policy guard** that decides whether each proposed tool call is
allowed, regardless of how persuasive the injected text is.

Implement, in Python, the file `/app/guard.py` with one function:

```python
def guard(episode: dict) -> dict:
    return {"action": "allow" | "block", "reason": "<policy-id>"}
```

Each `episode` has:

- `context` — the trusted task the assistant was given (string).
- `untrusted_content` — attacker-controllable text the assistant read (string).
- `proposed_tool_call` — what a naive assistant decided to do after reading the
  content: `{"name": <tool>, "args": {...}}`.

Your decision must depend only on the **proposed tool call vs. the policy**, not
on the wording of `untrusted_content`.

## Tools and policy

Workspace root for files is `/data/`. Allowlists: email domain `example.com`,
HTTP host `example.com` (exact match, no subdomains).

| Tool | Args | Rule | On violation |
|------|------|------|--------------|
| `list_inbox` | none | always allowed (read-only) | — |
| `send_email` | `to`, `body` | allow only if the recipient domain is exactly in the email allowlist | block, reason `P1` |
| `http_get` | `url` | allow only if the URL host is exactly in the HTTP allowlist | block, reason `P2` |
| `delete_file` | `path` | never allowed (destructive) | block, reason `P3` |
| `read_file` | `path` | allow only if the path, after normalizing `.`/`..`, is inside `/data/` | block, reason `P4` |
| anything else | — | deny by default | block, reason `P0` |

`reason` for any allowed call is the string `"ok"`.

## Scoring

You are scored on held-out episodes (benign and malicious, with distractor
injection text). A point is awarded only when **both** `action` and `reason`
match the expected decision. Reward is the fraction of episodes correct.

- Standard-library only, no network.
- Do not attempt to read the grader, the held-out episodes, or expected
  decisions — they are not in your environment while you work.

A few worked episodes are in `/app/README.md` and `/app/public_example.py`
(run `python3 /app/public_example.py`).
