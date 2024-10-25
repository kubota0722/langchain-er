import os
from dotenv import load_dotenv
from typing import Dict, Any

from fastapi import FastAPI, Depends, Request
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
from pydantic.v1 import BaseModel
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from langfuse.callback import CallbackHandler

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MY_NAME = os.getenv("MY_NAME")
MY_FAVORITE_CHARACTER = os.getenv("MY_FAVORITE_CHARACTER")
PRODUCT_NAME = os.getenv("PRODUCT_NAME")

langfuse = Langfuse()
langfuse_handler = CallbackHandler()

app = FastAPI(
    title="LangChainer",
    version="0.1.0",
    description="Imitate the tone of your favorite character."
)

add_routes(
    app=app,
    runnable=ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo"),
    path="/openai",
)

class CharacterRequest(BaseModel):
    topic: str

class InputLLMChainModel(BaseModel):
    product: str
    character: str
    name: str
    question: str

def get_name(name: str):
    print(f"get_name function called with: {name}")
    return {"name": name}

async def character_controller(input: Dict[str, Any], config: RunnableConfig):
    name = config.get("name", MY_NAME)
    print(f"Name from config: {name}")
    print(f"Input: {input}")
    
    langfuse_prompt = langfuse.get_prompt("one_question_to_character")
    prompt = ChatPromptTemplate.from_template(langfuse_prompt.get_langchain_prompt())
    print(f"Prompt: {prompt}")
    
    model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4-1106-preview")
    chain = prompt | model

    llm_input = InputLLMChainModel(
        product=PRODUCT_NAME,
        character=MY_FAVORITE_CHARACTER,
        name=name,
        question=input["topic"]
    )

    generated_answer = chain.invoke(input=llm_input.dict(), config={"callbacks": [langfuse_handler]})
    return generated_answer

add_routes(
    app=app,        
    runnable=RunnableLambda(character_controller),
    path="/{name}/character",
    input_type=Dict[str, Any],
    #RunnableConfig={"name": str},
    dependencies=[Depends(get_name)]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)