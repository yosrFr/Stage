import json
import sys
from typing import List
from config import settings

from services.AI.suggesting.rag.retrieval.audit_control import ControlRecord, IndexedExample
from services.AI.suggesting.rag.retrieval import text_utils, embedding_service
from services.database.vectorstore import chroma_client

INPUT_JSON_PATH = "../../../test_input_files/training_data.json"


def load_control_records(json_path: str) -> List[ControlRecord]:
    """
    Load and validate the raw JSON export into a list of ControlRecord objects.
    Validation happens via Pydantic, so malformed records fail loudly at ingest time with a clear error,
    rather than silently breaking retrieval downstream.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    records: List[ControlRecord] = []
    errors = []
    for i, raw_record in enumerate(raw_data):
        try:
            records.append(ControlRecord(**raw_record))
        except Exception as exc:
            errors.append(f"  - record #{i} (control_id={raw_record.get('control_id', '?')}): {exc}")

    if errors:
        print(f"WARNING: {len(errors)} record(s) failed validation and were skipped:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)

    return records


def build_indexed_examples(records: List[ControlRecord]) -> List[IndexedExample]:
    """
    Turn ControlRecords into IndexedExamples.

    Key rules (agreed on during design):
      - Records with NO usable finding anywhere in question_responses are skipped entirely.
      - A record with MULTIPLE question_responses produces MULTIPLE IndexedExamples (one per finding/measure pair),
        each independently retrievable, sharing the same control-level metadata.
      - A finding with an empty/missing `measures` is still indexed (it's valid for the findings collection)
        but will naturally be a weaker candidate for the measures collection, since there is no measure text to embed there.
    """
    examples: List[IndexedExample] = []

    for record_idx, record in enumerate(records):
        if not record.has_usable_examples():
            continue

        clean_description = text_utils.strip_html(record.control_description)

        for idx, qr in enumerate(record.question_responses):
            if not qr.finding or not qr.finding.strip():
                # No finding in this particular question_response means nothing to index for this pair,
                # even if the record overall has other usable pairs.
                continue

            example = IndexedExample(
                example_id=f"{record.control_id}__record{record_idx}__{idx}",
                norm_title=record.norm_title,
                control_id=record.control_id,
                control_title=record.control_title,
                control_description_clean=clean_description,
                language=record.language,
                risk_level=record.risk_level,
                non_conformity=record.non_conformity,
                finding=qr.finding.strip(),
                measures=(qr.measures.strip() if qr.measures else None),
                embedding_text=text_utils.build_control_embedding_text(
                    record.norm_title, record.control_title, clean_description
                ),
            )
            examples.append(example)

    return examples


def _risk_level_for_metadata(risk_level) -> int:
    return risk_level if risk_level is not None else settings.UNKNOWN_RISK_LEVEL_SENTINEL


def ingest_findings_collection(examples: List[IndexedExample]) -> None:
    """
    Populate the "control -> finding" collection.
    Embeds each example's control-identity text (norm + title + description).
    """
    if not examples:
        print("No examples to ingest into the findings collection. Skipping.")
        return

    texts_to_embed = [ex.embedding_text for ex in examples]
    vectors = embedding_service.embed_passages(texts_to_embed)

    ids = [ex.example_id for ex in examples]
    documents = texts_to_embed
    metadatas = [
        {
            "norm_title": ex.norm_title,
            "control_id": ex.control_id,
            "control_title": ex.control_title,
            "language": ex.language,
            "risk_level": _risk_level_for_metadata(ex.risk_level),
            "non_conformity": ex.non_conformity,
            "finding": ex.finding,
            "measures": ex.measures or "",
        }
        for ex in examples
    ]

    chroma_client.upsert_examples(
        collection_name=settings.CHROMA_COLLECTION_FINDINGS,
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"Ingested {len(examples)} example(s) into '{settings.CHROMA_COLLECTION_FINDINGS}'.")


def ingest_measures_collection(examples: List[IndexedExample]) -> None:
    """
    Populate the "finding -> measures" collection.
    Embeds each example's FINDING text.
    This collection is searched at generation time using the newly generated finding as the query,
    to retrieve precedent measures.

    Only examples that actually have a measures value are indexed here.
    A finding with no historical measure is useless as a measures example.
    """
    usable = [ex for ex in examples if ex.measures]

    if not usable:
        print("No examples with measures to ingest into the measures collection. Skipping.")
        return

    texts_to_embed = [text_utils.build_finding_embedding_text(ex.finding) for ex in usable]
    vectors = embedding_service.embed_passages(texts_to_embed)

    ids = [f"{ex.example_id}__measure" for ex in usable]
    documents = texts_to_embed
    metadatas = [
        {
            "norm_title": ex.norm_title,
            "control_id": ex.control_id,
            "control_title": ex.control_title,
            "language": ex.language,
            "risk_level": _risk_level_for_metadata(ex.risk_level),
            "non_conformity": ex.non_conformity,
            "finding": ex.finding,
            "measures": ex.measures,
        }
        for ex in usable
    ]

    chroma_client.upsert_examples(
        collection_name=settings.CHROMA_COLLECTION_MEASURES,
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"Ingested {len(usable)} example(s) into '{settings.CHROMA_COLLECTION_MEASURES}'.")


def run(json_path: str) -> None:
    print(f"Loading records from {json_path} ...")
    records = load_control_records(json_path)
    print(f"Loaded {len(records)} valid record(s).")

    examples = build_indexed_examples(records)
    print(f"Built {len(examples)} indexable example(s) (records with usable findings).")

    ingest_findings_collection(examples)
    ingest_measures_collection(examples)

    print("\nCurrent collection sizes:")
    print(f"  {settings.CHROMA_COLLECTION_FINDINGS}: {chroma_client.count(settings.CHROMA_COLLECTION_FINDINGS)}")
    print(f"  {settings.CHROMA_COLLECTION_MEASURES}: {chroma_client.count(settings.CHROMA_COLLECTION_MEASURES)}")


if __name__ == "__main__":
    run(INPUT_JSON_PATH)
