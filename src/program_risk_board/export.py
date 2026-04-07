"""Export risk board outputs."""

from __future__ import annotations

from csv import DictWriter
from html import escape
from pathlib import Path
from typing import Iterable, Mapping

from .analysis import RiskAnalysisResult


def export_reports(result: RiskAnalysisResult, export_dir: Path | str) -> None:
    """Write report artifacts."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    _write_text(export_path / "risk-summary.md", _render_summary_markdown(result))
    _write_csv(export_path / "risk-register.csv", result.risk_rows)
    _write_csv(export_path / "risk-gate-matrix.csv", result.gate_rows)
    _write_text(export_path / "risk-dashboard.html", _render_dashboard_html(result))


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def _render_summary_markdown(result: RiskAnalysisResult) -> str:
    summary = result.summary
    risks = "\n".join(
        f"- {row['id']} | {row['title']} | residual RPN {row['residual_rpn']}"
        for row in result.risk_rows
    ) or "- None"
    errors = "\n".join(f"- {message}" for message in result.errors) or "- None"
    warnings = "\n".join(f"- {message}" for message in result.warnings) or "- None"
    return (
        "# Program Risk Summary\n\n"
        f"- Risks: {summary['risk_count']}\n"
        f"- Open risks: {summary['open_count']}\n"
        f"- Critical residual risks: {summary['critical_count']}\n"
        f"- Review gates: {summary['review_gate_count']}\n"
        f"- Linked repositories: {summary['linked_repo_count']}\n"
        f"- Errors: {summary['error_count']}\n"
        f"- Warnings: {summary['warning_count']}\n\n"
        "## Ranked Risks\n\n"
        f"{risks}\n\n"
        "## Errors\n\n"
        f"{errors}\n\n"
        "## Warnings\n\n"
        f"{warnings}\n"
    )


def _render_dashboard_html(result: RiskAnalysisResult) -> str:
    summary = result.summary
    cards = [
        ("Risks", str(summary["risk_count"])),
        ("Open", str(summary["open_count"])),
        ("Critical Residual", str(summary["critical_count"])),
        ("Review Gates", str(summary["review_gate_count"])),
    ]
    card_html = "\n".join(
        f"<article class=\"card\"><span>{escape(label)}</span><strong>{escape(value)}</strong></article>"
        for label, value in cards
    )
    risk_table = _render_table(
        result.risk_rows,
        ["id", "title", "owner", "review_gate", "status", "residual_rpn"],
        "No risks available.",
    )
    gate_table = _render_table(
        result.gate_rows,
        ["review_gate", "risk_count", "max_residual_rpn", "average_residual_rpn"],
        "No gate rollup available.",
    )
    warning_items = "".join(f"<li>{escape(item)}</li>" for item in (result.warnings or ["None"]))
    error_items = "".join(f"<li>{escape(item)}</li>" for item in (result.errors or ["None"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Program Risk Board</title>
  <style>
    :root {{
      --bg: #f4efe8;
      --panel: rgba(255,255,255,0.9);
      --ink: #2e241f;
      --muted: #73645b;
      --accent: #b45309;
      --line: rgba(46,36,31,0.12);
      --shadow: 0 18px 40px rgba(65, 46, 24, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at top left, #f7f2eb, #ece3d7 48%, #e6d8c7 100%);
    }}
    main {{
      width: min(1100px, calc(100% - 28px));
      margin: 0 auto;
      padding: 28px 0 54px;
    }}
    .hero, section, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      border-radius: 24px;
    }}
    .hero {{
      padding: 28px;
      background: linear-gradient(135deg, rgba(180,83,9,0.95), rgba(146,64,14,0.95));
      color: #fffdf8;
    }}
    h1, h2 {{
      margin: 0 0 12px;
      font-family: "Georgia", serif;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 18px 0;
    }}
    .card {{
      padding: 20px;
      min-height: 116px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card span {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.84rem;
      letter-spacing: 0.07em;
    }}
    .card strong {{
      color: var(--accent);
      font-size: 1.9rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
    }}
    section {{
      padding: 22px;
      overflow: hidden;
    }}
    .wide {{
      grid-column: 1 / -1;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.8rem;
      letter-spacing: 0.06em;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
    @media (max-width: 860px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>Program Risk Board</h1>
      <p>Program-level risk review workspace for a systems engineering portfolio. The board highlights residual exposure across workstreams and review gates.</p>
    </section>
    <div class="metrics">{card_html}</div>
    <div class="grid">
      <section class="wide">
        <h2>Risk Register</h2>
        {risk_table}
      </section>
      <section>
        <h2>Review Gate Rollup</h2>
        {gate_table}
      </section>
      <section>
        <h2>Warnings</h2>
        <ul>{warning_items}</ul>
      </section>
      <section class="wide">
        <h2>Errors</h2>
        <ul>{error_items}</ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def _render_table(rows: Iterable[Mapping[str, str]], columns: list[str], empty_message: str) -> str:
    row_list = list(rows)
    if not row_list:
        return f"<p>{escape(empty_message)}</p>"
    header_html = "".join(f"<th>{escape(column.replace('_', ' '))}</th>" for column in columns)
    body_html = []
    for row in row_list:
        body_html.append(
            "<tr>" + "".join(f"<td>{escape(str(row.get(column, '')))}</td>" for column in columns) + "</tr>"
        )
    return f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"
