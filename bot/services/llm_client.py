"""LLM client for intent-based routing.

This client wraps the LLM API and handles tool calling loops.
The LLM receives user messages + tool definitions, decides which tools to call,
and the client executes them and feeds results back.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import httpx


class LlmClient:
    """Client for LLM API with tool calling support.
    
    Usage:
        client = LlmClient(base_url="...", api_key="...", model="...")
        response = await client.chat_with_tools(
            messages=[{"role": "user", "content": "what labs are available?"}],
            tools=TOOL_DEFINITIONS,
        )
    """

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Send a chat request to the LLM.
        
        Args:
            messages: List of message dicts with role and content
            tools: Optional list of tool definitions
        
        Returns:
            LLM response with choices
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        response = await self._client.post("/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()

    async def chat_with_tools(
        self,
        messages: list[dict],
        tools: list[dict],
        max_iterations: int = 5,
    ) -> str:
        """Chat with the LLM using tool calling loop.
        
        The LLM may call tools multiple times before producing a final answer.
        
        Args:
            messages: Initial conversation messages
            tools: List of tool definitions
            max_iterations: Maximum tool calling iterations
        
        Returns:
            Final LLM response text
        """
        conversation = list(messages)
        
        for iteration in range(max_iterations):
            # Call LLM
            response = await self.chat(conversation, tools)
            choice = response["choices"][0]
            message = choice["message"]
            
            # Check if LLM wants to call tools
            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                # LLM produced final answer
                return message.get("content", "I don't have information about that.")
            
            # Log tool calls for debugging
            for tc in tool_calls:
                func = tc["function"]
                print(
                    f"[tool] LLM called: {func['name']}({func['arguments']})",
                    file=sys.stderr,
                )
            
            # Execute tool calls and collect results
            tool_results = []
            for tc in tool_calls:
                func = tc["function"]
                tool_name = func["name"]
                tool_args = json.loads(func["arguments"])
                
                # Execute the tool
                result = await self._execute_tool(tool_name, tool_args)
                tool_results.append(result)
                print(f"[tool] Result: {result[:100]}...", file=sys.stderr)
            
            # Feed tool results back to LLM
            print(
                f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM",
                file=sys.stderr,
            )
            
            # Add assistant message with tool calls
            conversation.append(
                {
                    "role": "assistant",
                    "content": message.get("content"),
                    "tool_calls": tool_calls,
                }
            )
            
            # Add tool results
            for i, result in enumerate(tool_results):
                conversation.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_calls[i]["id"],
                        "content": result,
                    }
                )
        
        # If we get here, LLM didn't produce final answer in max iterations
        return "I'm having trouble getting a complete answer. Let me summarize what I found..."

    async def _execute_tool(self, name: str, arguments: dict) -> str:
        """Execute a tool by name.
        
        Args:
            name: Tool name (e.g., "get_items", "get_pass_rates")
            arguments: Tool arguments
        
        Returns:
            Tool result as JSON string
        """
        from services.lms_api import LmsApiClient
        from config import BotSettings
        
        settings = BotSettings()
        client = LmsApiClient(
            base_url=settings.lms_api_base_url,
            api_key=settings.lms_api_key,
        )
        
        try:
            if name == "get_items":
                result = await client.get_items()
            elif name == "get_learners":
                result = await client.get_learners()
            elif name == "get_scores":
                result = await client.get_analytics_scores(arguments.get("lab", ""))
            elif name == "get_pass_rates":
                result = await client.get_pass_rates(arguments.get("lab", ""))
            elif name == "get_timeline":
                result = await client.get_timeline(arguments.get("lab", ""))
            elif name == "get_groups":
                result = await client.get_groups(arguments.get("lab", ""))
            elif name == "get_top_learners":
                result = await client.get_top_learners(
                    arguments.get("lab", ""),
                    arguments.get("limit", 5),
                )
            elif name == "get_completion_rate":
                result = await client.get_completion_rate(arguments.get("lab", ""))
            elif name == "trigger_sync":
                result = await client.trigger_sync()
            else:
                return json.dumps({"error": f"Unknown tool: {name}"})
            
            return json.dumps(result, ensure_ascii=False)
        finally:
            await client.close()


# Tool definitions for the LLM
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks. Use this to discover what labs are available.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled learners and their groups.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submission timeline (submissions per day) for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance and student counts for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default: 5)",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL data sync from autochecker. Use when data seems outdated.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

# System prompt for the LLM
SYSTEM_PROMPT = """You are an assistant for a Learning Management System (LMS). 
You help users understand lab progress, scores, and student performance by querying backend data.

You have access to tools that fetch data from the LMS backend. 
When the user asks a question, use the appropriate tools to get the data, then provide a clear, helpful answer.

Guidelines:
1. Always call tools to get real data before answering questions about labs, scores, or students.
2. For questions like "which lab has the lowest pass rate", first get all labs with get_items, then get_pass_rates for each.
3. Present data in a clear, readable format with percentages and attempt counts.
4. If the user's message is a greeting or unclear, respond naturally without calling tools.
5. If tools fail or return empty data, explain what happened honestly.

Available tools:
- get_items: List all labs and tasks
- get_pass_rates: Get per-task scores for a lab
- get_scores: Get score distribution for a lab
- get_timeline: Get submission timeline for a lab
- get_groups: Get per-group performance
- get_top_learners: Get top students for a lab
- get_completion_rate: Get completion percentage
- get_learners: Get enrolled students
- trigger_sync: Refresh data from autochecker
"""
