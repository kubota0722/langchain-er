"""
chainの中に2つモデルを入れてみる
ちゃんと推論が2回行われてるか確認するためlangfuseのcallbackを使う
streaming出力ができるかどうか確認する
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

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

prompt1 = """
<Persona>
あなたは内容を整理して言語化することに長けたAIアシスタントです
</Persona>

<Task>
UserInputとして与えられる内容を整理して回答を作成してください
回答の形式はOutputFormatに従ってください
</Task>

<UserInput>
{user_input}
</UserInput>

<OutputFormat>
```json
{{"answer": "生成した回答"}}
```
</OutputFormat>
"""

prompt2 = """
<Persona>
あなたは与えられた文章の内容の正しさを評価し、回答の校正を行うAIアシスタントです
</Persona>

<Task>
AssistatInputとして与えられた文章の内容の正しさを評価します
内容に誤りがあると判断した場合は修正してください
回答はOutputFormatに従ってください
</Task>

<AssistantInput>
{assistant_input}
</AssistantInput>

<OutputFormat>
```json
{{"answer": "チェック後の回答"}}
```
</OutputFormat>
"""

prompt1 = ChatPromptTemplate.from_template(prompt1)

prompt2 = ChatPromptTemplate.from_template(prompt2)

json_parser = JsonOutputParser()

chain = (
    prompt1 
    | model1 
    | json_parser 
    | (lambda x: {"assistant_input": x["answer"]})  # 変換関数を追加、prompt1の出力とprompt2の入力を繋ぐ
    | prompt2 
    | model2 
    | json_parser
)

#result = chain.invoke({"user_input": "langchainについて"}, config={"callbacks": [langfuse_handler]})
#print(result)

# invoke()をstream()に変更し、結果を処理
for chunk in chain.stream({"user_input": "langchainについて"}, config={"callbacks": [langfuse_handler]}):
    if "answer" in chunk:
        print(chunk["answer"], end="\n", flush=True)
