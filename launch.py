"""
HumanChurnML Launcher
Run this to start everything
"""

import subprocess
import sys
import os
import time
import webbrowser

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def main():
    print_header("🚀 HumanChurnML - Launch Pad")
    
    print("\nWhat would you like to start?")
    print("1️⃣  Run API (for developers)")
    print("2️⃣  Run Dashboard (for business users)")
    print("3️⃣  Run Both (full system)")
    print("4️⃣  Test Engine (quick test)")
    print("5️⃣  Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        print_header("Starting API Server")
        print("📍 API will be at: http://localhost:5000")
        print("📚 Docs at: http://localhost:5000")
        print("\nPress Ctrl+C to stop\n")
        
        subprocess.run([sys.executable, "api/simple_api.py"])
    
    elif choice == "2":
        print_header("Starting Dashboard")
        print("📍 Dashboard will open in your browser")
        print("\nPress Ctrl+C to stop\n")
        
        # Open browser after a moment
        time.sleep(2)
        webbrowser.open("http://localhost:8501")
        
        subprocess.run(["streamlit", "run", "dashboard/simple_dashboard.py"])
    
    elif choice == "3":
        print_header("Starting Full System")
        
        # Start API in background
        print("📡 Starting API...")
        api_process = subprocess.Popen([sys.executable, "api/simple_api.py"])
        
        # Start dashboard
        print("📊 Starting Dashboard...")
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        subprocess.run(["streamlit", "run", "dashboard/simple_dashboard.py"])
        
        # Cleanup
        api_process.terminate()
    
    elif choice == "4":
        print_header("Testing Engine")
        
        from src.production.churn_engine import ChurnEngine
        
        engine = ChurnEngine(company_name="Test", industry="test")
        
        # Create test data
        import pandas as pd
        customers = pd.DataFrame({'customer_id': ['1', '2', '3']})
        activities = pd.DataFrame({
            'customer_id': ['1', '1', '2'],
            'timestamp': ['2024-03-01', '2024-03-15', '2024-02-01']
        })
        
        results = engine.analyze_customers(customers, activities)
        print("\n✅ Test Results:")
        print(results[['customer_id', 'engagement_level', 'churn_risk']])
    
    elif choice == "5":
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")