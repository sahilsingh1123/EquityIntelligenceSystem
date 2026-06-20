from app.repositories import repository
from app.services.pipeline import IntelligencePipeline

pipeline = IntelligencePipeline(repository)


def get_pipeline() -> IntelligencePipeline:
    return pipeline
