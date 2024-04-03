import os
from pymilvus import connections

def init():
    # 在环境变量中配置openai的key和代理地址
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["OPENAI_API_BASE"] = "https://one.996444.icu/v1"

def connectMilvus():
    print("connect to milvus")
    connections.connect(alias="default", host="localhost", port="19530")
    print("connect to milvus success")