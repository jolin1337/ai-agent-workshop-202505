import os
from llama_index.llms.openai_like import OpenAILike
import pandas as pd

from autorag.data.qa.filter.dontknow import dontknow_filter_rule_based
from autorag.data.qa.generation_gt.llama_index_gen_gt import (
    make_basic_gen_gt,
    make_concise_gen_gt,
)
from autorag.data.qa.query.llama_gen_query import factoid_query_gen
from autorag.data.qa.sample import random_single_hop
from autorag.parser import Parser
from autorag.data.qa.schema import Raw
from autorag.chunker import Chunker

base_folder = "data/autorag"
os.makedirs(base_folder, exist_ok=True)


def parse():
    parser = Parser(data_path_glob="data/*.md", project_dir=base_folder)
    parser.start_parsing(os.path.join(os.path.dirname(__file__), "parse_config.yaml"))


def chunk():
    chunker = Chunker.from_parquet(
        parsed_data_path="data/autorag/0.parquet", project_dir="data/autorag"
    )
    chunker.start_chunking(
        os.path.join(os.path.dirname(__file__), "./ingest/chunk_config.yaml")
    )


def get_corpus():
    raw = Raw(pd.read_parquet(f"{base_folder}/0.parquet"))
    initial_corpus = raw.chunk(
        "llama_index_chunk", chunk_method="token", chunk_size=128, chunk_overlap=5
    )
    return initial_corpus


def get_llm():
    llm = OpenAILike(
        "llama3.2:1b",
        api_key=os.environ.get("OPENAI_API_KEY", "sk-123"),
        api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
        is_chat_model=True,
        # is_function_calling_model=False,
    )
    return llm


def make_qa(initial_corpus, llm):
    initial_qa = (
        initial_corpus.sample(random_single_hop, n=3)
        .map(
            lambda df: df.reset_index(drop=True),
        )
        .make_retrieval_gt_contents()
        .batch_apply(
            factoid_query_gen,  # query generation
            llm=llm,
        )
        .batch_apply(
            make_basic_gen_gt,  # answer generation (basic)
            llm=llm,
        )
        .batch_apply(
            make_concise_gen_gt,  # answer generation (concise)
            llm=llm,
        )
        .filter(
            dontknow_filter_rule_based,  # filter don't know
            lang="en",
        )
    )

    initial_qa.to_parquet(f"{base_folder}/qa.parquet", f"{base_folder}/corpus.parquet")


def main():
    parse()
    initial_corpus = get_corpus()
    llm = get_llm()
    make_qa(initial_corpus, llm)


if __name__ == "__main__":
    main()
