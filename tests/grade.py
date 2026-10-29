"""Grader. Imports the agent's /app/guard.py, runs it on held-out episodes, and
writes a scalar reward (fraction decided correctly) to /logs/verifier/reward.txt.
A point requires both action and reason to match.
"""
import json
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = "/app"
REWARD_DIR = "/logs/verifier"
REWARD_FILE = os.path.join(REWARD_DIR, "reward.txt")

sys.path.insert(0, APP_DIR)


def _norm(x):
    return str(x).strip().lower()


def _write(score):
    os.makedirs(REWARD_DIR, exist_ok=True)
    with open(REWARD_FILE, "w") as f:
        f.write("%.6f\n" % score)
    print("%.6f" % score)


def main():
    with open(os.path.join(TESTS_DIR, "episodes.json")) as f:
        episodes = {e["id"]: e for e in json.load(f)}
    with open(os.path.join(TESTS_DIR, "ground_truth.json")) as f:
        truth = json.load(f)

    try:
        import guard as mod
    except Exception as e:
        sys.stderr.write("could not import /app/guard.py: %r\n" % e)
        _write(0.0)
        return

    total = correct = 0
    for eid, expected in truth.items():
        total += 1
        try:
            got = mod.guard(episodes[eid])
            ok = (isinstance(got, dict)
                  and _norm(got.get("action")) == _norm(expected["action"])
                  and _norm(got.get("reason")) == _norm(expected["reason"]))
        except Exception as e:
            sys.stderr.write("  %s raised %r\n" % (eid, e))
            ok = False
        if ok:
            correct += 1
        else:
            sys.stderr.write("  %s wrong (expected %s)\n" % (eid, expected))

    score = (correct / total) if total else 0.0
    sys.stderr.write("%d/%d episodes correct\n" % (correct, total))
    _write(max(0.0, min(1.0, score)))


if __name__ == "__main__":
    main()
