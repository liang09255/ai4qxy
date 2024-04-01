import init
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

init.init()
prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
model = ChatOpenAI()
outputParser = StrOutputParser()
chain = prompt | model | outputParser
res = chain.invoke({"foo": "bears"})
print(res)