import os
import requests
from typing import List
from mcp.server.fastmcp import FastMCP
import chromadb
from tqdm import tqdm

server = FastMCP("Kvadrat intranät")
chroma_client = chromadb.PersistentClient(
    path=os.path.join(os.path.dirname(__file__), "chroma_db")
)


class Embedding:
    def __call__(self, input: str | List[str]) -> List[List[float]]:
        emb = (
            requests.post(
                os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/")
                + "/api/embed",
                json={"model": "nomic-embed-text:latest", "input": input},
            )
            .json()
            .get("embeddings", [])
        )
        return emb


def chunk_seq(doc: str | list, chunk_size: int = 500, overlap: int = 100):
    if chunk_size < 1 or overlap < 0:
        raise ValueError("size must be >= 1 and overlap >= 0")

    for i in range(0, len(doc) - overlap, chunk_size - overlap):
        yield doc[i : i + chunk_size]


def ingest(domain: str):
    collection_name = domain
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "A collection for Bolagsverket scraped data"},
        embedding_function=Embedding(),  # Use the custom embedding function
    )
    for root, dirs, files in tqdm(list(os.walk(f"data/{domain}"))):
        if len(files) <= 0:
            continue
        documents, ids = zip(
            *[
                (chunk, f"{file}_{i}")
                for file in files
                if file.endswith(".md")
                for i, chunk in enumerate(
                    chunk_seq(open(os.path.join(root, file), "r").read())
                )
            ]
        )
        collection.add(documents=list(documents), ids=list(ids))


@server.tool()
async def retrieve(query: str) -> dict:
    collection = chroma_client.get_or_create_collection(
        name=os.environ.get("CRAWL_DOMAIN", "bolagsverket.se"),
        metadata={"description": "A collection for Bolagsverket scraped data"},
        embedding_function=Embedding(),  # Use the custom embedding function
    )
    results = collection.query(query_texts=[query], n_results=4)
    return results


if __name__ == "__main__":
    import asyncio

    # ingest("bolagsverket.se")
    print(asyncio.run(retrieve("verklig huvudman")))
