from markdown_it import MarkdownIt


def extract_specific_section(file_path, output_path, start_chapter, first_section_name=None, second_section_name=None,
                             third_section_name=None):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    md = MarkdownIt()
    tokens = md.parse(content)

    result = []
    inside_range = False
    inside_section = False
    current_chapter = None
    current_subtitle = None
    current_paragraph_title = None

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Only process once inside_range is True
        if token.type == "heading_open":
            level = int(token.tag[1])
            text = tokens[i + 1].content.strip()

            # Start range at the chosen chapter
            if level == 2 and text == start_chapter:
                inside_range = True

            if inside_range:  # <-- critical guard
                if level == 2:
                    current_chapter = text
                    result.append(f"## {current_chapter}\n")

                elif level == 3:
                    current_subtitle = text
                    result.append(f"### {current_subtitle}\n")

                elif level == 5:
                    if text == first_section_name or text == second_section_name or text == third_section_name:
                        inside_section = True
                        result.append(f"##### {text}\n")
                    else:
                        inside_section = False

                elif level == 6 and inside_section:
                    current_paragraph_title = text
                    result.append(f"###### {current_paragraph_title}\n")

        # Only keep paragraphs if inside_range AND inside_section
        if inside_range and inside_section and token.type == "paragraph_open":
            para_text = tokens[i + 1].content.strip()
            if current_paragraph_title:
                result.append(para_text + "\n")

        i += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(result))


extract_specific_section(
    "../../exports/IT_Grundschutz_Kompendium_Edition2023.md",
    "../../exports/IT_Grundschutz_Kompendium_Edition2023_filtered.md",
    "**ISMS: Sicherheitsmanagement**",
    "**3.1. Basis-Anforderungen**",
    "**3.2. Standard-Anforderungen**",
    "**3.3. Anforderungen bei erhöhtem Schutzbedarf**"
)
