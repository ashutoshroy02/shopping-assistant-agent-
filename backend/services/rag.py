from typing import Any

import chromadb
from chromadb.config import Settings

from config import get_settings

settings = get_settings()

chroma_client = chromadb.HttpClient(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT,
)


def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


class RAGService:
    def __init__(self):
        self.products_collection = get_or_create_collection("products")
        self.manuals_collection = get_or_create_collection("manuals")
        self.faqs_collection = get_or_create_collection("faqs")

    async def add_product(self, product: dict[str, Any]) -> None:
        doc_id = str(product.get("id", ""))
        document = f"{product.get('title', '')} {product.get('description', '')} {product.get('brand', '')}"
        metadata = {
            "category": product.get("category", ""),
            "brand": product.get("brand", ""),
            "price": product.get("price", 0),
            "rating": product.get("rating", 0),
        }

        self.products_collection.upsert(
            ids=[doc_id],
            documents=[document],
            metadatas=[metadata],
        )

    async def add_products_batch(self, products: list[dict[str, Any]]) -> None:
        ids = []
        documents = []
        metadatas = []

        for product in products:
            doc_id = str(product.get("id", ""))
            document = f"{product.get('title', '')} {product.get('description', '')} {product.get('brand', '')}"
            metadata = {
                "category": product.get("category", ""),
                "brand": product.get("brand", ""),
                "price": product.get("price", 0),
                "rating": product.get("rating", 0),
            }

            ids.append(doc_id)
            documents.append(document)
            metadatas.append(metadata)

        if ids:
            self.products_collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )

    async def search_products(
        self,
        query: str,
        n_results: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        where = {}
        if filters:
            if filters.get("category"):
                where["category"] = filters["category"]
            if filters.get("brand"):
                where["brand"] = filters["brand"]

        results = self.products_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where if where else None,
        )

        products = []
        if results and results.get("ids") and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                products.append({
                    "id": doc_id,
                    "score": results["distances"][0][i] if results.get("distances") else 0,
                    "metadata": metadata,
                })

        return products

    async def add_manual(self, manual: dict[str, Any]) -> None:
        doc_id = str(manual.get("id", ""))
        document = manual.get("content", "")
        metadata = {
            "product_id": manual.get("product_id", ""),
            "title": manual.get("title", ""),
        }

        self.manuals_collection.upsert(
            ids=[doc_id],
            documents=[document],
            metadatas=[metadata],
        )

    async def search_manuals(
        self, query: str, product_id: str | None = None, n_results: int = 5
    ) -> list[dict[str, Any]]:
        where = {}
        if product_id:
            where["product_id"] = product_id

        results = self.manuals_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where if where else None,
        )

        manuals = []
        if results and results.get("ids") and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                manuals.append({
                    "id": doc_id,
                    "content": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": metadata,
                })

        return manuals

    async def add_faq(self, faq: dict[str, Any]) -> None:
        doc_id = str(faq.get("id", ""))
        document = f"{faq.get('question', '')} {faq.get('answer', '')}"
        metadata = {
            "category": faq.get("category", ""),
        }

        self.faqs_collection.upsert(
            ids=[doc_id],
            documents=[document],
            metadatas=[metadata],
        )

    async def search_faqs(
        self, query: str, n_results: int = 5
    ) -> list[dict[str, Any]]:
        results = self.faqs_collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        faqs = []
        if results and results.get("ids") and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                faqs.append({
                    "id": doc_id,
                    "content": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": metadata,
                })

        return faqs


rag_service = RAGService()
