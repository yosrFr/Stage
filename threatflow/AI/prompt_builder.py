from threatflow.AI.context_builder import build_item_context

SYSTEM_PROMPT = """You are a friendly assistant helping non-experts understand cybersecurity alerts on a website. The person you're helping has NO security background.

Rules:
- If you must use a technical term (e.g. "CVSS", "ransomware", "phishing"), briefly explain it in plain words the first time you use it.
- Be reassuring but accurate. Don't minimize real risks, don't cause panic either.
- Only answer using the item data provided below. Don't invent details that aren't in the data.
- If you do not have the answer, do not rewrite the summary and do not re-explain from scratch.
- Keep the initial explanation focused: a clear rewrite of the summary, and a clear explanation of the recommended steps. Don't dump every field (like indicators or CVSS vectors) unless the user asks about them.
"""


def build_initial_prompt(item):
    context = build_item_context(item)

    return f"""Here is the full data for the item the user is currently viewing:

{context}

Please do two things:
1. Rewrite the summary so it's easy to understand.
2. Explain what the recommended steps actually mean and why they matter.
3. Include the vendors advisory link.

List out indicators, CVSS vectors, or other technical fields at the very bottom of the response as reference.
"""


def start_conversation(item):
    """Builds the initial message list to send to the model."""
    return [
        {"role": "user", "content": build_initial_prompt(item)},
    ]


def add_followup(conversation, user_question):
    conversation.append({"role": "user", "content": user_question})
    return conversation


def add_assistant_reply(conversation, assistant_text):
    conversation.append({"role": "assistant", "content": assistant_text})
    return conversation
