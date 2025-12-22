# Promptify Cloud API Documentation

**Base URL**: `https://6948346f001194e559d2.nyc.appwrite.run`

## Authentication
The API is currently public, but specific model providers (like OpenAI or Cerebras) may require an API key passed in the request body if not configured on the server.

---

## Endpoints

### 1. Health Check
Verify the service is running.

- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "ok",
    "service": "promptify-cloud"
  }
  ```

### 2. Refine Prompt
Refine a vague prompt into a professional specification using the Agentic workflow.

- **URL**: `/refine`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | The raw prompt to refine. |
| `model_provider` | string | No | `cerebras` | Provider to use (`cerebras`, `openai`, `gemini`, `anthropic`). |
| `model_name` | string | No | `None` | Specific model name (e.g. `llama3.1-70b`). |
| `api_key` | string | No | `None` | Optional API Key. If omitted, uses server environment variables. |

#### Response Body
| Field | Type | Description |
|-------|------|-------------|
| `refined_prompt` | string | The professionally refined prompt. |
| `original_prompt` | string | The input prompt (echoed back). |

#### Example (cURL)
```bash
curl -X POST "https://6948346f001194e559d2.nyc.appwrite.run/refine" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "build a snake game in python",
    "model_provider": "cerebras"
  }'
```

#### Example (JavaScript/Fetch)
```javascript
const response = await fetch('https://6948346f001194e559d2.nyc.appwrite.run/refine', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        prompt: "make a todo app",
        model_provider: "cerebras"
    })
});

const data = await response.json();
console.log(data.refined_prompt);
```
