#!/usr/bin/env python3

import json
import os
import time
import schedule
import argparse
import sys
from datetime import datetime, timedelta
from model_tester import ModelTester
from router import EnhancedModelRouter

class ModelRouterDaemon:
    def __init__(self):
        self.tester = ModelTester()
        self.router = EnhancedModelRouter("models.json")
        self.pid_file = "model_router_daemon.pid"
        self.running = False
    
    def start(self):
        """Start the daemon"""
        print("🚀 Starting Model Router Daemon...")
        
        # Write PID file
        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))
        
        self.running = True
        
        # Schedule daily tests at 4 AM
        schedule.every().day.at("04:00").do(self.run_daily_tests)
        
        # Schedule hourly status checks
        schedule.every().hour.do(self.check_model_status)
        
        # Schedule cost optimization report at 9 PM
        schedule.every().day.at("21:00").do(self.generate_cost_report)
        
        print(f"✅ Daemon started (PID: {os.getpid()})")
        print(f"📅 Daily tests scheduled for 04:00")
        print(f"📊 Hourly status checks active")
        print(f"💰 Cost reports scheduled for 21:00")
        
        # Run initial test
        self.run_daily_tests()
        
        # Keep daemon running
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop(self):
        """Stop the daemon"""
        print("🛑 Stopping daemon...")
        self.running = False
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
        print("✅ Daemon stopped")
    
    def run_daily_tests(self):
        """Run daily model health tests"""
        print(f"🧪 Running daily model tests at {datetime.now()}")
        
        try:
            results = self.tester.run_daily_tests()
            report = self.tester.generate_report(results)
            
            # Save report
            report_file = f"model_test_report_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(report_file, "w") as f:
                f.write(report)
            
            print(f"✅ Daily tests completed. Report saved to {report_file}")
            
            # Send notification if configured
            self.tester.send_notification(report)
            
        except Exception as e:
            print(f"❌ Daily tests failed: {e}")
    
    def check_model_status(self):
        """Check current model status"""
        try:
            status = self.router.load_model_status()
            
            # Count models by status
            healthy = sum(1 for s in status.values() if s["status"] == "healthy")
            degraded = sum(1 for s in status.values() if s["status"] == "degraded")
            unhealthy = sum(1 for s in status.values() if s["status"] == "unhealthy")
            
            if degraded > 0 or unhealthy > 0:
                print(f"⚠️ Model Status Alert: {healthy} healthy, {degraded} degraded, {unhealthy} unhealthy")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
    
    def generate_cost_report(self):
        """Generate daily cost optimization report"""
        print(f"💰 Generating cost optimization report at {datetime.now()}")
        
        try:
            # This would track actual usage and costs
            report = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": {
                    "total_requests": 0,  # Would track actual usage
                    "free_model_usage": 0,
                    "paid_model_usage": 0,
                    "estimated_cost": 0.00
                },
                "recommendations": [
                    "Continue using free models for simple tasks",
                    "Consider setting up approval workflow for paid models",
                    "Monitor response times for cost optimization"
                ]
            }
            
            # Save report
            report_file = f"cost_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Cost report saved to {report_file}")
            
        except Exception as e:
            print(f"❌ Cost report generation failed: {e}")
    
    def get_status(self):
        """Get daemon status"""
        try:
            status = self.router.load_model_status()
            
            return {
                "daemon_running": self.running,
                "pid_file_exists": os.path.exists(self.pid_file),
                "total_models": len(status),
                "healthy_models": sum(1 for s in status.values() if s["status"] == "healthy"),
                "degraded_models": sum(1 for s in status.values() if s["status"] == "degraded"),
                "unhealthy_models": sum(1 for s in status.values() if s["status"] == "unhealthy"),
                "last_test": max((s["last_test"] for s in status.values()), default=None)
            }
        except Exception as e:
            return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Model Router Daemon")
    parser.add_argument("--start", action="store_true", help="Start the daemon")
    parser.add_argument("--stop", action="store_true", help="Stop the daemon")
    parser.add_argument("--status", action="store_true", help="Show daemon status")
    parser.add_argument("--run-tests", action="store_true", help="Run manual tests")
    
    args = parser.parse_args()
    
    daemon = ModelRouterDaemon()
    
    if args.start:
        daemon.start()
    elif args.stop:
        daemon.stop()
    elif args.status:
        status = daemon.get_status()
        print("Daemon Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    elif args.run_tests:
        daemon.run_daily_tests()
    else:
        print("Use --start, --stop, --status, or --run-tests")

if __name__ == '__main__':
    main()