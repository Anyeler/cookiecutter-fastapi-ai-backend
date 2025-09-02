"""FastAPI application with LangChain, OpenAI, and optional MCP integration."""

import os
from typing import List, Optional, Dict, Any
import json
import asyncio
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request{% if cookiecutter.enable_websocket == "yes" %}, WebSocket, WebSocketDisconnect{% endif %}
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import openai
from openai import AsyncOpenAI

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

{% if cookiecutter.enable_langgraph == "yes" -%}
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
{% endif -%}

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.description }}",
    version="0.1.0",
)

# Configure OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "{{ cookiecutter.openai_model }}")

if not openai_api_key:
    print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")

# Initialize LangChain ChatOpenAI
llm = ChatOpenAI(
    model=openai_model,
    temperature=0.7,
    streaming=True,
) if openai_api_key else None

# Initialize AsyncOpenAI client for streaming
async_openai_client = AsyncOpenAI(
    api_key=openai_api_key
) if openai_api_key else None

# Pydantic models
class Message(BaseModel):
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of conversation messages")
    model: Optional[str] = Field(default=openai_model, description="OpenAI model to use")
    temperature: Optional[float] = Field(default=0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")

class ChatResponse(BaseModel):
    content: str = Field(..., description="Generated response content")
    model: str = Field(..., description="Model used for generation")

{% if cookiecutter.enable_langgraph == "yes" -%}
# LangGraph State
class State(TypedDict):
    messages: Annotated[list, add_messages]

def call_model(state: State):
    """Call the language model."""
    if not llm:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(State)
workflow.add_node("model", call_model)
workflow.set_entry_point("model")
workflow.add_edge("model", END)

# Compile the graph
graph = workflow.compile()
{% endif -%}

@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "{{ cookiecutter.project_name }}"}

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint using LangChain ChatOpenAI."""
    if not llm:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    try:
        # Convert request messages to LangChain format
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        
        # Generate response
        response = llm.invoke(
            langchain_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        return ChatResponse(
            content=response.content,
            model=request.model or openai_model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/v1/chat/stream")
async def chat_stream(prompt: str, model: Optional[str] = None):
    """Streaming chat endpoint using OpenAI SDK."""
    if not async_openai_client:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    async def generate():
        try:
            stream = await async_openai_client.chat.completions.create(
                model=model or openai_model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.7,
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    # Format as SSE event
                    content = chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'content': content})}\n\n"
            
            # Send completion signal
            yield f"data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

{% if cookiecutter.enable_websocket == "yes" -%}
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket chat endpoint for real-time streaming."""
    await websocket.accept()
    
    if not async_openai_client:
        await websocket.send_json({
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        })
        await websocket.close()
        return
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            prompt = data.get("prompt", "")
            
            if not prompt:
                await websocket.send_json({"error": "No prompt provided"})
                continue
            
            # Stream response
            try:
                stream = await async_openai_client.chat.completions.create(
                    model=openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                    temperature=0.7,
                )
                
                async for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        await websocket.send_json({"content": content})
                
                # Send completion signal
                await websocket.send_json({"content": "[DONE]"})
                
            except Exception as e:
                await websocket.send_json({"error": f"Error generating response: {str(e)}"})
    
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
{% endif -%}

{% if cookiecutter.enable_langgraph == "yes" -%}
@app.post("/v1/agent")
async def agent_chat(request: ChatRequest):
    """Agent endpoint using LangGraph workflow."""
    if not llm:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    try:
        # Convert request messages to LangChain format
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        
        # Run the workflow
        result = graph.invoke({"messages": langchain_messages})
        
        # Get the last AI message
        last_message = result["messages"][-1]
        
        return ChatResponse(
            content=last_message.content,
            model=request.model or openai_model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in agent workflow: {str(e)}")
{% endif -%}

# TODO: MCP Integration
# Uncomment the following import when implementing MCP tools:
# from {{ cookiecutter.package_name }}.mcp.placeholder import get_mcp_tools

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)