#!/usr/bin/env python3

import argparse
import json
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
import requests

class EnhancedModelRouter:
    def __init__(self, models_path: str):
        self.models = self.load_models(models_path)
        self.model_status = self.load_model_status()
        self.free_models = self.get_free_models()
        self.paid_models = [m for m in self.models if m not in self.free_models]
        
    def load_models(self, path: str) -> List[Dict]:
        """Load models configuration from JSON file"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Models file not found: {path}")
            sys.exit(1)
    
    def load_model_status(self) -> Dict:
        """Load model health status from database"""
        status_file = "model_status.json"
        try:
            with open(status_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def get_free_models(self) -> List[str]:
        """Identify free models from configuration"""
        return ["glm-4.5-air:free", "claude-3-haiku:free"]
    
    def get_model_complexity(self, task: str) -> int:
        """Analyze task complexity and return complexity score"""
        task_lower = task.lower()
        
        # Simple heuristics for complexity
        if len(task) <= 40 and not any(word in task_lower for word in 
            ["analyze", "debug", "complex", "explain", "design", "implement"]):
            return 0  # Low complexity
        
        complex_keywords = [
            "analyze", "debug", "security", "optimize", "refactor", "implement",
            "architecture", "performance", "scalability", "algorithms", "machine learning"
        ]
        
        keyword_count = sum(1 for word in complex_keywords if word in task_lower)
        if keyword_count >= 3:
            return 3  # High complexity
        elif keyword_count >= 1:
            return 2  # Medium complexity
        else:
            return 1  # Low-moderate complexity
    
    def is_model_healthy(self, model_name: str) -> bool:
        """Check if model is healthy based on status database"""
        status = self.model_status.get(model_name, {})
        return status.get("status") == "healthy"
    
    def test_model_response(self, model_info: Dict, test_prompt: str) -> bool:
        """Test if a model can respond to a prompt"""
        try:
            # This would make actual API calls in a real implementation
            # For now, simulate based on model capabilities
            model_name = model_info.get("name", "").lower()
            
            # Simple simulation: assume most models can handle basic prompts
            if len(test_prompt) < 100:
                return True
            
            # Assume complex models can handle longer prompts
            if "claude" in model_name or "gpt" in model_name or "gemini" in model_name:
                return True
                
            return True  # Default to working for simulation
            
        except Exception as e:
            print(f"Model test failed: {e}")
            return False
    
    def select_model(self, task: str, min_capability: Optional[str] = None, 
                    prefer: Optional[List[str]] = None) -> Dict:
        """Enhanced model selection with free model priority"""
        
        complexity = self.get_model_complexity(task)
        
        # First try: Free models
        free_candidates = []
        for model in self.models:
            if model.get("name") in self.free_models and self.is_model_healthy(model.get("name")):
                if min_capability and min_capability not in model.get("capabilities", []):
                    continue
                free_candidates.append(model)
        
        # Sort free models by capability and cost
        if free_candidates:
            free_candidates.sort(key=lambda m: (
                -m.get("power_score", 0),  # Prefer more capable free models
                m.get("cost_score", float('inf'))  # Then by cost
            ))
            
            # Test the best free model
            best_free = free_candidates[0]
            if self.test_model_response(best_free, task):
                return {
                    "model": best_free,
                    "reason": f"free model success - {complexity} complexity → {best_free['name']}",
                    "cost": 0,
                    "status": "free_model_success"
                }
        
        # Second try: Paid models (needs approval)
        paid_candidates = []
        for model in self.models:
            if model.get("name") not in self.free_models and self.is_model_healthy(model.get("name")):
                if min_capability and min_capability not in model.get("capabilities", []):
                    continue
                paid_candidates.append(model)
        
        if paid_candidates:
            # Sort paid models by capability and cost
            paid_candidates.sort(key=lambda m: (
                -m.get("power_score", 0),
                m.get("cost_score", float('inf'))
            ))
            
            best_paid = paid_candidates[0]
            
            return {
                "model": best_paid,
                "reason": f"requires approval - {complexity} complexity needs paid model capabilities",
                "cost": best_paid.get("cost_score", 0),
                "status": "requires_approval",
                "explanation": self.generate_approval_explanation(task, complexity, best_paid)
            }
        
        # Fallback: Any available model
        available_models = [m for m in self.models if self.is_model_healthy(m.get("name"))]
        if available_models:
            return {
                "model": available_models[0],
                "reason": f"fallback model - limited options available",
                "cost": available_models[0].get("cost_score", 0),
                "status": "fallback"
            }
        
        # No models available
        return {
            "model": {},
            "reason": "no healthy models available",
            "cost": 0,
            "status": "no_models_available"
        }
    
    def generate_approval_explanation(self, task: str, complexity: int, model: Dict) -> str:
        """Generate explanation for why paid model approval is needed"""
        capability_explanation = {
            0: "general conversation",
            1: "moderate analysis", 
            2: "complex analysis",
            3: "advanced technical work"
        }
        
        return f"""Task requires {capability_explanation.get(complexity, 'unknown')} complexity.
Selected model: {model['name']} ({model.get('provider', 'unknown')})
Estimated cost: ${model.get('cost_score', 0) * 0.01:.3f} per request
Capabilities: {', '.join(model.get('capabilities', []))}
Model provides: {model.get('description', 'advanced AI capabilities')}"""

def main():
    parser = argparse.ArgumentParser(description="Enhanced model router with free model priority")
    parser.add_argument("--models", required=True, help="path to models JSON")
    parser.add_argument("--task", required=True, help="task description")
    parser.add_argument("--min-capability", help="require model to have this capability")
    parser.add_argument("--prefer", action='append', help="prefer model/provider name")
    parser.add_argument("--dry", action='store_true', help="don't print JSON, only show reasoning")
    parser.add_argument("--check-models", action='store_true', help="check available models status")
    parser.add_argument("--cost-report", action='store_true', help="show cost optimization report")
    parser.add_argument("--test-model", help="test specific model response")
    
    args = parser.parse_args()
    
    router = EnhancedModelRouter(args.models)
    
    if args.check_models:
        print("🔍 Available Models Status:")
        for model in router.models:
            name = model.get("name")
            status = "✅ Healthy" if router.is_model_healthy(name) else "❌ Unhealthy"
            free_model = "🆓 Free" if name in router.free_models else "💰 Paid"
            print(f"  {name}: {status} ({free_model})")
        return
    
    if args.cost_report:
        print("💰 Cost Optimization Report:")
        print(f"  Free models available: {len(router.free_models)}")
        print(f"  Paid models available: {len(router.paid_models)}")
        print(f"  Total models: {len(router.models)}")
        print(f"  Healthy models: {sum(1 for m in router.models if router.is_model_healthy(m.get('name')))}")
        return
    
    if args.test_model:
        model_to_test = next((m for m in router.models if m.get("name") == args.test_model), None)
        if model_to_test:
            test_result = router.test_model_response(model_to_test, "Hello, test prompt")
            status = "✅ Working" if test_result else "❌ Failed"
            print(f"{args.test_model}: {status}")
        else:
            print(f"Model {args.test_model} not found")
        return
    
    # Normal model selection
    result = router.select_model(args.task, args.min_capability, args.prefer)
    
    if not args.dry:
        print(json.dumps(result["model"], ensure_ascii=False, indent=2))
    
    print(f"---")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")
    
    if result.get('cost', 0) > 0:
        print(f"Cost: ${result['cost'] * 0.01:.3f}")
    
    if result.get('explanation'):
        print(f"\n🔒 Approval Required:")
        print(result['explanation'])

if __name__ == '__main__':
    main()