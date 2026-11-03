"""RNF-06 / US-11: converter JUnit XML em relatório HTML autónomo.

Mantém evidência de testes aprovados, falhados, ignorados e com erros.
"""
import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

source, target = map(Path, sys.argv[1:3])
root = ET.parse(source).getroot()
tests = root.findall('.//testcase')
rows = []
for test in tests:
    status = 'FAILED' if test.find('failure') is not None else ('ERROR' if test.find('error') is not None else ('SKIPPED' if test.find('skipped') is not None else 'PASSED'))
    details = test.find('failure') or test.find('error') or test.find('skipped')
    message = '' if details is None else (details.get('message') or details.text or '')
    rows.append(f'<tr><td>{html.escape(test.get("classname", ""))}</td><td>{html.escape(test.get("name", ""))}</td><td>{status}</td><td><pre>{html.escape(message)}</pre></td></tr>')
summary = {'PASSED': 0, 'FAILED': 0, 'ERROR': 0, 'SKIPPED': 0}
for test in tests:
    status = ('FAILED' if test.find('failure') is not None else
              'ERROR' if test.find('error') is not None else
              'SKIPPED' if test.find('skipped') is not None else 'PASSED')
    summary[status] += 1

target.parent.mkdir(parents=True, exist_ok=True)
target.write_text('<!doctype html><html lang="pt"><meta charset="utf-8"><title>SmartTasks — Relatório</title><style>body{font:16px system-ui;margin:2rem}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:.5rem;text-align:left}pre{white-space:pre-wrap}</style><h1>SmartTasks — Relatório de testes</h1><p>'+html.escape(str(summary))+'</p><table><tr><th>Classe</th><th>Teste</th><th>Resultado</th><th>Detalhes</th></tr>'+''.join(rows)+'</table></html>',encoding='utf-8')
print(f'HTML gerado: {target}')
