#!/usr/bin/env bash
# RNF-06 / US-11: executar todas as suites e gerar relatório global.
# Os resultados de cada suite são preservados mesmo quando outra falha.
set -u
# Garantir que o script funciona mesmo invocado fora da pasta do projeto.
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
# Detetar uma cópia incompleta antes de executar qualquer teste.
for required in requirements.txt app/main.py app/store.py tests/conftest.py tests/bdd/test_steps.py; do
  if [ ! -f "$required" ]; then
    echo "ERRO: falta o ficheiro $required. Atualiza o repositório com git pull origin main." >&2
    exit 2
  fi
done
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
