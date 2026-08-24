from fastapi import APIRouter, HTTPException, status

from schema.rag_schema import FindingGenerationResponse, build_retrieval_diagnostics
from services.AI.suggesting.rag.rag_sugg.finding_only.rag_prompt_builder import build_finding_messages
from services.AI.suggesting.rag.rag_sugg.finding_only.schema import FindingGenerationRequest
from services.AI.suggesting.rag.rag_sugg.list_output_parsing import parse_findings_list
from services.AI.suggesting.rag.rag_sugg.ollama_client import generate_completion, OllamaGenerationError
from services.AI.suggesting.rag.retrieval import retrieval_service

router = APIRouter(prefix="/suggestion", tags=["rag_system"])


@router.post("/rag_findings", response_model=FindingGenerationResponse)
def generate_finding(request: FindingGenerationRequest) -> FindingGenerationResponse:
    # Retrieve similar past controls with human-written findings.
    control_query = request.to_control_query()
    retrieval_result = retrieval_service.retrieve_finding_examples(control_query)

    # Build the grounded prompt from the request + retrieved examples.
    messages = build_finding_messages(request, retrieval_result)

    # Generate via the local LLM.
    try:
        raw_text = generate_completion(messages)
    except OllamaGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Finding generation failed: {exc}",
        ) from exc

    # Parse the model's numbered-list-or-NONE response into a clean list.
    findings = parse_findings_list(raw_text)

    return FindingGenerationResponse(
        findings=findings,
        retrieval=build_retrieval_diagnostics(retrieval_result),
    )
