"""Relatórios pedagógicos SmartTasks: HTML individual e global (RNF-06, US-11).

Lê os JUnit XML gerados pelo pytest, associa testes aos requisitos e
apresenta resultados com cores, detalhes de falhas e cobertura observada.
Não confunde testes não executados com testes aprovados.
"""
from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# Metadados explícitos: título compreensível, requisitos, história e objetivo.
# Os testes parametrizados herdam os metadados da função principal.
CATALOG = {
    "test_empty_and_creation": ("Criação e listagem de tarefas", "RF-01, RF-02, RF-06", "US-01, US-02", "Validar lista vazia, criação com/sem descrição, IDs únicos e estado inicial."),
    "test_invalid_title": ("Rejeição de títulos inválidos", "RF-03", "US-02", "Rejeitar títulos vazios ou só com espaços, sem criar tarefas."),
    "test_transitions": ("Concluir e reabrir tarefas", "RF-04, RF-05, RF-07", "US-03, US-04", "Validar mudanças de estado, ações repetidas e ID inexistente."),
    "test_store_isolation": ("Isolamento do armazenamento", "RT-07", "US-12", "Confirmar que instâncias diferentes não partilham tarefas."),
    "test_health_and_empty_list": ("Saúde e lista inicial", "RF-01, RF-08", "US-01, US-10", "Validar GET /health e lista inicialmente vazia."),
    "test_create_and_list": ("Criação através da API", "RF-01, RF-02, RF-07", "US-02", "Validar POST com 201 e consulta da tarefa criada."),
    "test_validation": ("Validação HTTP de entradas", "RF-03, RF-07", "US-02", "Rejeitar títulos inválidos com HTTP 422."),
    "test_complete_reopen_and_errors": ("Estados e erros HTTP", "RF-04, RF-05, RF-07", "US-03, US-04, US-08", "Validar concluir/reabrir e respostas HTTP 404/409."),
    "test_html": ("Interface HTML inicial", "RNF-01, RNF-02", "US-01, US-02", "Verificar a entrega da página e dos elementos essenciais; não executa JS."),
}
# Cenários BDD: os nomes apresentados são identificados diretamente pelo
# nome do cenário no XML. Mantêm a rastreabilidade dos ficheiros .feature.
BDD = {
    "Lista vazia": ("BDD-01", "RF-01, RF-06", "US-01", "Consultar lista sem tarefas."),
    "Criar tarefa": ("BDD-02", "RF-02, RF-03", "US-02", "Criar tarefa com título válido."),
    "Rejeitar título vazio": ("BDD-02", "RF-03", "US-02", "Impedir criação com título inválido."),
    "Concluir tarefa": ("BDD-03", "RF-04", "US-03", "Concluir tarefa pendente."),
    "Reabrir tarefa": ("BDD-04", "RF-05", "US-04", "Reabrir tarefa concluída."),
    "Consultar lista partilhada": ("BDD-05", "RF-01", "US-05", "Consultar tarefas existentes."),
    "Distinguir estados": ("BDD-06", "RF-06", "US-06", "Distinguir Pendente e Concluída."),
    "Consultar título e descrição": ("BDD-07", "RF-01, RF-02", "US-07", "Ler título e descrição."),
    "Consultar estado atualizado": ("BDD-08", "RF-04, RF-05, RNF-03", "US-08", "Consultar estado após uma alteração."),
    "Validar execução Docker": ("BDD-09", "RT-04, RT-05, RT-06", "US-09", "Verificar configuração Compose; não prova arranque."),
    "Verificar saúde": ("BDD-10", "RF-08", "US-10", "Verificar HTTP 200 em /health."),
    "Validar relatórios de testes": ("BDD-11", "RNF-06", "US-11", "Confirmar relatórios das outras suites."),
    "Verificar modularidade": ("BDD-12", "RNF-05", "US-12", "Confirmar separação dos módulos."),
}
COLORS = {"PASSED": "#087f4f", "FAILED": "#b42318", "ERROR": "#b42318", "SKIPPED": "#9a6700", "NOT RUN": "#65758b"}
LABELS = {"PASSED": "Aprovado", "FAILED": "Falhou", "ERROR": "Erro", "SKIPPED": "Ignorado", "NOT RUN": "Não executado"}
CSS = """
body{font:15px system-ui,sans-serif;background:#f6f8fb;color:#1c2738;max-width:1200px;margin:2rem auto;padding:0 1rem}
h1{margin-bottom:.25rem}a{color:#1455a1}.muted{color:#576578}.cards{display:flex;flex-wrap:wrap;gap:.75rem;margin:1.5rem 0}
.card{background:white;border:1px solid #dce2ea;border-radius:10px;padding:1rem;min-width:135px}
.card strong{display:block;font-size:1.65rem}.card small{color:#59677b}
table{width:100%;border-collapse:collapse;background:white;font-size:.92rem}
th,td{border:1px solid #e1e6ee;padding:.7rem;text-align:left;vertical-align:top}
th{background:#eaf0f7}tr:nth-child(even){background:#fafbfd}
.status{font-weight:700;border-radius:6px;padding:.25rem .5rem;white-space:nowrap}
pre{white-space:pre-wrap;overflow-wrap:anywhere;max-width:450px}
details{max-width:470px}summary{cursor:pointer}.note{background:#fff8e8;padding:.9rem;border-left:4px solid #9a6700}
"""


def read_suite(path: Path, suite: str):
    """Converter um JUnit XML em registos com estado e rastreabilidade."""
    if not path.exists():
        return [{"suite": suite, "name": "Suite não executada", "status": "NOT RUN",
                 "title": "Sem relatório XML", "requirements": "—", "stories": "—",
                 "objective": "A suite não produziu resultados.", "detail": str(path)}]
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [{"suite": suite, "name": "Relatório inválido", "status": "ERROR",
                 "title": "Falha na leitura do XML", "requirements": "—", "stories": "—",
                 "objective": "Não foi possível interpretar os resultados.", "detail": str(exc)}]
    records = []
    for case in root.findall(".//testcase"):
        name = case.get("name", "")
        base = name.split("[")[0]
        meta = CATALOG.get(base)
        if meta:
            title, req, stories, objective = meta
        else:
            found = next(((key, value) for key, value in BDD.items() if key.lower() in name.lower()), None)
            if found:
                key, (bdd_id, req, stories, objective) = found
                title = f"{bdd_id} — {key}"
            else:
                title, req, stories, objective = name, "Não mapeado", "Não mapeada", "Consultar teste de origem."
        error = next((case.find(k) for k in ("failure", "error", "skipped") if case.find(k) is not None), None)
        status = "FAILED" if case.find("failure") is not None else ("ERROR" if case.find("error") is not None else ("SKIPPED" if case.find("skipped") is not None else "PASSED"))
        detail = "" if error is None else (error.get("message", "") + "\n" + (error.text or "")).strip()
        records.append({"suite": suite, "name": name, "status": status, "title": title,
                        "requirements": req, "stories": stories, "objective": objective, "detail": detail})
    if not records:
        records.append({"suite": suite, "name": "Sem casos", "status": "NOT RUN", "title": "Sem testes registados",
                        "requirements": "—", "stories": "—", "objective": "O XML não contém testes.", "detail": ""})
    return records


def render(records, title, global_report=False):
    counts = {status: sum(item["status"] == status for item in records) for status in COLORS}
    cards = "".join(f'<div class="card"><strong style="color:{COLORS[s]}">{counts[s]}</strong><small>{LABELS[s]}</small></div>' for s in COLORS)
    rows = []
    for record in records:
        status = record["status"]
        details = f'<details><summary>Ver detalhes</summary><pre>{escape(record["detail"])}</pre></details>' if record["detail"] else "—"
        rows.append("<tr>" + "".join((
            f'<td>{escape(record["suite"])}</td>',
            f'<td><strong>{escape(record["title"])}</strong><br><small>{escape(record["name"])}</small></td>',
            f'<td>{escape(record["objective"])}</td>',
            f'<td>{escape(record["requirements"])}</td>',
            f'<td>{escape(record["stories"])}</td>',
            f'<td><span class="status" style="color:{COLORS[status]};background:{COLORS[status]}16">{LABELS[status]}</span></td>',
            f'<td>{details}</td>')) + "</tr>")
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    navigation = '<p><a href="unit/results.html">Unitários</a> · <a href="integration/results.html">Integração</a> · <a href="bdd/results.html">BDD</a></p>' if global_report else '<p><a href="../index.html">Voltar ao relatório global</a></p>'
    warning = '<p class="note">Um teste ignorado ou não executado não equivale a aprovação. O relatório documenta a execução de pytest, não a validação real do browser ou do arranque Docker.</p>'
    return ('<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><style>{CSS}</style></head><body><h1>{escape(title)}</h1>'
            f'<p class="muted">Gerado em {when} · SmartTasks · RF/RNF/RT → US → teste</p>{navigation}{warning}'
            f'<div class="cards">{cards}</div><table><thead><tr><th>Suite</th><th>Teste</th><th>Objetivo</th><th>Requisitos</th><th>User Stories</th><th>Resultado</th><th>Diagnóstico</th></tr></thead><tbody>{"".join(rows)}</tbody></table></body></html>')


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--global":
        folder, output = Path(sys.argv[2]), Path(sys.argv[3])
        records = []
        for suite in ("unit", "integration", "bdd"):
            records.extend(read_suite(folder / suite / "results.xml", suite))
        document = render(records, "SmartTasks — Relatório global de testes", True)
    elif len(sys.argv) == 3:
        source, output = Path(sys.argv[1]), Path(sys.argv[2])
        document = render(read_suite(source, source.parent.name), "SmartTasks — Testes " + source.parent.name)
    else:
        raise SystemExit("Uso: report_from_junit.py XML HTML | --global PASTA HTML")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print("Relatório gerado:", output)


if __name__ == "__main__":
    main()
