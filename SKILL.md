name: model-router-enhanced
description: Enhanced model router with free model prioritization, automatic testing, and OpenRouter model monitoring. Routes requests based on complexity while respecting free models and requiring approval for paid upgrades.
---

# Enhanced Model Router

## Overview
Enhanced version of model-router-premium with intelligent free model prioritization, automatic model testing, and OpenRouter model health monitoring.

## Key Features

### 🎯 Smart Free Model Prioritization
- **Automatic free model selection**: Always tries free models first
- **Graceful degradation**: Falls back to paid models only when necessary
- **Cost optimization**: Minimizes paid model usage without compromising quality

### 🔒 Approval System for Paid Models
- **Human approval required**: Any paid model usage needs explicit permission
- **Clear explanations**: Provides detailed reasons for paid model requests
- **Budget awareness**: Tracks and reports on paid model usage

### 🤖 Daily Model Testing Agent
- **Automatic testing**: Tests all OpenRouter models daily
- **Health monitoring**: Checks token limits, response quality, and availability
- **Status reporting**: Provides daily model health reports

## Configuration

### Free Model Priority List
```json
{
  "free_models": [
    "openrouter/z-ai/glm-4.5-air:free",
    "openrouter/anthropic/claude-3-haiku:free", 
    "openrouter/meta/llama-3.1-8b-instruct:free"
  ],
  "paid_models": [
    "openrouter/openai/gpt-4o",
    "openrouter/anthropic/claude-3-5-sonnet",
    "openrouter/google/gemini-pro"
  ]
}
```

### Model Health Configuration
```json
{
  "testing": {
    "schedule": "daily",
    "time": "04:00",
    "max_tokens": 1000,
    "test_prompts": [
      "Hello, how are you?",
      "Explain quantum computing in simple terms",
      "Write a Python function to calculate fibonacci numbers"
    ]
  },
  "approval": {
    "require_approval": true,
    "max_daily_cost": 10.00,
    "reason_template": "For task complexity: {task_complexity}, requiring model capabilities: {required_capabilities}"
  }
}
```

## Usage Examples

### Automatic Free Model Routing
```bash
# Always tries free models first
python3 router.py --models models.json --task "Hello, how are you?"

# Output if free model works:
# {
#   "name": "openrouter/z-ai/glm-4.5-air:free",
#   "provider": "openrouter",
#   "cost_score": 0,
#   "status": "free_model_success"
# }

# Output if free model fails and needs approval:
# {
#   "name": "openrouter/anthropic/claude-3-5-sonnet",
#   "provider": "openrouter", 
#   "cost_score": 50,
#   "status": "requires_approval",
#   "reason": "Task requires code analysis capabilities not available in free models"
# }
```

### Daily Model Testing
```bash
# Run manual model health check
python3 tester.py --check-all

# View model health status
python3 tester.py --status

# Get detailed report
python3 tester.py --report --format json
```

## Model Health Status

The system maintains a model health database:

```json
{
  "model_status": {
    "openrouter/z-ai/glm-4.5-air:free": {
      "status": "healthy",
      "last_test": "2026-03-16T22:00:00Z",
      "response_time": 2.3,
      "success_rate": 98.5,
      "token_limit": 10000,
      "notes": "Excellent for general chat, limited context"
    },
    "openrouter/anthropic/claude-3-5-sonnet": {
      "status": "healthy", 
      "last_test": "2026-03-16T22:00:00Z",
      "response_time": 5.1,
      "success_rate": 99.2,
      "token_limit": 200000,
      "cost_per_1k": 0.015
    }
  }
}
```

## Approval Workflow

### 1. Free Model Attempt
```
Task: "Debug this Python function"
↓
Try: openrouter/z-ai/glm-4.5-air:free
↓
Result: ❌ Cannot handle complex code analysis
↓
Request: Needs approval for paid model
```

### 2. Approval Request
```
🔒 PAID MODEL APPROVAL REQUIRED

Model: openrouter/anthropic/claude-3-5-sonnet
Cost: $0.015 per 1K tokens
Reason: Task requires advanced code debugging capabilities not available in free models
Task: "Debug this Python function that's causing memory leaks"

Approve? (y/n) 
```

### 3. Daily Model Health Report
```
📊 Daily Model Health Report - 2026-03-16

✅ HEALTHY MODELS (8):
• openrouter/z-ai/glm-4.5-air:free - 98.5% success, 2.3s response
• openrouter/meta/llama-3.1-8b-instruct:free - 97.2% success, 3.1s response
• openrouter/anthropic/claude-3-haiku:free - 99.1% success, 1.8s response

⚠️ DEGRADED MODELS (2):  
• openrouter/openai/gpt-4o - 85.3% success, 8.2s response (high latency)
• openrouter/google/gemini-pro - 92.1% success, 6.5s response (occasional timeouts)

❌ UNAVAILABLE MODELS (1):
• openrouter/cohere/command-r-plus - 0% success (API errors)

📈 SUMMARY: 11 models operational, 2 degraded, 1 offline
```

## Integration with OpenClaw

### Automatic Testing Agent
```bash
# Start daily model testing daemon
python3 daemon.py --start

# Check daemon status  
python3 daemon.py --status

# Stop daemon
python3 daemon.py --stop
```

### Model Status Commands
```bash
# Check current model recommendations
python3 router.py --check-models

# View cost optimization report
python3 router.py --cost-report

# Test specific model
python3 router.py --test-model "openrouter/z-ai/glm-4.5-air:free"
```

## Cost Optimization

### Smart Routing Algorithm
1. **First attempt**: Use best available free model
2. **Assessment**: Check if task complexity matches model capabilities
3. **Fallback**: If free model insufficient, request paid model approval
4. **Optimization**: Track usage patterns and recommend model selections

### Cost Tracking
```json
{
  "daily_costs": {
    "2026-03-16": 0.45,
    "2026-03-15": 0.00,
    "2026-03-14": 1.20
  },
  "model_usage": {
    "openrouter/z-ai/glm-4.5-air:free": 47,
    "openrouter/anthropic/claude-3-5-sonnet": 3
  }
}
```

## Benefits

### 🎯 Cost Efficiency
- **Zero cost for simple tasks**: Uses free models for 80%+ of requests
- **Controlled paid usage**: Only pays for necessary complexity
- **Budget predictability**: Daily cost limits and notifications

### 🤖 Reliability  
- **Daily health checks**: Ensures models are working before use
- **Automatic fallbacks**: Switches to working models if primary fails
- **Performance monitoring**: Tracks response times and success rates

### 👨‍💬 User Control
- **Approval system**: Always knows when paid models will be used
- **Detailed explanations**: Understands why specific models are needed
- **Usage transparency**: Full visibility into model selection reasoning

## Installation

```bash
# Copy enhanced router
cp /path/to/model-router-enhanced/ ~/.openclaw/skills/

# Install dependencies
pip install requests pydantic

# Start daily testing
python3 daemon.py --start
```

The enhanced router provides intelligent model selection while maintaining cost control and reliability through daily monitoring and approval workflows.