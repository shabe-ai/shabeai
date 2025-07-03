# Structured Logging with Request IDs

This application uses `structlog` for structured JSON logging with request IDs for better observability and debugging.

## Features

- **Request ID Middleware**: Every request gets a unique UUID that's added to response headers as `X-Request-ID`
- **Structured JSON Logs**: All logs are output in JSON format with timestamps
- **Component Binding**: Logs are tagged with component names for easy filtering
- **Request Context**: Request IDs are automatically included in all log entries

## Usage

### Basic Logging

```python
import structlog
from fastapi import Request

# In any endpoint
def my_endpoint(request: Request):
    log = structlog.get_logger().bind(
        component="my-api",
        request_id=request.state.request_id
    )
    log.info("operation_started")
    # ... do work ...
    log.info("operation_completed", result="success")
```

### Example from Meta Router

```python
@router.get("/healthz")
async def healthz(request: Request):
    log = structlog.get_logger().bind(
        component="health-api",
        request_id=request.state.request_id
    )
    log.info("health_check_requested")
    return {"status": "ok"}
```

### Example from Leads Router

```python
@router.post("/", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadCreate, request: Request, db: Session = Depends(get_session)):
    log = structlog.get_logger().bind(
        component="leads-api",
        request_id=request.state.request_id
    )
    log.info("lead_creation_requested", lead_email=lead.email)
    new_lead = LeadService(db).create(lead)
    log.info("lead_created", lead_id=new_lead.id)
    return new_lead
```

## Log Output Format

Logs are output in JSON format with the following structure:

```json
{
  "timestamp": "2025-06-30T21:55:13.123456Z",
  "level": "info",
  "event": "health_check_requested",
  "component": "health-api",
  "request_id": "c7daa0be-4fec-41bc-a365-cfeb05a84e70"
}
```

## Request ID Headers

Every response includes an `X-Request-ID` header with a unique UUID:

```
HTTP/1.1 200 OK
x-request-id: c7daa0be-4fec-41bc-a365-cfeb05a84e70
Content-Type: application/json
...
```

## Configuration

The logging is configured in `app/logging_config.py`:

- Uses ISO timestamps
- Outputs JSON format
- Log level: INFO
- Output: stdout

## Benefits

1. **Traceability**: Every log entry can be traced back to a specific request
2. **Structured Data**: JSON format makes logs easy to parse and analyze
3. **Component Isolation**: Different parts of the app are clearly separated
4. **Observability**: Easy to monitor and debug production issues 