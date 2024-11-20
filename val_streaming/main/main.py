from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser
from pydantic.v1 import BaseModel

import os
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler


class Generate:
    def __init__(
            self,
            llm1: BaseChatModel,
            llm2: BaseChatModel,
            prompt1:ChatPromptTemplate,
            prompt2:ChatPromptTemplate,
            output_parser,
    ):
        self.llm1 = llm1
        self.llm2 = llm2
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.output_parser = output_parser

    def generate(self, user_input: str):
        chain1 = self.prompt1 | self.llm1 | self.output_parser
        
        generate1 = chain1.invoke({"user_input": user_input})
        print(generate1)
        print("--------------------------------")

        prompt2_input = {"assistant_input": generate1["answer"]}
        formatted_prompt2_input = self.prompt2.format(assistant_input=generate1["answer"])

        chain2 = formatted_prompt2_input | self.llm2 | self.output_parser
        return chain2.stream()


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



chain = Generate(model1, model2, prompt1, prompt2, json_parser)

for chunk in chain.generate("langchainについて"):
    if "answer" in chunk:
        print(chunk["answer"], end="\n", flush=True)
