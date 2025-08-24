from typing import Union
from dotenv import load_dotenv

from langchain_ollama import ChatOllama

from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description, Tool

from schema import AgentResponse
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish

load_dotenv()

prompt_template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:
"""


@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in the text"""
    print("I am getting invoked")
    return len(text)


def find_tool_by_name(tools, tool_name) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


def main():
    print("Hello from react-search-agent!")
    tools = [get_text_length]
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["input", "tools"],
    ).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
        format_instructions=PydanticOutputParser(
            pydantic_object=AgentResponse
        ).get_format_instructions(),
    )
    llm = ChatOllama(
        model="llama3.1", stop=["\nObservation", "Observation"], temperature=0
    )
    agent = prompt | llm | ReActSingleInputOutputParser()
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        input={"input": "How many characters are in `HelloWorlds`?"}
    )
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.invoke(tool_input)

        print(f"{observation=}")


if __name__ == "__main__":
    main()
