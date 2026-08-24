from collections import Counter

from config import settings
from services.database.vectorstore import chroma_client


def run() -> None:
    for collection_name in [settings.CHROMA_COLLECTION_FINDINGS, settings.CHROMA_COLLECTION_MEASURES]:
        print(f"Collection: {collection_name}")

        collection = chroma_client.get_collection(collection_name)
        total = collection.count()
        print(f"Total items: {total}\n")

        if total == 0:
            print("(empty, nothing to analyze)\n")
            continue

        # Pull all metadata.
        result = collection.get(include=["metadatas"])
        metadatas = result["metadatas"]

        bucket_counts = Counter((m.get("language"), m.get("norm_title")) for m in metadatas)

        print(f"Number of distinct (language, norm_title) combinations: {len(bucket_counts)}\n")

        # How many combos would succeed at Tier 1 for various MIN_POOL_SIZE thresholds?
        for threshold in [1, 2, 3, 4, 5]:
            combos_meeting_threshold = sum(1 for count in bucket_counts.values() if count >= threshold)
            pct = 100 * combos_meeting_threshold / len(bucket_counts)
            print(
                f"  MIN_POOL_SIZE={threshold}: {combos_meeting_threshold}/{len(bucket_counts)} "
                f"combos ({pct:.0f}%) would pass Tier 1 directly"
            )

        print("\nBucket sizes (language, norm_title) -> count, largest first:")
        for (language, norm_title), count in bucket_counts.most_common():
            print(f"  ({language}, {norm_title!r}): {count}")
        print()


if __name__ == "__main__":
    run()
