from models import FamilyNorm, Language, Norm, Category, CategoryLanguage, Chapter, ChapterLanguage, Control, \
    ControlLanguage, ControlTagLanguage, ControlTags


def get_or_create_language(db, language_name):
    language = (db.query(Language).filter(Language.language == language_name).first())

    if language:
        return language

    language = Language(language=language_name)

    db.add(language)
    db.flush()

    return language


def get_or_create_family_norm(db, name):
    family = (db.query(FamilyNorm).filter(FamilyNorm.name == name).first())

    if family:
        return family

    family = FamilyNorm(name=name)

    db.add(family)
    db.flush()

    return family


def get_or_create_norm(db, data, family_norm_id):
    norm = (db.query(Norm).filter(Norm.title == data["title"]).first())

    if norm:
        return norm

    nrom = Norm(
        title=data["title"],
        description=data["description"],
        abbreviation=data["abbreviation"],
        publish_year=data["publish_year"],
        family_norm_id=family_norm_id
    )

    db.add(nrom)
    db.flush()

    return nrom


def get_or_create_control_tag(db, control_tag_id):
    tag = db.query(ControlTags).filter(ControlTags.control_tag_id == control_tag_id).first()

    if tag:
        return tag

    tag = ControlTags(control_tag_id=control_tag_id)

    db.add(tag)
    db.flush()

    return tag


def upsert_control_tag_languages(db, control_tag_id, control_tag_language):
    language = get_or_create_language(db, control_tag_language["language"])

    exists = db.query(ControlTagLanguage).filter(
        ControlTagLanguage.control_tag_id == control_tag_id,
        ControlTagLanguage.language_id == language.language_id
    ).first()

    if exists:
        return

    db.add(ControlTagLanguage(
        control_tag_id=control_tag_id,
        language_id=language.language_id,
        title=control_tag_language["title"]
    ))


def import_control_tag_languages(db, control_tag_id, control_tag_languages):
    if not control_tag_id or not control_tag_languages:
        return

    get_or_create_control_tag(db, control_tag_id)
    for control_tag_language in control_tag_languages:
        upsert_control_tag_languages(db, control_tag_id, control_tag_language)


def get_or_create_category(db, item, norm_id):
    category = db.query(Category).filter(Category.id == item["id"], Category.norm_id == norm_id).first()

    if category:
        return category

    category = Category(id=item["id"], norm_id=norm_id)

    db.add(category)
    db.flush()

    return category


def upsert_category_language(db, category_id, category_language):
    language = get_or_create_language(db, category_language["language"])

    exists = (db.query(CategoryLanguage)
              .filter(CategoryLanguage.category_id == category_id,
                      CategoryLanguage.language_id == language.language_id)
              .first())

    if exists:
        return

    db.add(CategoryLanguage(
        category_id=category_id,
        language_id=language.language_id),
        category_name=category_language["category_name"]
    )


def import_categories(db, norm_id, categories):
    category_map = {}

    for item in categories:
        category = get_or_create_category(db, item, norm_id)
        category_map[item["category_id"]] = category.category_id

        for control_language in item.get("category_language", []):
            upsert_category_language(db, category.category_id, control_language)

    return category_map


def get_or_create_chapter(db, item, norm_id):
    chapter = db.query(Chapter).filter(Chapter.id == item["id"], Chapter.norm_id == norm_id).first()

    if chapter:
        return chapter

    chapter = Chapter(id=item["id"], norm_id=norm_id)

    db.add(chapter)
    db.flush()

    return chapter


def upsert_chapter_language(db, chapter_id, chapter_language):
    """
    Insert a ChapterLanguage row if it doesn't exist.
    If it does, only 'objective' is updated
    """
    language = get_or_create_language(db, chapter_language["language"])

    exists = (db.query(ChapterLanguage)
              .filter(ChapterLanguage.chapter_id == chapter_id,
                      ChapterLanguage.language_id == language.language_id)
              .first())

    if exists:
        exists.objective = chapter_language.get("objective", exists.objective)
        return

    db.add(ChapterLanguage(
        chapter_id=chapter_id,
        language_id=language.language_id,
        title=chapter_language["title"],
        objective=chapter_language.get("objective"),
    ))


def import_chapters(db, norm_id, chapters):
    chapter_map = {}

    for item in chapters:
        chapter = get_or_create_chapter(db, item, norm_id)
        chapter_map[item["chapter_id"]] = chapter.chapter_id

        for lang in item.get("chapter_language", []):
            upsert_chapter_language(db, chapter.chapter_id, lang)

    return chapter_map


def get_or_create_control(db, item, norm_id, category_map, chapter_map):
    control = db.query(Control).filter(Control.id == item["id"], Control.norm_id == norm_id).first()

    if control:
        return control

    control_tag_id = item.get("control_tag_id")
    if control_tag_id:
        import_control_tag_languages(db, control_tag_id, item.get("control_tag_languages", []))

    control = Control(
        id=item["id"],
        norm_id=norm_id,
        category_id=category_map[item["category_id"]],
        chapter_id=chapter_map[item["chapter_id"]],
        control_tag_id=control_tag_id
    )

    db.add(control)
    db.flush()

    return control


def upsert_control_language(db, control_id, control_language):
    """
    Insert a ControlLanguage row if it doesn't exist.
    If it does, only 'description' is updated.
    """
    language = get_or_create_language(db, control_language["language"])

    exists = ((db.query(ControlLanguage)
               .filter(ControlLanguage.control_id == control_id,
                       ControlLanguage.language_id == language.language_id))
              .first())

    if exists:
        exists.description = control_language.get("description", exists.description)
        return

    db.add(ControlLanguage(
        control_id=control_id,
        language_id=language.language_id,
        title=control_language["title"],
        description=control_language.get("description")
    ))


def import_controls(db, norm_id, controls, chapter_map, category_map):
    """
    Upsert controls and their language entries for a given norm

    For each control :
    - If the control doesn't exist, it creates it.
    - It processes control_language and control_tag_language by inserting new ones and updating existing ones.

    :param chapter_map: dict containing the link between json_id and database_id produced by 'import_chapters'
    :param category_map: dict containing the link between json_id and category_id produced by 'import_chapters'
    """
    for item in controls:
        control = get_or_create_control(db, item, norm_id, category_map, chapter_map)

        for lang in item.get("control_language", []):
            upsert_control_language(db, control.control_id, lang)

        control_tag_id = item.get("control_tag_id")
        if control_tag_id and item.get("control_tag_languages"):
            import_control_tag_languages(db, control_tag_id, item.get["control_tag_languages"])


def import_norm(db, data):
    """
    Import a norm from a JSON file

    :param db: SQLAlchemy database session
    :param data: Parsed JSON dictionary having the same schema as the norm
    :return: {"message": "Import done"} on success
    :raises HTTPException: If an error occurs during the import, after the rollback.
    """
    try:
        family_norm = get_or_create_family_norm(db, data["family_norm"]["name"])
        norm = get_or_create_norm(db, data, family_norm.family_norm_id)
        category_map = import_categories(db, norm.norm_id, data.get("categories", []))
        chapter_map = import_chapters(db, norm.norm_id, data.get("chapters", []))
        import_controls(db, norm.norm_id, data.get("controls", []), chapter_map, category_map)

        db.commit()

        return {"message": "Import done"}

    except Exception:
        db.rollback()
        raise
