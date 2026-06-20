from app.api.v1.dependencies import pipeline
from app.ingestion.seed import seed_documents


def main() -> None:
    for document in seed_documents():
        pipeline.ingest_document(document)
    print("Seeded demo documents.")


if __name__ == "__main__":
    main()
