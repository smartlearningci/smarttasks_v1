#!/usr/bin/env bash
# RNF-06 / US-11: executar testes e guardar evidências XML e HTML.
# Uma falha não impede a geração dos relatórios das outras suites.
set -u
mkdir -p reports/{unit,bdd,integration}
failed=0
for suite in unit integration bdd; do
  # JUnit XML permite integração futura com CI/CD.
  python -m pytest "tests/$suite" --junitxml="reports/$suite/results.xml" || failed=1
  if [ -f "reports/$suite/results.xml" ]; then
    # Transformar os resultados em relatório legível para os formandos.
    python scripts/report_from_junit.py "reports/$suite/results.xml" "reports/$suite/results.html"
  fi
done
exit "$failed"
