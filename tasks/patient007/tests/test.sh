#!/bin/bash

# Runs in the separate verifier container. /app/report is restored from the agent container
# (task.toml `artifacts`). Reward is currently 1 iff the report is a valid, complete form;
# scoring against the expert answers in /tests/expert_answers is still to be defined.
if pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
