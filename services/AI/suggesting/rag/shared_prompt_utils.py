from typing import List

from services.AI.suggesting.rag.retrieval.retrieval_schemas import RetrievedExample, RetrievalResult

LANGUAGE_INSTRUCTIONS = {
    1: "Write your entire response in English.",
    2: "Write your entire response in German (Deutsch).",
}


def language_instruction(language: int) -> str:
    """
    Fallback to English if an unexpected language code ever shows up,
    rather than raising and breaking generation over a formatting detail.
    """
    return LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS[1])


def format_retrieved_examples(examples: List[RetrievedExample], show_measures: bool = False) -> str:
    """
    Render retrieved examples as numbered blocks for the prompt.

    show_measures=False for the finding prompt.
    show_measures=True for the measure prompt.
    """
    if not examples:
        return "(No comparable past examples were found in the historical data.)"

    blocks = []
    for i, ex in enumerate(examples, start=1):
        risk_display = ex.risk_level if ex.risk_level is not None else "unknown"
        block = (
            f"Example {i} "
            f"(norm: {ex.norm_title} | control: {ex.control_title} | "
            f"risk_level: {risk_display} | maturity level: {ex.non_conformity})\n"
            f'  Finding: "{ex.finding}"'
        )
        if show_measures and ex.measures:
            block += f'\n  Measures: "{ex.measures}"'
        blocks.append(block)

    return "\n\n".join(blocks)


def confidence_note(result: RetrievalResult) -> str:
    """
    A short instruction block telling the model how much to trust the retrieved examples.
    """
    if not result.examples:
        return (
            "IMPORTANT: No comparable historical examples were found at all for this control. "
            "Base your answer solely on the control information provided below, and be conservative. "
            "Do not invent details not present in the control description or current state."
        )
    if result.used_no_filter_fallback:
        return (
            "NOTE: The examples below come from a different norm and/or language than this control "
            "(no close precedent was found in the historical data). "
            "Use them only as loose stylistic guidance for tone and structure, not as close factual precedent."
        )
    if result.used_language_only_filter:
        return (
            "NOTE: The examples below are in the same language but from different norms than this control. "
            "Use them as general guidance on tone and structure, "
            "weighing exact content less heavily than you would for a same-norm example."
        )
    return ""
