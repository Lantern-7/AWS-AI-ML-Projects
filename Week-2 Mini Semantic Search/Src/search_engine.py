import chromadb
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class FAQSearchEngine:
    def __init__(self, collection_name="aastu_faqs"):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name=collection_name)
        logging.info("Search Engine initialized.")

    def index_documents(self, documents: list, ids: list):
        self.collection.add(documents=documents, ids=ids)
        logging.info(f"Indexed {len(documents)} documents.")

    def search(self, query: str, top_k: int = 3):
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return results["documents"][0], results["distances"][0]
