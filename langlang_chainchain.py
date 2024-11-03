"""
chainの中に2つモデルを入れてみる
ちゃんと推論が2回行われてるか確認するためlangfuseのcallbackを使う
streaming出力ができるかどうか確認する
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler


load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

langfuse_handler = CallbackHandler(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_HOST
)

model1 = ChatOpenAI(model_name="gpt-4o", api_key=OPENAI_API_KEY)
model2 = ChatOpenAI(model_name="gpt-4o", api_key=OPENAI_API_KEY)

prompt1 = ChatPromptTemplate.from_template(
    "あなたは{user_input}について説明してください。"
)

prompt2 = ChatPromptTemplate.from_template(
    "あなたは与えられた文章の内容の正しさを評価してください{model1_output}"
)

chain = (prompt1 | model1 | prompt2 | model2)

#result = chain.invoke({"user_input": "ドナルド・トランプ"}, config={"callbacks": [langfuse_handler]})
#print(result)

# invoke()をstream()に変更し、結果を処理
for chunk in chain.stream({"user_input": "ドナルド・トランプ"}, config={"callbacks": [langfuse_handler]}):
    print(chunk.content, end="|", flush=True)
