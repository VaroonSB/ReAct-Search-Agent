# ReAct Search Agent

An AI-powered agent that uses the ReAct (Reasoning and Acting) framework to answer questions by searching the web and returning structured, source-backed answers. Built with [LangChain](https://github.com/langchain-ai/langchain), [Ollama](https://ollama.com/), and [Tavily Search](https://tavily.com/).

## Features

- **ReAct Agent**: Uses the ReAct pattern for reasoning and tool use.
- **Web Search**: Integrates TavilySearch for real-time web results.
- **LLM Support**: Default to Ollama's Llama 3.1, easily switchable to OpenAI or Groq models.
- **Structured Output**: Returns answers and sources in a Pydantic schema.
- **Custom Tool Examples**: See how to add your own tools and callbacks.

## Project Structure

- `main.py` — Entry point; sets up the agent, tools, and runs a sample query.
- `prompt.py` — Contains the custom ReAct prompt template.
- `schema.py` — Pydantic models for agent output.
- `callbacks.py` — Custom callback handler for LLM events.
- `custom_tool_example.py` — Example: minimal custom tool with ReAct agent.
- `custom_tool_with_scratchpad.py` — Example: advanced custom tool with scratchpad and callback handler.
- `requirements.txt` — Python dependencies.
- `pyproject.toml` — Project metadata and dependencies.

## Setup

1. **Clone the repository**

	```bash
	git clone <repo-url>
	cd ReAct-search-agent
	```

2. **Create a virtual environment (recommended)**

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

3. **Install dependencies**

	```bash
	pip install -r requirements.txt
	# or, if using poetry/pdm:
	pip install .
	```

	If `requirements.txt` is missing, install from `pyproject.toml` dependencies manually.

4. **Set up environment variables**

	Create a `.env` file in the project root and add any required API keys (e.g., for Tavily, OpenAI, Groq, etc.). Example:

	```env
	TAVILY_API_KEY=your_tavily_api_key
	# OPENAI_API_KEY=your_openai_api_key
	# GROQ_API_KEY=your_groq_api_key
	```

5. **Run the main agent**

	```bash
	python main.py
	```

	You should see the agent's output for the sample query in the console.

## Custom Tool Examples

### Minimal Custom Tool

Run the minimal custom tool example:

```bash
python custom_tool_example.py
```

### Advanced Custom Tool with Scratchpad and Callback

Run the advanced custom tool example:

```bash
python custom_tool_with_scratchpad.py
```

This demonstrates:
- How to add your own tools
- How to use a scratchpad for intermediate steps
- How to use a custom callback handler for LLM events

## Usage

Modify the `main.py` or custom tool scripts to change the input query or integrate the agent into your own application. The agent is set up to:

1. Accept a user query (e.g., "search for 3 job postings for an ai engineer on linkedin and list their details").
2. Use the ReAct pattern to decide when to search and how to reason.
3. Return a structured response with an answer and a list of sources (URLs).

## Customization

- **Change LLM**: Swap the `llm` variable in `main.py` or the example scripts to use OpenAI, Groq, or other supported models.
- **Add Tools**: Add more tools to the `tools` list for additional capabilities.
- **Prompt Engineering**: Edit `prompt.py` or the prompt in the example scripts to customize the agent's reasoning and output style.
- **Callbacks**: Use or extend `callbacks.py` to add custom logging or monitoring for LLM events.

## Example Output

```
Hello from react-search-agent!
answer='Here are 3 AI Engineer job postings from LinkedIn: ...' sources=[Source(url='https://www.linkedin.com/jobs/view/...'), ...]
```

## Requirements

- Python 3.9+
- API keys for Tavily, and optionally OpenAI or Groq if using those models
