import os
import sys
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from promptify.core.service import PromptifyService
from promptify.agent.graph import promptify

app = FastAPI(title="Promptify Cloud API")

# Initialize the service
service = PromptifyService(graph=promptify)

class RefineRequest(BaseModel):
    prompt: str
    model_provider: str = "cerebras" # cerebras, openai, etc.
    model_name: Optional[str] = None
    api_key: Optional[str] = None # Optional, user can provide their own
    
class RefineResponse(BaseModel):
    refined_prompt: str
    original_prompt: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "promptify-cloud"}

@app.post("/refine", response_model=RefineResponse)
async def refine_prompt(request: RefineRequest):
    """
    Refines the given prompt using the Promptify Agentic workflow.
    """
    try:
        # Set API key if provided
        if request.api_key:
            # Set the appropriate env var based on provider
            key_name = f"{request.model_provider.upper()}_API_KEY"
            os.environ[key_name] = request.api_key
        
        # Use the service to refine the prompt
        result = service.refine(
            query=request.prompt,
            model_provider=request.model_provider,
            model_name=request.model_name,
            api_key=request.api_key
        )
        
        refined = result.get('final_prompt_draft', 'Error: No refined prompt generated')
        
        return RefineResponse(
            refined_prompt=refined,
            original_prompt=request.prompt
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
