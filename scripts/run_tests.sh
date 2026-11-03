#!/usr/bin/env bash
# RNF-06 / US-11: executar todas as suites e gerar relatório global.
# Os resultados de cada suite são preservados mesmo quando outra falha.
set -u
mkdir -p reports/{unit,integration,bdd}
failed=0
for suite in unit integration bdd; do
  # Remover relatórios antigos: evita apresentar resultados desatualizados.
  rm -f "reports/$suite/results.xml" "reports/$suite/results.html"
  python -m pytest "tests/$suite" --junitxml="reports/$suite/results.xml" || failed=1
  if [ -f "reports/$suite/results.xml" ]; then
    python scripts/report_from_junit.py "reports/$suite/results.xml" "reports/$suite/results.html" || failed=1
  else
    failed=1
  fi
done
# Mesmo que uma suite falhe, o relatório global é sempre tentado.
python scripts/report_from_junit.py --global reports reports/index.html || failed=1
echo "Relatório global: reports/index.html"
exit "$failed"
