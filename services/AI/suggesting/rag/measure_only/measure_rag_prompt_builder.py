from typing import Any, Dict, List

from services.AI.suggesting.rag import shared_prompt_utils
from services.AI.suggesting.rag.measure_only.measure_rag_schema import MeasureGenerationRequest
from services.AI.suggesting.rag.retrieval.retrieval_schemas import RetrievalResult

SYSTEM_PROMPT = """You are an experienced information security auditor's assistant. Your job is to propose remediation MEASURES for a given audit finding.

Rules you must follow:
- The measures must directly resolve the stated finding. Read the finding carefully and address the specific gap it describes, not the control in general.
- Measures must be concrete and actionable: describe WHAT should be done, not vague intentions. Prefer specific steps an auditee could actually implement over generic advice like "improve security awareness".
- Ground your measures ONLY in facts explicitly stated in the finding, the control description, and the current state. Do not add numbers, thresholds, frequencies, or timeframes that are not explicitly written there (e.g. if nothing states a review cadence, do not invent "every six months" or similar). Do not name specific tools, systems, platforms, or technologies unless they are explicitly named in the finding or control description. Describe the required control in generic terms instead.
- Do not widen the scope stated in the finding. If the finding says "several accounts" or "some systems", your measure must not generalize that to "all accounts" or "all systems".
- The control's current state may describe several distinct issues at once (this control may have multiple findings drawn from the same current state). Address ONLY what THIS finding states, do not pull in remediation for other issues mentioned in the current state, or in sibling findings, that are not part of this specific finding. Write your measure AS IF you have never seen any other finding for this control and do not know the rest of the current state exists. Your only knowledge of the situation is the single finding given to you below.
Example of the mistake to avoid: 
suppose the current state describes three separate issues:
(a) no formal access review process, 
(b) privileged accounts not audited, 
(c) some accounts have excessive permissions requiring immediate action
and you are asked for a measure for finding (a) ONLY ("There is no formal access review process"). 
Wrong: "Establish a formal access review process for all privileged and service accounts, starting immediately with the accounts found to have excessive permissions." (this pulls in content from findings (b) and (c), which finding (a) never mentioned)
Correct: "Establish a formal process for periodically reviewing access rights." (addresses ONLY what finding (a) states, nothing more)
- If the finding signals urgency (e.g. "immediate remediation required", "critical", "active exposure"), the measure must call for immediate, corrective action on the already-identified instance, not merely a future, recurring, or periodic review process. But only apply this if THIS finding itself states the urgency, do not add urgency language to a measure for a finding that does not itself mention urgency, even if a sibling finding elsewhere does.
- You may use the retrieved past examples below as a guide for tone, structure, and level of specificity, but do NOT copy their specific content. This is a different finding; the examples are style references only.
- Output the measure as a SINGLE plain paragraph (1-4 sentences, length proportional to the finding). Do NOT use bullet points, numbered lists, dashes, or any markdown formatting. If the measure genuinely needs multiple steps, combine them into one flowing paragraph instead of a list. No preamble, no headers, no explanation of your reasoning.

Before finalizing your answer, silently check: 
(1) does every specific noun, number, tool, or system in your measure also appear in the finding, control description, or current state?
(2) does your measure address ONLY this one finding, without pulling in other issues from the current state or sibling findings? 
(3) if the finding indicates urgency, does your measure call for immediate action rather than a periodic process? If any check fails, revise your answer before outputting it.
"""


def build_measure_messages(
        request: MeasureGenerationRequest,
        retrieval_result: RetrievalResult,
) -> List[Dict[str, Any]]:
    """
    Build the chat messages for measure generation.

    :param request: the full endpoint 2 input, including the finding text this request is generating measures for.
    :param retrieval_result: output of retrieval_service.retrieve_measure_examples()
    """
    examples_text = shared_prompt_utils.format_retrieved_examples(
        retrieval_result.examples, show_measures=True
    )
    confidence_text = shared_prompt_utils.confidence_note(retrieval_result)
    lang_instruction = shared_prompt_utils.language_instruction(request.language)

    risk_display = request.risk_level if request.risk_level is not None else "unknown"
    description_display = request.control_description or "(no control description provided)"

    user_prompt_parts = [
        "## Control context",
        f"Norm: {request.norm_title}",
        f"Control ID: {request.control_id}",
        f"Control title: {request.control_title}",
        f"Control description: {description_display}",
        f"Risk level: {risk_display}",
        f"Maturity level (non_conformity): {request.non_conformity}",
        f"Current state (auditee's actual situation. NOTE: this may describe multiple issues; address only the ONE finding below, not other issues mentioned here): {request.current_state}",
        "",
        "## Finding to address (address ONLY this, nothing else from the current state above)",
        request.finding,
        "",
        "## Past finding -> measures examples for reference (style guidance only)",
        examples_text,
    ]

    if confidence_text:
        user_prompt_parts += ["", confidence_text]

    user_prompt_parts += ["", lang_instruction, "", "Now write the measure(s) for the finding above."]

    user_prompt = "\n".join(user_prompt_parts)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
