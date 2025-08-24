from dotenv import load_dotenv

# from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from schema import AgentResponse
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS

load_dotenv()

tools = [TavilySearch()]
llm = ChatOllama(model="llama3.1")
# llm = ChatOpenAI(model="gpt-5-nano")
# llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

# react_prompt = hub.pull("hwchase17/react")

react_prompt = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x)) # type: ignore

chain = agent_executor | extract_output | parse_output


def main():
    print("Hello from react-search-agent!")

    result = chain.invoke(
        input={
            "input": "search for 3 job postings for an ai engineer on linkedin and list their details",
        },
    )
    print(result)


if __name__ == "__main__":
    main()
