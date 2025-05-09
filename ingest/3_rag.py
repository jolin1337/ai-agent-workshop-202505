import asyncio
import os

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

from autorag.evaluator import Evaluator
from autorag.validator import Validator
import autorag

autorag.embedding_models["ollama_nomic"] = autorag.LazyInit(
    OpenAILikeEmbedding,
    model_name="nomic-embed-text",
    api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
    api_key="sk-123",
)
base_folder = "data/autorag"
os.makedirs(base_folder, exist_ok=True)


def validate():
    validator = Validator(
        qa_data_path=f"{base_folder}/qa.parquet",
        corpus_data_path=f"{base_folder}/corpus.parquet",
        project_dir=f"{base_folder}/val_trails",
    )
    validator.validate(f"{base_folder}/trials/config.yaml")


def main():
    # validate()
    evaluator = Evaluator(
        qa_data_path=f"{base_folder}/qa.parquet",
        corpus_data_path=f"{base_folder}/corpus.parquet",
        project_dir=f"{base_folder}/trials",
    )
    evaluator.start_trial(f"{base_folder}/trials/config.yaml", skip_validation=True)


if __name__ == "__main__":
    main()
