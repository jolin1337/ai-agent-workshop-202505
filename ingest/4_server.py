import os
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from autorag.deploy import ApiRunner
import autorag
import nest_asyncio

autorag.embedding_models["ollama_nomic"] = autorag.LazyInit(
    OpenAILikeEmbedding,
    model_name="nomic-embed-text",
    api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
    api_key="sk-123",
)

nest_asyncio.apply()

base_folder = "data/autorag"
latest_trial = str(
    sorted(
        [int(t) for t in os.listdir(f"{base_folder}/trials") if t[0] in "0123456789"]
    )[-1]
)
print("Runing api with trial nr:", latest_trial)
runner = ApiRunner.from_trial_folder(f"{base_folder}/trials/{latest_trial}")
runner.run_api_server(remote=False)
