"""Risk analysis helpers."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


VALID_STATUSES = {"open", "mitigating", "watch", "closed"}
REQUIRED_FIELDS = {
    "id",
    "title",
    "owner",
    "review_gate",
    "status",
    "severity",
    "likelihood",
    "detection",
    "residual_likelihood",
    "residual_detection",
    "workstream_refs",
    "mitigation_actions",
}


@dataclass
class RiskAnalysisResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    risk_rows: List[Dict[str, str]]
    gate_rows: List[Dict[str, str]]


def analyze_risks(risks: Sequence[Mapping[str, Any]]) -> RiskAnalysisResult:
    """Validate and summarize risk data."""
    errors: List[str] = []
    warnings: List[str] = []
    _check_duplicate_ids(risks, errors)

    risk_rows: List[Dict[str, str]] = []
    gate_rollup: Dict[str, List[int]] = defaultdict(list)

    for risk in risks:
        if not _validate_risk(risk, errors, warnings):
            continue
        initial_rpn = _calculate_rpn(risk["severity"], risk["likelihood"], risk["detection"])
        residual_rpn = _calculate_rpn(
            risk["severity"],
            risk["residual_likelihood"],
            risk["residual_detection"],
        )
        risk_rows.append(
            {
                "id": risk["id"],
                "title": risk["title"],
                "owner": risk["owner"],
                "review_gate": risk["review_gate"],
                "status": risk["status"],
                "initial_rpn": str(initial_rpn),
                "residual_rpn": str(residual_rpn),
                "workstream_refs": "; ".join(risk["workstream_refs"]),
                "mitigation_count": str(len(risk["mitigation_actions"])),
            }
        )
        gate_rollup[risk["review_gate"]].append(residual_rpn)
        if residual_rpn >= 160:
            warnings.append(f"{risk['id']}: residual RPN remains review-board critical ({residual_rpn}).")

    gate_rows = []
    for gate, scores in sorted(gate_rollup.items()):
        gate_rows.append(
            {
                "review_gate": gate,
                "risk_count": str(len(scores)),
                "max_residual_rpn": str(max(scores)),
                "average_residual_rpn": f"{sum(scores) / len(scores):.1f}",
            }
        )

    residual_scores = [int(row["residual_rpn"]) for row in risk_rows]
    summary = {
        "risk_count": len(risk_rows),
        "open_count": sum(1 for row in risk_rows if row["status"] == "open"),
        "critical_count": sum(1 for score in residual_scores if score >= 160),
        "review_gate_count": len(gate_rows),
        "linked_repo_count": len({ref for risk in risks for ref in risk.get("workstream_refs", [])}),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    return RiskAnalysisResult(errors, warnings, summary, risk_rows, gate_rows)


def _check_duplicate_ids(risks: Sequence[Mapping[str, Any]], errors: List[str]) -> None:
    seen = set()
    for risk in risks:
        risk_id = risk.get("id")
        if risk_id in seen:
            errors.append(f"duplicate risk id '{risk_id}' detected.")
        seen.add(risk_id)


def _validate_risk(risk: Mapping[str, Any], errors: List[str], warnings: List[str]) -> bool:
    risk_id = str(risk.get("id", "<missing-id>"))
    missing = sorted(field for field in REQUIRED_FIELDS if not risk.get(field))
    if missing:
        errors.append(f"{risk_id}: missing required fields: {', '.join(missing)}.")
        return False
    if risk["status"] not in VALID_STATUSES:
        errors.append(f"{risk_id}: invalid status '{risk['status']}'.")
    for field in ("severity", "likelihood", "detection", "residual_likelihood", "residual_detection"):
        value = risk[field]
        if not isinstance(value, int) or value < 1 or value > 10:
            errors.append(f"{risk_id}: {field} must be an integer between 1 and 10.")
    if not isinstance(risk["workstream_refs"], list) or not risk["workstream_refs"]:
        errors.append(f"{risk_id}: workstream_refs must contain at least one repository reference.")
    if len(risk["mitigation_actions"]) < 2:
        warnings.append(f"{risk_id}: fewer than two mitigation actions are recorded.")
    return True


def _calculate_rpn(severity: int, likelihood: int, detection: int) -> int:
    return severity * likelihood * detection
