def format_iocs(item, max_listed=10):
    iocs = item.get("iocs") or []
    if not iocs:
        return None

    sample = iocs[:max_listed]
    formatted = ", ".join(f"{i['type']}: {i['value']}" for i in sample)
    remaining = len(iocs) - len(sample)
    suffix = f" (+{remaining} more not listed)" if remaining > 0 else ""
    return f"Known indicators ({item.get('iocs_total', len(iocs))} total): {formatted}{suffix}"


def format_playbook_steps(playbook_steps):
    if not playbook_steps:
        return None
    lines = [f"- {s['title']}: {s['detail']}" for s in playbook_steps]
    return "\n".join(lines)


def build_item_context(item):
    """
    A complete, readable description of the item.
    Includes every field, not just summary+steps. Lets the model answer follow-up questions about
    indicators, actors, CVSS, etc. without a second fetch.
    """
    parts = []

    parts.append(f"Title: {item.get('title', 'N/A')}")
    parts.append(f"Category: {item.get('category', 'N/A')}")

    if item.get("summary"):
        parts.append(f"Original summary (technical): {item['summary']}")

    if item.get("severity"):
        severity_line = f"Severity: {item['severity']}"
        if item.get("cvss_score") is not None:
            severity_line += f" (CVSS score {item['cvss_score']}"
            if item.get("cvss_vector"):
                severity_line += f", vector {item['cvss_vector']}"
            severity_line += ")"
        parts.append(severity_line)

    if item.get("actors"):
        parts.append(f"Threat actors: {', '.join(item['actors'])}")

    if item.get("families"):
        parts.append(f"Malware families: {', '.join(item['families'])}")

    ioc_text = format_iocs(item)
    if ioc_text:
        parts.append(ioc_text)

    steps_text = format_playbook_steps(item.get("playbook_steps"))
    if steps_text:
        parts.append(f"Recommended steps (technical):\n{steps_text}")

    return "\n".join(parts)