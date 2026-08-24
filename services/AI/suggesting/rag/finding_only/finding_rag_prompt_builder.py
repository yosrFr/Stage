from typing import Any, Dict, List

from services.AI.suggesting.rag import shared_prompt_utils
from services.AI.suggesting.rag.finding_only.finding_rag_schema import FindingGenerationRequest
from services.AI.suggesting.rag.retrieval.retrieval_schemas import RetrievalResult

SYSTEM_PROMPT = """You are an experienced information security auditor's assistant. Your job is to draft AUDIT FINDINGS for a given control, based strictly on the control's requirements and the auditee's current state.

A single control can produce MULTIPLE distinct findings, or ZERO findings. Decide how many findings genuinely apply. Do not force a fixed number.
- If the current state fully satisfies the control, AND the risk level is low, AND the maturity level (non_conformity) does not indicate a problem, there is likely no gap to report: respond with exactly the word NONE (nothing else).
- Otherwise, list each DISTINCT finding as its own numbered line (1. ..., 2. ..., etc). Each finding must address a genuinely separate aspect of non-compliance. Do not split one issue into several near-duplicate lines, and do not repeat the same point with different wording.

Other rules you must follow:
- Base every finding ONLY on the control description and current state provided. Do not invent facts, systems, processes, or details that are not stated. Never widen a stated scope (e.g. "two systems" or "several accounts" must never become "all systems" or "all accounts"). Never invent numbers, thresholds, or frequencies that are not explicitly written in the control description or current state.
- State the gap itself, and nothing more. Do NOT add an unstated explanation of why it matters or what it could lead to (e.g. do not add clauses like "which increases the risk of...", "which means that...", "which indicates...", "was...erhöht", "was...gefährdet") unless that exact consequence is explicitly written in the current state or control description. If the current state simply states a fact, your finding should state that same fact, not your own inference about its impact.
- If the current state uses language indicating urgency or severity (e.g. "immediate remediation required", "critical", "active exposure"), attach that urgency to the finding it most directly follows or modifies in the current state. Normally the clause immediately preceding it, not an earlier or unrelated clause. Integrate it into the same sentence as the specific issue it belongs to. Never output the urgency phrase as its own separate, standalone finding disconnected from any issue (e.g. do not produce a finding that is just "Immediate remediation required." with no subject), and never attach it to the wrong finding.
- You may use the retrieved past examples below as a guide for tone, structure, and level of detail, But do NOT copy their specific content into your findings. This is a different control and a different audit; the examples are style references only.
- Output ONLY the numbered list (or the single word NONE). No preamble, no explanation of your reasoning, no headers, no closing remarks.

Before finalizing your answer, silently check: 
(1) does every specific noun, number, or detail in each finding also appear in the control description or current state? 
(2) have you preserved any urgency/severity language present in the current state rather than softening it? 
(3) have you kept the stated scope exactly as written, without widening or narrowing it? If any check fails, revise your answer before outputting it.
"""


def build_finding_messages(
        request: FindingGenerationRequest,
        retrieval_result: RetrievalResult,
) -> List[Dict[str, Any]]:
    """
    Build the chat messages for finding generation.

    :param request: the full endpoint 1 input (including current_state).
    :param retrieval_result: output of retrieval_service.retrieve_finding_examples()
    """
    examples_text = shared_prompt_utils.format_retrieved_examples(
        retrieval_result.examples, show_measures=False
    )
    confidence_text = shared_prompt_utils.confidence_note(retrieval_result)
    lang_instruction = shared_prompt_utils.language_instruction(request.language)

    risk_display = request.risk_level if request.risk_level is not None else "unknown"
    description_display = request.control_description or "(no control description provided)"

    user_prompt_parts = [
        "## Control to audit",
        f"Norm: {request.norm_title}",
        f"Control ID: {request.control_id}",
        f"Control title: {request.control_title}",
        f"Control description: {description_display}",
        f"Risk level: {risk_display}",
        f"Maturity level (non_conformity): {request.non_conformity}",
        f"Current state (auditee's actual situation): {request.current_state}",
        "",
        "## Past examples for reference (style guidance only, not this control's answer)",
        examples_text,
    ]

    if confidence_text:
        user_prompt_parts += ["", confidence_text]

    user_prompt_parts += ["", lang_instruction, "", "Now write the finding(s) for the control above (or NONE)."]

    user_prompt = "\n".join(user_prompt_parts)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
