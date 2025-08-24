from typing import Union
from dotenv import load_dotenv

from langchain_ollama import ChatOllama

from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description, Tool

from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_groq import ChatGroq

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
Thought: {agent_scratchpad}
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
        input_variables=["input"],
    ).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        stop_sequences=["\nObservation"],
        temperature=0,
    )
    # llm = ChatOllama(
    #     model="llama3.1",
    #     stop=["\nObservation"],
    #     temperature=0,
    # )
    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        input={
            "input": "How many characters are in `HelloWorlds`?",
            "agent_scratchpad": intermediate_steps,
        }
    )
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.invoke(tool_input)

        print(f"{observation=}")

        intermediate_steps.append((agent_step, str(observation)))

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        input={
            "input": "How many characters are in `HelloWorlds`?",
            "agent_scratchpad": intermediate_steps,
        }
    )
    print(agent_step)

    if isinstance(agent_step, AgentFinish):
        print("### AgentFinish ###")
        print(agent_step.return_values)


if __name__ == "__main__":
    main()
