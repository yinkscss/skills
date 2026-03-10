# Deployment & Production

Best practices for deploying LangChain applications to production.

## Table of Contents

- [LangSmith](#langsmith)
- [FastAPI Deployment](#fastapi-deployment)
- [Docker](#docker)
- [Environment Configuration](#environment-configuration)
- [Monitoring & Logging](#monitoring--logging)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Security](#security)
- [Scaling](#scaling)

## LangSmith

LangSmith provides tracing, evaluation, and monitoring for LangChain applications.

### Setup

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

### Tracing

```python
from langchain_openai import ChatOpenAI

# Automatically traced
llm = ChatOpenAI()
response = llm.invoke("Hello!")

# View trace at: https://smith.langchain.com
```

### Custom Runs

```python
from langsmith import Client

client = Client()

# Create custom run
with client.trace(name="custom_operation") as run:
    result = perform_operation()
    run.end(outputs={"result": result})
```

### Evaluation

```python
from langsmith import Client
from langchain.evaluation import load_evaluator

client = Client()

# Create dataset
dataset = client.create_dataset("test_dataset")
client.create_examples(
    dataset_id=dataset.id,
    inputs=[{"question": "What is AI?"}],
    outputs=[{"answer": "Artificial Intelligence..."}]
)

# Evaluate
def run_chain(example):
    return rag_chain.invoke(example)

results = client.evaluate(
    run_chain,
    dataset_name="test_dataset",
    evaluators=[load_evaluator("qa")]
)
```

### Feedback

```python
# Collect user feedback
from langsmith import Client

client = Client()

run_id = "abc123"  # From traced run
client.create_feedback(
    run_id=run_id,
    key="helpfulness",
    score=0.9,
    comment="Very helpful response"
)
```

## FastAPI Deployment

### Basic Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = FastAPI()

# Initialize chain
llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("Answer: {question}")
chain = prompt | llm

class Query(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

@app.post("/query", response_model=Response)
async def query(query: Query):
    try:
        result = await chain.ainvoke({"question": query.question})
        return Response(answer=result.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Streaming Endpoint

```python
from fastapi.responses import StreamingResponse
import asyncio

@app.post("/stream")
async def stream_response(query: Query):
    async def generate():
        async for chunk in chain.astream({"question": query.question}):
            yield f"data: {chunk.content}\n\n"
            await asyncio.sleep(0.01)
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### With Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

@app.post("/query", dependencies=[Depends(verify_token)])
async def secure_query(query: Query):
    result = await chain.ainvoke({"question": query.question})
    return Response(answer=result.content)
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/query")
@limiter.limit("10/minute")
async def rate_limited_query(request: Request, query: Query):
    result = await chain.ainvoke({"question": query.question})
    return Response(answer=result.content)
```

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt

```txt
langchain==0.1.0
langchain-openai==0.0.5
langchain-community==0.0.20
langgraph==0.0.30
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
python-dotenv==1.0.0
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### Build and Run

```bash
# Build
docker build -t langchain-app .

# Run
docker run -p 8000:8000 --env-file .env langchain-app

# Or with docker-compose
docker-compose up -d
```

## Environment Configuration

### .env File

```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=production

# Database
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_WORKERS=4
```

### Config Class

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str | None = None
    langchain_api_key: str
    environment: str = "production"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Monitoring & Logging

### Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName
        }
        return json.dumps(log_data)

# Setup logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Use
logger.info("Processing query", extra={"user_id": "123", "query": "..."})
```

### Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

# Define metrics
request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.post("/query")
async def monitored_query(query: Query):
    request_count.inc()
    
    with request_duration.time():
        result = await chain.ainvoke({"question": query.question})
    
    return Response(answer=result.content)
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    try:
        # Check dependencies
        await check_database()
        await check_llm_api()
        
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503
```

## Error Handling

### Global Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.environment != "production" else None
        }
    )
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_llm_with_retry(query: str):
    return await chain.ainvoke({"question": query})
```

### Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_external_api():
    # Fails fast after 5 failures
    # Retries after 60 seconds
    return await external_api_call()
```

## Performance Optimization

### Caching

```python
from functools import lru_cache
from langchain.cache import InMemoryCache, RedisCache
from langchain.globals import set_llm_cache

# LLM response cache
set_llm_cache(RedisCache(redis_url="redis://localhost:6379"))

# Function cache
@lru_cache(maxsize=1000)
def expensive_operation(input: str):
    return result
```

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Async Operations

```python
import asyncio

async def parallel_queries(queries: list[str]):
    """Execute multiple queries in parallel."""
    tasks = [chain.ainvoke({"question": q}) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

### Batch Processing

```python
# Process multiple queries efficiently
queries = [{"question": q} for q in query_list]
results = await chain.abatch(queries)
```

## Security

### API Key Management

```python
from cryptography.fernet import Fernet
import os

# Encrypt API keys
def encrypt_key(key: str) -> str:
    f = Fernet(os.environ["ENCRYPTION_KEY"])
    return f.encrypt(key.encode()).decode()

def decrypt_key(encrypted: str) -> str:
    f = Fernet(os.environ["ENCRYPTION_KEY"])
    return f.decrypt(encrypted.encode()).decode()
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator

class Query(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    
    @validator("question")
    def validate_question(cls, v):
        # Prevent injection attacks
        forbidden = ["<script>", "DROP TABLE", "eval("]
        if any(word in v for word in forbidden):
            raise ValueError("Invalid input detected")
        return v
```

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("100/hour")
async def rate_limited(request: Request, query: Query):
    return await process_query(query)
```

## Scaling

### Horizontal Scaling

```python
# Run multiple workers
# uvicorn main:app --workers 4

# Or with gunicorn
# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Load Balancing

```nginx
# nginx.conf
upstream langchain_app {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://langchain_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langchain-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: langchain
  template:
    metadata:
      labels:
        app: langchain
    spec:
      containers:
      - name: app
        image: langchain-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: langchain-service
spec:
  selector:
    app: langchain
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Best Practices

### 1. Graceful Shutdown

```python
import signal

def signal_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    # Cleanup operations
    cleanup()
    exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

### 2. Configuration Management

```python
# Different configs for different environments
config = {
    "development": {
        "log_level": "DEBUG",
        "workers": 1,
        "cache": False
    },
    "production": {
        "log_level": "INFO",
        "workers": 4,
        "cache": True
    }
}

current_config = config[os.getenv("ENVIRONMENT", "development")]
```

### 3. Monitoring Dashboards

Use Grafana with Prometheus for metrics visualization:

```python
# Export custom metrics
from prometheus_client import Gauge

active_requests = Gauge('active_requests', 'Number of active requests')
llm_token_usage = Counter('llm_tokens_used', 'Total LLM tokens used')

@app.middleware("http")
async def track_requests(request: Request, call_next):
    active_requests.inc()
    response = await call_next(request)
    active_requests.dec()
    return response
```

### 4. Backup and Recovery

```python
import boto3
from datetime import datetime

def backup_vectorstore():
    """Backup vector store to S3."""
    s3 = boto3.client('s3')
    
    # Save vectorstore
    vectorstore.save_local("/tmp/backup")
    
    # Upload to S3
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3.upload_file(
        "/tmp/backup",
        "my-bucket",
        f"backups/vectorstore_{timestamp}"
    )
```

### 5. Cost Tracking

```python
from langchain.callbacks import get_openai_callback

@app.post("/query")
async def tracked_query(query: Query):
    with get_openai_callback() as cb:
        result = await chain.ainvoke({"question": query.question})
        
        # Log costs
        logger.info(
            "Query cost",
            extra={
                "tokens": cb.total_tokens,
                "cost": cb.total_cost,
                "user_id": request.user_id
            }
        )
    
    return Response(answer=result.content)
```

## Troubleshooting

### High Latency

1. Enable caching
2. Use async operations
3. Implement connection pooling
4. Add load balancing
5. Scale horizontally

### Memory Leaks

1. Clear caches periodically
2. Use generators for large datasets
3. Monitor memory usage
4. Implement proper cleanup

### Rate Limit Errors

1. Implement exponential backoff
2. Use multiple API keys
3. Add request queuing
4. Cache responses

### Database Connection Issues

1. Use connection pooling
2. Implement retry logic
3. Add health checks
4. Monitor connection count
