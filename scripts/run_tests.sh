#!/usr/bin/env bash
set -u
mkdir -p reports/{unit,bdd,integration}
failed=0
for suite in unit integration bdd; do
  python -m pytest "tests/$suite" --junitxml="reports/$suite/results.xml" || failed=1
  if [ -f "reports/$suite/results.xml" ]; then
    python scripts/report_from_junit.py "reports/$suite/results.xml" "reports/$suite/results.html"
  fi
done
exit "$failed"
