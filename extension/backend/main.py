import os
import json
from app_logging import logger

# Lazy initialization — avoids crash at Appwrite cold start
_service = None

def get_service():
    global _service
    if _service is None:
        from promptify.core.service import PromptifyService
        from promptify.agent.graph import promptify
        _service = PromptifyService(graph=promptify)
    return _service

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
            output_format = body.get("output_format")

            # Set API Key in Env (for this execution only)
            if api_key:
                key_name = f"{model_provider.upper()}_API_KEY"
                os.environ[key_name] = api_key

            logger.info(f"Refining prompt with provider: {model_provider}")

            # Call Service
            result = get_service().refine(
                query=prompt_text,
                model_provider=model_provider,
                model_name=model_name,
                api_key=api_key,
                output_format=output_format
            )

            # get_service().refine() returns a str when output_format is set, dict otherwise
            if isinstance(result, str):
                refined = result
            else:
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
