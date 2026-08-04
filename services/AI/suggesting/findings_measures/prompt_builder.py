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
- Propose one concrete, actionable remediation measure that directly resolves this finding.
- Base the measure ONLY on facts explicitly stated in the finding. Do not invent numbers, thresholds, named tools/technologies, or standards the finding doesn't mention.
- If the finding states a specific number, describe the needed change in words, without stating any number (not the original, not a new one).
- Match the finding's language exactly.
- Proportionate to risk level and target maturity level. One paragraph, length proportional to the finding.
- Do not restate the finding.

EXAMPLES:
    Finding: Security events from servers are not centrally collected or monitored.
    Measure: Implement centralized log collection and monitoring with appropriate alerting.

    Finding: A cloud storage bucket containing confidential engineering documents is publicly accessible without authentication.
    Measure: Restrict access using the principle of least privilege, remove public permissions, and review all cloud storage configurations.

    Finding: Third-party suppliers with access to sensitive information are not subject to documented security assessments before onboarding.
    Measure: Implement a supplier security assessment process that includes risk evaluation, contractual security requirements, and periodic reassessments.

    Finding: The current password policy allows passwords as short as six characters without complexity requirements.
    Wrong: Strengthen the password policy to require a minimum of eight characters with complexity requirements. (invents a number not in the finding)
    Correct: Strengthen the password policy to require greater length and complexity.

    Finding: Loss or theft of removable media could expose confidential customer information.
    Measure: Implement controls to prevent unauthorized loss or exposure of confidential data stored on removable media.

    Finding: Multiple workstations are running outdated antivirus software.
    Measure: Update antivirus software on all affected workstations to a supported and current version.

    Finding: Incident response procedures exist but have not been tested.
    Measure: Test and validate the incident response procedures to confirm their effectiveness.

    Finding: Data classification policy exists but is not consistently applied across departments.
    Measure: Enforce consistent application of the existing data classification policy across all departments.

    Finding: Backup retention is currently set to 15 days, which may not meet business requirements.
    Wrong: Increase backup retention to at least 30 days. (invents a number)
    Correct: Review and adjust the backup retention period to meet business requirements.

    Finding: Audit logs can be modified by system administrators without oversight.
    Measure: Restrict the ability to modify audit logs and ensure changes are subject to independent oversight.

OUTPUT FORMAT
Return ONLY a the measure text.
"""