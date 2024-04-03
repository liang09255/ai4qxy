# 1. 加载文档
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import TokenTextSplitter

loader = TextLoader("../data/qxy-all.txt", encoding="utf-8")
text_spliter = TokenTextSplitter(chunk_size=200, chunk_overlap=50)
docs = text_spliter.split_documents(loader.load())

# 2. 加载embedding模型
print("loading embedding model")

# 方式一 使用towheee的pipelien
# from towhee import AutoPipes
# p = AutoPipes.pipeline('sentence_embedding')
# output = p('Hello world').get()

# 方式二 使用langchain提供的HuggingFaceEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
hf_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("embedding model load success")
# embeddings_doc = hf_embeddings.embed_query("hello world!")

# 3. 连接mivlus，构造写入方法
import init
import hashlib
from pymilvus import Collection
init.connectMilvus()
ai4qxy_collection = Collection("ai4qxy")
def insert(content: str):
    content_byte = content.encode("utf-8")
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