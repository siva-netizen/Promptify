import os
import sys
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app_logging import logger
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


logger.info("Starting Promptify Cloud API...")

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

# --- Appwrite Function Entrypoint ---
def main(context):
    """
    Appwrite Function Entrypoint.
    Docs: https://appwrite.io/docs/products/functions/development
    """
    # 1. Log Start
    logger.info(f"Appwrite Function Triggered: {context.req.method} {context.req.path}")

    # 2. Handle Health Check
    if context.req.path == "/health" or (context.req.path == "/" and context.req.method == "GET"):
        return context.res.json({
            "status": "ok",
            "service": "promptify-cloud-function"
        })

    # 3. Handle Refine Endpoint
    if context.req.path == "/refine" and context.req.method == "POST":
        try:
            # Parse Body (Appwrite gives it as object or string depending on content-type)
            body = context.req.body
            if isinstance(body, str):
                import json
                try:
                    body = json.loads(body)
                except:
                    pass # Keep as is if parsing fails

            # Extract fields
            prompt_text = body.get("prompt")
            if not prompt_text:
                 return context.res.json({"error": "Missing 'prompt' field"}, 400)

            model_provider = body.get("model_provider", "cerebras")
            model_name = body.get("model_name")
            api_key = body.get("api_key")

            # Set API Key in Env (for this execution only)
            if api_key:
                key_name = f"{model_provider.upper()}_API_KEY"
                os.environ[key_name] = api_key

            logger.info(f"Refining prompt with provider: {model_provider}")

            # Call Service
            result = service.refine(
                query=prompt_text,
                model_provider=model_provider,
                model_name=model_name,
                api_key=api_key
            )
            
            refined = result.get('final_prompt_draft', 'Error: No refined prompt generated')
            
            logger.info("Refinement successful")

            return context.res.json({
                "refined_prompt": refined,
                "original_prompt": prompt_text
            })

        except Exception as e:
            logger.error(f"Refinement Error: {str(e)}")
            return context.res.json({"error": str(e)}, 500)

    # 4. Handle 404
    return context.res.json({"error": "Not Found. Use POST /refine"}, 404)
