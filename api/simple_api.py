"""
Simple API for HumanChurnML
Run with: python simple_api.py
"""

from flask import Flask, request, jsonify
import pandas as pd
import sys
sys.path.append('..')
from src.production.churn_engine import ChurnEngine
import json

app = Flask(__name__)

# Initialize engine
engine = ChurnEngine(company_name="API User", industry="unknown")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "HumanChurnML API",
        "version": "1.0",
        "endpoints": {
            "/predict": "POST - Send customer data for predictions",
            "/health": "GET - Check if API is running",
            "/stats": "GET - Get model statistics"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model": "loaded"})

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "customers_analyzed": engine.patterns['universal']['total_customers_analyzed'],
        "industries": engine.patterns['universal']['industries_covered'],
        "multiplier": engine.patterns['universal']['engagement_multiplier']
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects JSON with:
    {
        "customers": [{"customer_id": "123"}, ...],
        "activities": [{"customer_id": "123", "timestamp": "2024-03-19", "duration": 10}, ...]
    }
    """
    try:
        data = request.get_json()
        
        # Convert to DataFrames
        customers_df = pd.DataFrame(data['customers'])
        activities_df = pd.DataFrame(data['activities'])
        
        # Run analysis
        results = engine.analyze_customers(customers_df, activities_df)
        
        # Convert to JSON-friendly format
        output = results.to_dict(orient='records')
        
        return jsonify({
            "success": True,
            "results": output,
            "summary": engine.get_summary_stats(results)
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting HumanChurnML API...")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000)