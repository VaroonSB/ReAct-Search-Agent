from typing import List
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="The agent's answer to the query in string format. Should contain the job listing link as well")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used by the agent to generate the answer"
    )
