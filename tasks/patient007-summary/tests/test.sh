#!/bin/bash

# Runs in the separate verifier container. /app/output is restored from the agent container
# (task.toml `artifacts`). Reward is currently 1 iff summary.md exists and has a headline and an impression;
# grading the clinical content of the summary is still to be defined.
if pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
