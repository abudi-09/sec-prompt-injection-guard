def guard(episode):
    """Decide whether a proposed tool call is allowed under the policy.

    Args:
        episode: dict with keys "context" (str), "untrusted_content" (str),
                 and "proposed_tool_call" ({"name": str, "args": dict}).

    Returns:
        {"action": "allow"|"block", "reason": "<policy-id>"} where reason is
        "ok" for allowed calls, or one of "P0".."P4" for blocked calls.

    See /app/README.md for the policy table and /app/public_example.py for
    runnable examples.
    """
    raise NotImplementedError("implement guard()")
