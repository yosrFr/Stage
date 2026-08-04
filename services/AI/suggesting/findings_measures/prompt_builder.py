def build_finding_suggestion_prompt(data: dict) -> str:
    return f"""You are an experienced IT/security compliance auditor.

Your task is to identify realistic audit findings (non-conformities, gaps, or observations) for the control described below, based on the gap between the control's expectations and its current implementation state.

CONTROL CONTEXT
- Norm family: {data.get("norm_family")}
- Control title: {data.get("control_title")}
- Control description: {data.get("control_description")}
- Risk level: {data.get("risk_level")}
- Maturity level: {data.get("maturity_level")}
- Current state (as observed by the auditor): {data.get("current_state")}

INSTRUCTIONS
- Propose distinct realistic findings that an auditor could raise for this control, given the current state described.
- Each finding must be specific to the current_state provided. Do not invent unrelated facts.
- Each finding must be written as a complete, professional audit statement (what is missing, weak, or non-compliant, and why it matters).
- Do not propose remediation measures here, findings only.
- Do not repeat the control description verbatim.
- If the current_state already fully satisfies the control at the expected maturity level, return an empty list.

OUTPUT FORMAT
Return ONLY a valid JSON array of strings, with no markdown, no preamble, no explanation. Example:
["Finding text 1", "Finding text 2"]
"""


def build_measure_suggestion_prompt(data: dict) -> str:
    return f"""You are an experienced IT/security compliance auditor and remediation advisor.

Your task is to propose concrete remediation measures to address the audit finding below.

CONTROL CONTEXT
- Norm family: {data.get("norm_family")}
- Control title: {data.get("control_title")}
- Control description: {data.get("control_description")}
- Risk level: {data.get("risk_level")}
- Maturity level: {data.get("maturity_level")}
- Current state: {data.get("current_state")}

AUDIT FINDING TO ADDRESS
{data.get("finding")}

INSTRUCTIONS
- Propose concrete, actionable remediation measure that directly resolve this specific finding.
- The measure should be realistic to implement, proportionate to the risk level, and aligned with reaching or exceeding the target maturity level.
- Be specific (mention what should be done, not vague generalities like "improve security").
- Do not restate the finding itself.
- One paragraph, length proportional to the finding.

OUTPUT FORMAT
Return ONLY a the measure text.
"""