LANG_NAMES = {
    "deutsch": "German",
    "english": "English",
}


def build_rewrite_prompt(text: str, expected_lang: str) -> str:
    lang_name = LANG_NAMES.get(expected_lang)
    lang_line = (
        f"Output language: {lang_name}. Stay entirely in {lang_name}, no translation, no mixed language.\n"
    )

    return f"""You are rewriting a compliance/audit requirement. Reword it for clarity without changing what it requires.
    
    {lang_line}
    
    RULES:
    1. Same obligation strength, this is the most critical rule. Never add, remove, or change modal verbs (must/shall/should/may/need/muss/soll/sollte/kann) anywhere in the text. If a sentence has no modal verb, the output must not introduce one. This applies to the intro paragraph and bullet items equally.
    2. Same meaning and scope. Nothing added, nothing removed, including qualifiers like "immediately", "in writing", "if applicable", "verifiably".
    2b. Verbless bullet points (noun phrases with no verb, e.g. "+ Code of conduct in case of special incidents.") must remain verbless noun phrases. Do not complete them by adding a verb or modal construction.
    3. Keep technical/legal terms as-is. Never substitute these terms or their German equivalents:
       - "third countries" / "Drittländer"
       - "data controller" / "Verantwortlicher"
       - "data processor" / "Auftragsverarbeiter"
       - "supervisory authority" / "Aufsichtsbehörde"
       - "adequacy decision" / "Angemessenheitsbeschluss"
       - "sub-processor" / "Unterauftragsverarbeiter"
       - "Datenschutzvorfall" ≠ "Datenschutzverletzung"
       - "Datenschutzfolgenabschätzung" (do not abbreviate or substitute)
       - "classified as requiring protection" / "als schutzbedürftig klassifiziert" (do not shorten to "protected" or substitute with "sensitive")
       - "test and trial grounds" / "Test- und Erprobungsgelände" (do not substitute with "test sites" or "test tracks")
       - "customer" and "client" must remain consistent within a single document, use whichever the input uses
    4. Keep all HTML tags exactly as they appear (<strong>, <br>, &nbsp;). Never convert to Markdown or plain text. A standalone bold keyword line like <strong>Must</strong> must stay standalone, unchanged, in the same position.
    5. Don't restructure: same number of sentences/bullets, same order, no new headings or labels.
    6. Every field must show at least some rewording. Vary sentence structure, word choice, or phrasing somewhere in the text, even if the changes are minimal.
    7. Output only the rewritten text, no preamble, no notes.
    8. If the input has explanatory text before the <strong>Must</strong> block, the output must also have explanatory text before it covering the same points. Do not drop the introduction and jump straight to the Must block.
    
    EXAMPLE 1 (English):
    Input:
    <strong>Must</strong><br>
    <strong>+ A policy is created, regularly updated, and approved by the organization's management.</strong><br><br>
    
    Output:
    <strong>Must</strong><br>
    <strong>+ A policy is drafted, kept up to date, and signed off by the organization's leadership.</strong><br><br>
    
    EXAMPLE 2 (German):
    Input:
    <strong>Muss</strong><br>
    <strong>+ Mitarbeiter werden zur Vertraulichkeit verpflichtet.</strong><br><br>
    
    Output:
    <strong>Muss</strong><br>
    <strong>+ Mitarbeiter werden zur Wahrung der Vertraulichkeit angehalten.</strong><br><br>
    
    EXAMPLE 3 (English, paragraph + Must-block):
    Input:
    The organization needs at least one privacy policy. This reflects the importance of data protection and is adapted to the organization.<br><br>
    <strong>Must</strong><br>
    <strong>+ A policy is created, regularly updated, and approved by the organization's management.</strong>
    
    Output:
    The organization must maintain at least one privacy policy. This reflects the importance of data protection and is tailored to the organization.<br><br>
    <strong>Must</strong><br>
    <strong>+ A policy is drafted, kept up to date, and signed off by the organization's leadership.</strong>
    
    NEVER do this:
    Input:  It must be ensured that security requirements are known.
    Output: It is mandatory that security requirements are identified.
    Reason: "must be ensured" was changed to "is mandatory" (modal weakened), and "known" was changed to "identified" (meaning shifted). FAIL.
    Correct output: It must be verified that security requirements are understood.
    
    Text:
    {text}""".strip()
