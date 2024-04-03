from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections

print("connect to milvus")
connections.connect(alias="default", host="localhost", port="19530")
print("connect to milvus success")

def build_ai4qxy_collection() -> Collection:
    print("start to build ai4qxy collection")
    # 字段设置
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=32, is_primary=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1024)
    ]
    schema = CollectionSchema(fields=fields)
    ai4qxy_collection = Collection("ai4qxy", schema)

    # 给向量字段创建索引
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 10}
    }
    ai4qxy_collection.create_index("embedding", index)
    ai4qxy_collection.load()
    print("build success")
    return ai4qxy_collection

if __name__ == "__main__":
    build_ai4qxy_collection()
