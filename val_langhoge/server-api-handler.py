from fastapi import FastAPI, Request
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from typing import Any, Dict
from pydantic import BaseModel, Field

from langserve import APIHandler, add_routes

app = FastAPI()

# prompt template
prompt = PromptTemplate(
    input_variables=["param"],
    template="This is the parameter value: {param}. Please generate a response based on this information."
)

# Input schema
class CustomInput(BaseModel):
    param: str = Field(description="Parameter value")

# Custom Runnable
class CustomChain(Runnable):
    def invoke(self, input: Dict[str, Any]) -> str:
        param = input.get("param", "")
        print("2")
        print(param)
        return f"Processed: {param}"

    def get_input_schema(self):
        return CustomInput.schema()

# Create an instance of CustomChain
chain = CustomChain()

# API Handler
api_handler = APIHandler(runnable=chain, path="/process/{param}")

# routing by fastapi
@app.post("/process/{param}")
async def process(param: str, request: Request):
    print("1")
    print(param)
    # リクエストボディを取得
    body = await request.json()
    # パラメータをボディに追加
    body["param"] = param
    return await api_handler.invoke(request, body)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)