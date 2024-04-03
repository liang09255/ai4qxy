# 加载
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import TokenTextSplitter

loader = TextLoader("../data/qxy-all.txt", encoding="utf-8")
text_spliter = TokenTextSplitter(chunk_size=200, chunk_overlap=50)
docs = text_spliter.split_documents(loader.load())

# from towhee import AutoPipes
#
# p = AutoPipes.pipeline('sentence_embedding')
# output = p('Hello world').get()
# print(output)
print("loading embedding model")
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

hf_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("embedding model load success")
# embeddings_doc = hf_embeddings.embed_query("hello world!")
# print(embeddings_doc)

# mivlus创建集合
from pymilvus import connections

print("connect to mivlus")
connections.connect(alias="default", host="localhost", port="19530")
print("connect to mivlus success")
from pymilvus import FieldSchema, CollectionSchema, Collection, DataType

ai4qxy_collection = Collection("ai4qxy")
ai4qxy_collection.load()


def insert(content: str):
    content_byte = content.encode("utf-8")
    import hashlib
    hash_value = hashlib.md5(content_byte).hexdigest()
    res = ai4qxy_collection.query(f'id=="{hash_value}"')
    if len(res) != 0:
        return

    embedding = hf_embedding_model.embed_query(content)
    entity = [
        [hash_value],
        [embedding],
        [content]
    ]
    ai4qxy_collection.insert(entity)


# 写入milvus
for doc in docs:
    content = doc.page_content.strip()
    insert(content)

from typing import List
from langchain.schema.document import Document


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


query = "怎么创建课程"
docs = get_documents(query)
print(f"检索到的文档数量{len(docs)}")

from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
import init

init.init()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
chain = load_qa_chain(llm, chain_type="stuff")
result = chain.invoke({"input_documents": docs, "question": query})
print(result.get("output_text"))
