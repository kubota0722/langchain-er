from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

class Generate:
    def __init__(
            self,
            llm1:ChatOpenAI,
            llm2:ChatOpenAI,
            prompt1:ChatPromptTemplate,
            prompt2:ChatPromptTemplate,
            output_parser:JsonOutputParser
    ):
        self.llm1 = llm1
        self.llm2 = llm2
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.output_parser = output_parser

    def generate(self, user_input: str):
        chain1 = self.prompt1 | self.llm1 | self.output_parser
        
        generate1 = chain1.invoke({"user_input": user_input})

        prompt2_input = {"assistant_input": generate1["answer"]}

        chain2 = prompt2_input | self.llm2 | self.output_parser
        return chain2.stream()
