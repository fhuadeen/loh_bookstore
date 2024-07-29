import json
from typing import List, Dict, Tuple
import os
import sys
import abc
import uuid

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

from loh_ai.loh_langchain import (
    RedundantChromaFilterRetriever,
    LohLangChain,
    LangchainModel,
    DocumentLoader,
    LangChainVectorDB,
)

from flask import jsonify

from api.config import S3_BUCKET_NAME


class AIService():
    embeddings_obj = OpenAIEmbeddings()

    def __init__(self):

        self.chroma = Chroma(
            persist_directory="chromadb",
            embedding_function=self.embeddings_obj
        )

        self.retriever = RedundantChromaFilterRetriever(
            embeddings_obj=self.embeddings_obj,
            chroma=self.chroma
        )
        self.chat_model = LangchainModel(model_name="chat_openai")

    @classmethod
    def embed(cls, data: Dict) -> Tuple[Dict, int]:
        """
        Embed the content of a pdf-formated book

        Args:
            data (Dict): Book metadata

        Returns:
            Tuple[Dict, int]: Embedding successful
        """
        s3_key = data.get("file_name")

        try:
            docs = DocumentLoader().load_file_from_s3(
                bucket_name=S3_BUCKET_NAME,
                s3_key=s3_key,
            )
        except Exception as err:
            return jsonify({"error": f"Error loading file from storage: {str(err)}"}), 200

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        try:
            split_docs = text_splitter.split_documents(documents=docs)
        except Exception as err:
            return jsonify({"error": f"Error splitting document: {str(err)}"}), 500

        try:
            LangChainVectorDB().create_embeddings_db(
                db_type="chroma",
                docs=split_docs,
                embeddings_obj=cls.embeddings_obj,
            )
        except Exception as err:
            return jsonify({"error": f"Error creating embedding: {str(err)}"}), 500

        return jsonify({"message": "Embeddings created"}), 201

    def summarise(self, query: str) -> Tuple[Dict, int]:
        """
        Summarise content of a book

        Args:
            query (str): Summary query

        Returns:
            _type_: AI response
        """
        try:
            response = LohLangChain().run(
                query=query,
                retriever=self.retriever,
                chat_model=self.chat_model,
            )
        except Exception as err:
            return jsonify({"error": f"Error generating summary: {str(err)}"}), 500

        return jsonify({
            "message": response,
        }), 200
