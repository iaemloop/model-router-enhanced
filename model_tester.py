#!/usr/bin/env python3

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText

class ModelTester:
    def __init__(self):
        self.test_results = {}
        self.model_status_file = "model_status.json"
        self.load_model_status()
    
    def load_model_status(self) -> Dict:
        """Load existing model status"""
        try:
            with open(self.model_status_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_model_status(self, status: Dict):
        """Save model status to file"""
        with open(self.model_status_file, "w") as f:
            json.dump(status, f, indent=2)
    
    def get_openrouter_models(self) -> List[Dict]:
        """Get list of available OpenRouter models"""
        try:
            response = requests.get("https://openrouter.ai/api/v1/models")
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching OpenRouter models: {e}")
            return []
    
    def test_model_response(self, model_info: Dict, test_prompt: str) -> Dict:
        """Test a single model's response"""
        model_id = model_info.get("id")
        model_name = model_info.get("name")
        
        start_time = time.time()
        
        try:
            # Make API call to test the model
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.get_api_key()}",
                    "HTTP-Referer": "https://localhost:3000",
                    "X-Title": "Model Tester"
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": test_prompt}],
                    "max_tokens": 100
                }
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                return {
                    "success": True,
                    "response_time": response_time,
                    "content_length": len(content),
                    "has_response": len(content.strip()) > 0,
                    "full_response": result
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code,
                    "response_time": response_time
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def get_api_key(self) -> str:
        """Get OpenRouter API key from environment"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        return api_key
    
    def run_daily_tests(self) -> Dict:
        """Run tests on all available models"""
        print("🧪 Starting daily model tests...")
        
        models = self.get_openrouter_models()
        print(f"Found {len(models)} models to test")
        
        test_results = {}
        
        # Test prompts for different scenarios
        test_prompts = [
            "Hello, how are you?",
            "Explain quantum computing in simple terms",
            "Write a Python function to calculate fibonacci numbers"
        ]
        
        for model in models:
            model_id = model.get("id")
            model_name = model.get("name")
            
            print(f"Testing {model_name}...")
            
            model_results = {
                "model_id": model_id,
                "model_name": model_name,
                "tests": [],
                "summary": {}
            }
            
            # Test with multiple prompts
            for i, prompt in enumerate(test_prompts):
                print(f"  Test {i+1}: {prompt[:50]}...")
                result = self.test_model_response(model, prompt)
                model_results["tests"].append({
                    "prompt": prompt,
                    "result": result
                })
            
            # Calculate summary statistics
            successful_tests = [t for t in model_results["tests"] if t["result"]["success"]]
            response_times = [t["result"]["response_time"] for t in successful_tests]
            
            model_results["summary"] = {
                "total_tests": len(test_prompts),
                "successful_tests": len(successful_tests),
                "success_rate": len(successful_tests) / len(test_prompts) * 100,
                "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                "min_response_time": min(response_times) if response_times else 0,
                "max_response_time": max(response_times) if response_times else 0
            }
            
            test_results[model_id] = model_results
            
            # Add delay to avoid rate limiting
            time.sleep(1)
        
        # Update model status
        self.update_model_status(test_results)
        
        return test_results
    
    def update_model_status(self, test_results: Dict):
        """Update model health status based on test results"""
        current_status = self.load_model_status()
        
        for model_id, results in test_results.items():
            summary = results["summary"]
            model_name = results["model_name"]
            
            # Determine health status
            if summary["success_rate"] >= 95:
                status = "healthy"
            elif summary["success_rate"] >= 80:
                status = "degraded" 
            else:
                status = "unhealthy"
            
            # Update or create status entry
            current_status[model_name] = {
                "status": status,
                "last_test": datetime.now().isoformat(),
                "success_rate": summary["success_rate"],
                "avg_response_time": summary["avg_response_time"],
                "min_response_time": summary["min_response_time"],
                "max_response_time": summary["max_response_time"],
                "total_tests": summary["total_tests"],
                "successful_tests": summary["successful_tests"],
                "notes": self.generate_status_notes(summary, status)
            }
        
        self.save_model_status(current_status)
        print(f"✅ Model status updated for {len(current_status)} models")
    
    def generate_status_notes(self, summary: Dict, status: str) -> str:
        """Generate notes based on model performance"""
        notes = []
        
        if status == "healthy":
            notes.append("Excellent performance")
        elif status == "degraded":
            notes.append("Some reliability issues")
        else:
            notes.append("Poor performance - avoid use")
        
        if summary["avg_response_time"] > 5:
            notes.append(f"High latency: {summary['avg_response_time']:.1f}s")
        
        if summary["success_rate"] < 90:
            notes.append(f"High failure rate: {100-summary['success_rate']:.1f}%")
        
        return "; ".join(notes)
    
    def generate_report(self, test_results: Dict) -> str:
        """Generate detailed test report"""
        report = []
        report.append("📊 Daily Model Health Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Count models by status
        healthy_count = 0
        degraded_count = 0
        unhealthy_count = 0
        
        for model_id, results in test_results.items():
            summary = results["summary"]
            model_name = results["model_name"]
            
            if summary["success_rate"] >= 95:
                healthy_count += 1
            elif summary["success_rate"] >= 80:
                degraded_count += 1
            else:
                unhealthy_count += 1
        
        report.append(f"📈 SUMMARY:")
        report.append(f"  ✅ Healthy: {healthy_count} models")
        report.append(f"  ⚠️  Degraded: {degraded_count} models") 
        report.append(f"  ❌ Unhealthy: {unhealthy_count} models")
        report.append("")
        
        # Detailed breakdown
        report.append("🔍 DETAILED RESULTS:")
        for model_id, results in test_results.items():
            summary = results["summary"]
            model_name = results["model_name"]
            
            status_icon = "✅" if summary["success_rate"] >= 95 else "⚠️" if summary["success_rate"] >= 80 else "❌"
            
            report.append(f"{status_icon} {model_name}")
            report.append(f"   Success Rate: {summary['success_rate']:.1f}%")
            report.append(f"   Avg Response: {summary['avg_response_time']:.1f}s")
            report.append(f"   Tests: {summary['successful_tests']}/{summary['total_tests']}")
            report.append("")
        
        return "\n".join(report)
    
    def send_notification(self, report: str):
        """Send test results via email (optional)"""
        # This would be configured with actual email settings
        print("📧 Email notification would be sent here")
        print("Report preview:")
        print(report[:500] + "..." if len(report) > 500 else report)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Daily OpenRouter model tester")
    parser.add_argument("--check-all", action="store_true", help="Run tests on all models")
    parser.add_argument("--status", action="store_true", help="Show current model status")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Report format")
    parser.add_argument("--model", help="Test specific model only")
    
    args = parser.parse_args()
    
    tester = ModelTester()
    
    if args.status:
        status = tester.load_model_status()
        print("Current Model Status:")
        for model_name, info in status.items():
            status_icon = "✅" if info["status"] == "healthy" else "⚠️" if info["status"] == "degraded" else "❌"
            print(f"{status_icon} {model_name}: {info['status']} ({info['success_rate']:.1f}% success)")
        return
    
    if args.check_all:
        results = tester.run_daily_tests()
        
        if args.report:
            report = tester.generate_report(results)
            
            if args.format == "json":
                report_json = {
                    "timestamp": datetime.now().isoformat(),
                    "summary": {
                        "total_models": len(results),
                        "healthy": sum(1 for r in results.values() if r["summary"]["success_rate"] >= 95),
                        "degraded": sum(1 for r in results.values() if 80 <= r["summary"]["success_rate"] < 95),
                        "unhealthy": sum(1 for r in results.values() if r["summary"]["success_rate"] < 80)
                    },
                    "detailed_results": results
                }
                print(json.dumps(report_json, indent=2))
            else:
                print(report)
                tester.send_notification(report)
        
        return
    
    if args.model:
        # Test specific model
        models = tester.get_openrouter_models()
        target_model = next((m for m in models if m.get("id") == args.model), None)
        
        if target_model:
            result = tester.test_model_response(target_model, "Hello, test prompt")
            print(f"Test result for {target_model['name']}:")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Response time: {result['response_time']:.2f}s")
                print(f"  Content length: {result['content_length']}")
            else:
                print(f"  Error: {result['error']}")
        else:
            print(f"Model {args.model} not found")
        return

if __name__ == '__main__':
    main()