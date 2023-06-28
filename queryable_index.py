import os
from llama_index import (
    LLMPredictor,
    ServiceContext,
    StorageContext,
    load_index_from_storage
)
from langchain.chat_models import ChatOpenAI


class QueryableIndex:
    def __init__(self, persist_dir):
        self.persist_dir = persist_dir
        self.index = None
        self.llm = None
        self.llm_predictor = None

    def initialize(self):
        print("Initializing index")

        if not os.path.exists(self.persist_dir):
            raise FileNotFoundError(f"No index found in {self.persist_dir}")

        self.llm = ChatOpenAI(temperature=0, model_name='gpt-4',
                              max_tokens=4096, request_timeout=240)
        self.llm_predictor = LLMPredictor(llm=self.llm)

        service_context = ServiceContext.from_defaults(
            chunk_size_limit=512, llm_predictor=self.llm_predictor)

        self.index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=self.persist_dir),
            service_context=service_context
        )
        print('Initialized index')

    def query(self, prompt):
        if not self.index:
            raise ValueError(
                "Index not initialized. Please call initialize() method first."
            )

        return self.index.as_query_engine().query(prompt)
