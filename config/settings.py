from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Embedding model
EMBEDDING_MODEL_NAME = "mixedbread-ai/deepset-mxbai-embed-de-large-v1"

# Output dimensionality of the embedding model (fixed by the model itself).
EMBEDDING_DIMENSIONS = 1024

# Device for sentence-transformers to run on: "cpu", "cuda", or "mps".
EMBEDDING_DEVICE = "cuda"

# Vector store (ChromaDB)
CHROMA_PERSIST_DIR = str(PROJECT_ROOT / "services" / "database" / "vectorstore" / "audit_rag_chroma_store")

# Two separate collections:
#   - one for "control -> finding" examples   (used by endpoint 1 retrieval)
#   - one for "finding -> measures" examples  (used by endpoint 2 retrieval)
CHROMA_COLLECTION_FINDINGS = "audit_controls_findings"
CHROMA_COLLECTION_MEASURES = "audit_findings_measures"

# Language mapping
LANGUAGE_CODE_MAP = {
    1: "en",
    2: "de",
}

# Retrieval tuning
# Number of few-shot examples to retrieve per request.
RETRIEVAL_TOP_K = 3

# When the metadata-filtered pool (same language + same norm) has fewer than this many candidates,
# we fall back to a relaxed search rather than returning too few / zero examples.
RETRIEVAL_MIN_POOL_SIZE = 3

# How many candidates to pull from Chroma before soft-boost reranking.
# Larger than RETRIEVAL_TOP_K so reranking has something to work with.
RETRIEVAL_CANDIDATE_POOL_MULTIPLIER = 4

# Soft-boost bonuses added to a candidate's similarity score when its risk_level / non_conformity matches the query's.
# A much more semantically similar candidate can still outrank a same-risk-level but less relevant one.
# Tune these if reranking feels too weak/strong.
RETRIEVAL_RISK_LEVEL_BOOST = 0.05
RETRIEVAL_NON_CONFORMITY_BOOST = 0.05

# Sentinel used for records where risk_level is unknown/null in the source data.
# Never award a match bonus against this value.
UNKNOWN_RISK_LEVEL_SENTINEL = -1

# Local LLM (Ollama)
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_MODEL = "mistral-nemo"
OLLAMA_TEMPERATURE = 0
OLLAMA_SEED = 42