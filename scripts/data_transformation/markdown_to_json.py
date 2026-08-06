import json
from markdown_it import MarkdownIt


def construct_description_paragraph(lines, start_index):
    """
    Format the description of a control by:
        - adding a number for each paragraph
        - add html <br> tag after every paragraph

    :param lines:  list of strings (lines in the markdown paragraph token)
    :param start_index: the number of the current paragraph in a control
    :return: the accumulated value of the description and the index of the ext paragraph if it exists
    """
    description = ""
    idx = start_index

    for line in lines:
        if line.strip():
            description += f"({idx}) {line}<br>"
            idx += 1

    return description, idx


def construct_description_list(items):
    """
    Returns a list of strings as a single string using html blocks
    :param items: list of strings
    """
    description = "<ul>"

    for item in items:
        if item.strip():
            description += f"<li>{item}</li>"

    description += "</ul>"

    return description


def markdown_to_json(file_path):
    """
    Parse the input markdown file and returns multiple json files derived from it

    Iterate through the markdown file line per line and create json objects.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    md = MarkdownIt()
    tokens = md.parse(content)

    # The lists that will contain the objects
    controls = []
    control_languages = []
    categories = []
    category_languages = []
    chapters = []
    chapter_languages = []

    # The starting ids
    # will be incremented after adding items
    category_id = 1
    chapter_id = 1
    control_id = 1

    # Boolean variables to mark which section are we currently in
    # bol_chapter = True if we encounter a chapter heading and turns False if we encounter any other heading
    # bol_control = True if we encounter a control heading and turns False if we encounter any other heading
    bol_chapter = False
    bol_control = False

    # Paragraph counter
    # Every time there's a new control detected the counter is back to 1
    # The counter is incremented for each paragraph under a control
    paragraph_counter = 1

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])
            text = tokens[i + 1].content.strip()

            # Category
            if level == 3:
                current_category = text

                sub = current_category.split(" ")[0]
                cat_str_id = sub[2:]
                current_category_id = category_id

                category = {
                    "norm_id": 5,
                    "category_id": current_category_id,
                    "id": cat_str_id
                }

                # Avoid duplicate entries if the same category id already exists
                # if not any(obj["id"] == category["id"] for obj in categories):
                categories.append(category)
                category_id += 1

                name = " ".join(current_category.split(" ")[1:])[:-2]

                category_language = {
                    "language_id": 2,
                    "category_name": name,
                    "category_id": current_category_id,
                }

                # Avoid duplicate entries if the same category_language name already exists
                # if not any(obj["category_name"] == category_language["category_name"] for obj in category_languages):
                category_languages.append(category_language)

                bol_chapter = False
                bol_control = False

            # Chapter
            elif level == 5:
                current_chapter = text

                start_pos = current_chapter.find(".")
                chap_str_id = current_chapter.split(" ")[0][start_pos + 1:-1]
                current_chapter_id = chapter_id

                chapter = {
                    "norm_id": 5,
                    "chapter_id": chapter_id,
                    "id": cat_str_id + '.' + chap_str_id,
                }

                # Avoid duplicate entries if the same chapter id already exists
                # if not any(obj["id"] == chapter["id"] for obj in chapters):
                chapters.append(chapter)
                chapter_id += 1

                title = current_chapter.split(" ")[1][:-2]

                chapter_language = {
                    "language_id": 2,
                    "title": title,
                    "chapter_id": current_chapter_id,
                }

                # Avoid duplicate entries if the same chapter_language title already exists
                # if not any(obj["chapter_id"] == chapter_language["chapter_id"] for obj in chapter_languages):
                chapter_languages.append(chapter_language)

                # We're inside a chapter
                bol_chapter = True
                bol_control = False

            # Control
            elif level == 6:
                current_control = text
                control_tag = current_control[current_control.find("(") + 1:current_control.find(")")]

                control = {
                    "norm_id": 5,
                    "control_id": control_id,
                    "id": current_control.split(" ")[0][2:],
                    "category_id": current_category_id,
                    "chapter_id": current_chapter_id,
                    "control_tag_id": 1 if control_tag == "B" else 2 if control_tag == "S" else 3
                }

                # Avoid duplicate entries if the same control id already exists
                # if not any(obj["id"] == control["id"] for obj in controls):
                controls.append(control)

                control_language = {
                    "language_id": 2,
                    "control_id": control_id,
                    "title": current_control[2:-2]
                }

                # Avoid duplicate entries if the same control_language title already exists
                # if not any(obj["title"] == control_language["title"] for obj in control_languages):
                control_languages.append(control_language)
                control_id += 1

                # We're inside control
                bol_control = True
                bol_chapter = False

                # Reset the counter for each control
                paragraph_counter = 1

        # The paragraphs could be the objective of a chapter or the descriptions of a control
        elif token.type == "paragraph_open":
            para_text = tokens[i + 1].content.strip()

            if bol_control:
                # If the text is the control's description
                # Split th paragraph using the seperator \n
                # Number each paragraph and concatenate all the descriptions
                lines = para_text.split("\n")
                addition, paragraph_counter = construct_description_paragraph(lines, paragraph_counter)
                existing = control_language.get("description", "")
                control_language["description"] = existing + addition

            if bol_chapter:
                # If the text is the chapter's objective
                chapter_language["objective"] = para_text

        # The description of the control could have a list
        elif token.type == "bullet_list_open":
            items = []
            j = i + 1
            # Control the depth of the list because it might be nested
            depth = 1
            while j < len(tokens) and depth > 0:
                if tokens[j].type == "bullet_list_open":
                    depth += 1

                elif tokens[j].type == "bullet_list_close":
                    depth -= 1
                    if depth == 0:
                        break

                elif tokens[j].type == "inline":  # The content of each list item
                    items.append(tokens[j].content.strip())

                j += 1

            if bol_control:
                # If the text is the control's description
                # Concatenate all the texts and lists
                existing = control_language.get("description", "")
                control_language["description"] = existing + construct_description_list(items)

            i = j

        i += 1

    with open("../../data/BSI_json/controls.json", "w", encoding="utf-8") as f:
        json.dump(controls, f, indent=2, ensure_ascii=False)

    with open("../../data/BSI_json/control_languages.json", "w", encoding="utf-8") as f:
        json.dump(control_languages, f, indent=2, ensure_ascii=False)

    with open("../../data/BSI_json/categories.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)

    with open("../../data/BSI_json/category_languages.json", "w", encoding="utf-8") as f:
        json.dump(category_languages, f, indent=2, ensure_ascii=False)

    with open("../../data/BSI_json/chapters.json", "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=2, ensure_ascii=False)

    with open("../../data/BSI_json/chapter_languages.json", "w", encoding="utf-8") as f:
        json.dump(chapter_languages, f, indent=2, ensure_ascii=False)


markdown_to_json("../../exports/IT_Grundschutz_Kompendium_Edition2023_filtered.md")
