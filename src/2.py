# 1. 读取知识库文档
txt = ""
with open("../data/qxy-1.txt", encoding="utf-8") as f:
    for line in f:
        txt += line.strip()

# 2. 构建chain --- 用户输入 + 文档 = 完整的promt -> gpt -> 结果
import init
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

init.init()
template = """参考以下文档回答问题:
{document}

问题:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
output_parser = StrOutputParser()
chain = prompt | model | output_parser
res = chain.invoke({"document": txt, "question": "学员怎么学习我的课程"})
print(res)
