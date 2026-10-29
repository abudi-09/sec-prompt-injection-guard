FROM python:3.11-slim

WORKDIR /app

# The agent sees only the stub, the contract, and a public self-check. The
# grader, held-out episodes, and expected decisions live in tests/ and are
# uploaded to /tests/ by Harbor only after the agent finishes.
COPY app/ /app/

CMD ["sleep", "infinity"]
