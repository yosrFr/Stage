import re

from bs4 import BeautifulSoup


def strip_html(raw_html: str) -> str:
    """
    Remove HTML tags and normalize whitespace.
    """
    if not raw_html:
        return ""

    # get_text(separator=" ") ensures "<br>" etc. become a space rather than gluing two words together.
    text = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ")

    # Collapse repeated whitespace/newlines left behind by the tag removal.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_control_embedding_text(norm_title: str, control_title: str, control_description_clean: str) -> str:
    """
    Build the exact text that gets embedded for a "control identity" record.
    """
    return f"{norm_title}. {control_title}. {control_description_clean}"


def build_finding_embedding_text(finding_text: str) -> str:
    """
    Build the exact text that gets embedded for a "finding" record.
    """
    return finding_text.strip()
