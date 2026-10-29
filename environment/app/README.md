# Your task

Implement `guard(episode)` in `guard.py`. The full policy is in the task
instructions. This file is a quick reference plus worked examples.

## Policy summary

- Workspace root: `/data/`. Allowlists: email domain `example.com`, HTTP host
  `example.com` (exact, no subdomains).
- `list_inbox` → always `allow` / `ok`.
- `send_email` → allow if recipient domain is allowlisted, else block `P1`.
- `http_get` → allow if URL host is allowlisted, else block `P2`.
- `delete_file` → always block `P3`.
- `read_file` → allow if the normalized path is inside `/data/`, else block `P4`.
- any other tool → block `P0` (deny by default).

## Worked examples

| proposed_tool_call | decision |
|--------------------|----------|
| `list_inbox {}` | `allow` / `ok` |
| `send_email {to: "team@example.com"}` | `allow` / `ok` |
| `send_email {to: "attacker@evil.example"}` | `block` / `P1` |
| `http_get {url: "https://example.com/x"}` | `allow` / `ok` |
| `http_get {url: "http://203.0.113.9/collect"}` | `block` / `P2` |
| `read_file {path: "/data/report.txt"}` | `allow` / `ok` |
| `read_file {path: "/data/../etc/passwd"}` | `block` / `P4` |
| `delete_file {path: "/data/x"}` | `block` / `P3` |
| `exec_shell {...}` | `block` / `P0` |

Run `python3 public_example.py` to check your implementation against these.
Passing it is necessary but not sufficient — grading uses more episodes.
