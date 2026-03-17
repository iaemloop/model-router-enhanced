# Enhanced Model Router

Smart model routing system that prioritizes free models, requires approval for paid models, and includes daily model health monitoring.

## Features

### 🎯 Smart Free Model Prioritization
- **Always tries free models first** for cost optimization
- **Automatic fallback** to paid models when necessary
- **Complexity analysis** to determine model requirements

### 🔒 Approval System for Paid Models
- **Human approval required** for all paid model usage
- **Detailed explanations** of why paid models are needed
- **Cost tracking** and budget awareness

### 🤖 Daily Model Testing
- **Automatic daily health checks** at 4:00 AM
- **Real-time model status** monitoring
- **Performance tracking** (response times, success rates)

## Quick Start

### 1. Setup Configuration
```bash
# Copy enhanced router to your skills directory
cp -r model-router-enhanced ~/.openclaw/skills/

# Set your OpenRouter API key
export OPENROUTER_API_KEY="your-api-key-here"
```

### 2. Test the Router
```bash
# Test with a simple task (should use free model)
python3 router.py --models models.json --task "Hello, how are you?"

# Test with a complex task (may require paid model approval)
python3 router.py --models models.json --task "Debug this Python memory leak"
```

### 3. Start Daily Monitoring
```bash
# Start the daemon for automatic testing
python3 daemon.py --start

# Check daemon status
python3 daemon.py --status

# Stop daemon when needed
python3 daemon.py --stop
```

## Usage Examples

### Free Model Usage
```bash
$ python3 router.py --models models.json --task "Hello, how are you?"

{
  "name": "openrouter/z-ai/glm-4.5-air:free",
  "provider": "openrouter",
  "cost_score": 0,
  "power_score": 75,
  "capabilities": ["chat", "general", "writing"]
}
---
Status: free_model_success
Reason: free model success - 0 complexity → openrouter/z-ai/glm-4.5-air:free
Cost: $0.000
```

### Paid Model Approval Request
```bash
$ python3 router.py --models models.json --task "Analyze this security vulnerability"

{
  "name": "openrouter/anthropic/claude-3-5-sonnet", 
  "provider": "openrouter",
  "cost_score": 25,
  "power_score": 92,
  "capabilities": ["chat", "analysis", "coding", "reasoning"]
}
---
Status: requires_approval
Reason: requires approval - 3 complexity needs paid model capabilities

🔒 Approval Required:
Task requires advanced technical work complexity.
Selected model: openrouter/anthropic/claude-3-5-sonnet (anthropic)
Estimated cost: $0.250 per request
Capabilities: chat, analysis, coding, reasoning
Model provides: Advanced reasoning and coding capabilities
```

### Model Health Check
```bash
# Check current model status
python3 router.py --check-models

🔍 Available Models Status:
  openrouter/z-ai/glm-4.5-air:free: ✅ Healthy (🆓 Free)
  openrouter/anthropic/claude-3-haiku:free: ✅ Healthy (🆓 Free)
  openrouter/openai/gpt-4o: ✅ Healthy (💰 Paid)
  openrouter/anthropic/claude-3-5-sonnet: ⚠️ Degraded (💰 Paid)
```

## Daily Testing Schedule

### 4:00 AM - Daily Model Health Tests
- Tests all available OpenRouter models
- Updates model status database
- Generates health report

### 9:00 PM - Cost Optimization Report  
- Tracks daily model usage
- Estimates costs
- Provides optimization recommendations

### Hourly Status Checks
- Monitors model health
- Alerts on degraded performance
- Updates statistics

## Model Status System

The system maintains a comprehensive model health database:

```json
{
  "model_status": {
    "openrouter/z-ai/glm-4.5-air:free": {
      "status": "healthy",
      "last_test": "2026-03-16T22:00:00Z",
      "response_time": 2.3,
      "success_rate": 98.5,
      "token_limit": 10000,
      "notes": "Excellent for general chat"
    }
  }
}
```

### Status Levels
- **✅ Healthy**: 95%+ success rate, good performance
- **⚠️ Degraded**: 80-95% success rate, some issues
- **❌ Unhealthy**: <80% success rate, avoid use

## Configuration

### Environment Variables
```bash
export OPENROUTER_API_KEY="your-api-key"
export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
```

### Custom Models
Edit `models.json` to add your preferred models:

```json
{
  "name": "your-custom-model",
  "provider": "openrouter",
  "cost_score": 10,
  "power_score": 80,
  "capabilities": ["chat", "analysis"],
  "description": "Your custom model description"
}
```

## Cost Optimization

### Free Model Priority
The system automatically prioritizes these free models:
1. `openrouter/z-ai/glm-4.5-air:free` - Best overall free model
2. `openrouter/anthropic/claude-3-haiku:free` - Fast and efficient
3. `openrouter/meta/llama-3.1-8b-instruct:free` - Good instruction following

### Paid Model Usage
Paid models are only used when:
- Free models cannot handle the task complexity
- Explicit approval is given
- The task requires specific capabilities

### Cost Tracking
- Tracks daily usage by model
- Estimates costs based on token usage
- Provides usage reports and recommendations

## Integration with OpenClaw

### As a Skill
The enhanced router can be integrated as an OpenClaw skill:

```bash
# Add to your workspace
cp -r model-router-enhanced ~/.openclaw/skills/

# Use in OpenClaw sessions
# The router will automatically handle model selection
```

### With Existing Skills
Replace the original model-router-premium with this enhanced version:

```bash
# Backup original
mv ~/.openclaw/skills/model-router-premium ~/.openclaw/skills/model-router-premium.backup

# Replace with enhanced version
cp -r model-router-enhanced ~/.openclaw/skills/model-router-premium
```

## Monitoring and Alerts

### Health Reports
Daily reports include:
- Model availability statistics
- Performance metrics
- Cost optimization insights
- Recommendations for improvements

### Email Notifications (Optional)
Configure email alerts for:
- Model failures
- Cost threshold breaches
- Performance degradation

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: OPENROUTER_API_KEY environment variable not set
   ```
   Solution: Set your OpenRouter API key in environment variables

2. **Model Testing Fails**
   ```
   Error: Model test failed
   ```
   Solution: Check internet connection and API key validity

3. **Daemon Not Starting**
   ```
   Error: PID file conflict
   ```
   Solution: Remove existing PID file or stop running daemon

### Debug Mode
```bash
# Enable debug logging
export MODEL_ROUTER_DEBUG=1

# Run manual tests
python3 model_tester.py --check-all --report
```

## License

MIT License - feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the model status reports
- Contact support for API-related issues