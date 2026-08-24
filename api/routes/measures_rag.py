from fastapi import APIRouter, HTTPException, status

from schema.rag_schema import MeasureGenerationResponse, build_retrieval_diagnostics
from services.AI.suggesting.rag.measure_only.measure_rag_prompt_builder import build_measure_messages
from services.AI.suggesting.rag.measure_only.measure_rag_schema import MeasureBatchGenerationRequest
from services.AI.suggesting.rag.rag_ollama_client import generate_completion, OllamaGenerationError
from services.AI.suggesting.rag.retrieval import retrieval_service
from services.AI.suggesting.rag.retrieval.output_cleanup import strip_llm_formatting_artifacts

router = APIRouter(prefix="/suggestion", tags=["rag_system"])


@router.post("/rag_measures", response_model=MeasureGenerationResponse)
def generate_measures(request: MeasureBatchGenerationRequest) -> MeasureGenerationResponse:
    if not request.findings:
        return MeasureGenerationResponse(measures=[], retrieval=[])

    single_requests = request.to_single_requests()

    measures: list[str] = []
    diagnostics: list = []

    for i, single_request in enumerate(single_requests):
        # Retrieve similar past findings with human-written measures, for THIS specific finding.
        retrieval_result = retrieval_service.retrieve_measure_examples(single_request.to_finding_query())

        # Build the grounded prompt for this one finding.
        messages = build_measure_messages(single_request, retrieval_result)

        # Generate via the local LLM.
        try:
            measure_text = generate_completion(messages)
        except OllamaGenerationError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Measure generation failed for finding {i + 1}/{len(single_requests)}: {exc}",
            ) from exc

        measure_text = strip_llm_formatting_artifacts(measure_text, known_labels=["Measures", "Measure"])

        measures.append(measure_text)
        diagnostics.append(build_retrieval_diagnostics(retrieval_result))

    return MeasureGenerationResponse(measures=measures, retrieval=diagnostics)
