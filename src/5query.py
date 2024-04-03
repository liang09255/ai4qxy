from typing import List
from langchain.schema.document import Document
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from pymilvus import Collection
import init

init.init()
init.connectMilvus()
ai4qxy_collection = Collection("ai4qxy")
hf_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_documents(content) -> List[Document]:
    embedding = hf_embedding_model.embed_query(content)
    params = {"metric_type": "L2", "offset": 0}
    result = ai4qxy_collection.search(
        data=[embedding],
        anns_field="embedding",
        param=params,
        limit=10,
        output_fields=["content"]
    )
    documents = []
    for hits in result:
        for hit in hits:
            content = hit.entity.get("content")
            doc = Document(page_content=content)
            documents.append(doc)
    return documents

# 查询文档并提问
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

query = "怎么创建课程"
docs = get_documents(query)
print(f"检索到的文档数量{len(docs)}")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
chain = load_qa_chain(llm, chain_type="stuff")
result = chain.invoke({"input_documents": docs, "question": query})
print(result.get("output_text"))
