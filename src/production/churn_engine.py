"""
HumanChurnML - Production Engine
Convert your Jupyter discovery into a reusable system
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

class ChurnEngine:
    """
    Universal churn prediction that works for ANY business
    Based on real patterns discovered from 190,000+ customers
    """
    
    def __init__(self, company_name="", industry="unknown"):
        self.company_name = company_name
        self.industry = industry
        self.patterns = self._load_patterns()
        print(f"✅ HumanChurnML Engine Initialized")
        print(f"   Company: {company_name}")
        print(f"   Industry: {industry}")
        print(f"   Knowledge from: {self.patterns['universal']['total_customers_analyzed']:,} customers")
    
    def _load_patterns(self):
        """Load the universal patterns from JSON"""
        json_path = 'models/universal_patterns.json'
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                return json.load(f)['discovered_patterns']
        else:
            print("⚠️  Patterns file not found, using defaults")
            return self._default_patterns()
    
    def _default_patterns(self):
        """Fallback patterns if JSON not found"""
        return {
            'gaming': {
                'Tried Once': {'retention_7day': 0.02},
                'Casual': {'retention_7day': 0.18},
                'Regular': {'retention_7day': 0.47},
                'Hardcore': {'retention_7day': 0.70},
                'Obsessed': {'retention_7day': 0.84}
            },
            'ecommerce': {
                'Tried Once': {'avg_spend': 160.99},
                'Casual': {'avg_spend': 245.67},
                'Regular': {'avg_spend': 389.45},
                'Loyal': {'avg_spend': 512.33},
                'Super Customer': {'avg_spend': 629.78}
            },
            'universal': {
                'engagement_multiplier': 3.9,
                'total_customers_analyzed': 189630
            }
        }
    
    def analyze_customers(self, customer_data, activity_data):
        """
        Main function - analyze any customer dataset
        
        Parameters:
        - customer_data: DataFrame with customer info (must have 'customer_id')
        - activity_data: DataFrame with user actions (must have 'customer_id' and 'timestamp')
        
        Returns:
        - DataFrame with risk scores and recommendations
        """
        
        # Step 1: Calculate engagement metrics
        print("📊 Calculating engagement metrics...")
        engagement = self._calculate_engagement(customer_data, activity_data)
        
        # Step 2: Assign engagement levels
        engagement = self._assign_levels(engagement)
        
        # Step 3: Calculate churn risk
        engagement['churn_risk'] = self._calculate_risk(engagement)
        
        # Step 4: Recommend actions
        engagement['recommended_action'] = engagement.apply(
            lambda x: self._recommend_action(x), axis=1
        )
        
        # Step 5: Predict customer value
        engagement['predicted_ltv'] = engagement.apply(
            lambda x: self._predict_ltv(x), axis=1
        )
        
        # Step 6: Flag urgent cases
        engagement['urgent'] = engagement['churn_risk'] > 70
        
        print(f"✅ Analysis complete for {len(engagement)} customers")
        
        return engagement
    
    def _calculate_engagement(self, customers, activities):
        """Extract universal engagement metrics from raw data"""
        
        # Handle empty activities
        if len(activities) == 0:
            return pd.DataFrame({
                'customer_id': customers['customer_id'],
                'total_activities': 0,
                'active_days': 0,
                'recency_days': 999,
                'frequency_trend': 'unknown'
            })
        
        # Convert timestamp if needed
        if 'timestamp' in activities.columns:
            activities['date'] = pd.to_datetime(activities['timestamp'])
        elif 'date' in activities.columns:
            activities['date'] = pd.to_datetime(activities['date'])
        else:
            # Create dummy date
            activities['date'] = datetime.now()
        
        # Calculate metrics per customer
        results = []
        
        for cust_id in customers['customer_id'].unique():
            cust_activities = activities[activities['customer_id'] == cust_id]
            
            if len(cust_activities) > 0:
                # Calculate metrics
                metrics = {
                    'customer_id': cust_id,
                    'total_activities': len(cust_activities),
                    'active_days': cust_activities['date'].nunique(),
                    'recency_days': (datetime.now() - cust_activities['date'].max()).days,
                    'frequency_trend': self._calculate_trend(cust_activities)
                }
                
                # Calculate average session length if available
                if 'duration' in cust_activities.columns:
                    metrics['avg_duration'] = cust_activities['duration'].mean()
                else:
                    metrics['avg_duration'] = 0
                
                # Calculate total value if available
                if 'value' in cust_activities.columns:
                    metrics['total_value'] = cust_activities['value'].sum()
                else:
                    metrics['total_value'] = 0
            else:
                # No activities
                metrics = {
                    'customer_id': cust_id,
                    'total_activities': 0,
                    'active_days': 0,
                    'recency_days': 999,
                    'frequency_trend': 'inactive',
                    'avg_duration': 0,
                    'total_value': 0
                }
            
            results.append(metrics)
        
        return pd.DataFrame(results)
    
    def _calculate_trend(self, activities):
        """Detect if engagement is increasing or decreasing"""
        if len(activities) < 3:
            return 'stable'
        
        # Sort by date
        activities = activities.sort_values('date')
        
        # Compare recent vs old
        recent_count = activities.tail(3)['date'].nunique()
        old_count = activities.head(3)['date'].nunique()
        
        if recent_count < old_count * 0.5:
            return 'decreasing'
        elif recent_count > old_count * 1.5:
            return 'increasing'
        else:
            return 'stable'
    
    def _assign_levels(self, df):
        """Assign universal engagement levels"""
        conditions = [
            df['total_activities'] == 0,
            df['total_activities'] == 1,
            df['total_activities'] == 2,
            df['total_activities'] <= 4,
            df['total_activities'] <= 8,
            df['total_activities'] > 8
        ]
        choices = [
            'Never Active',
            'Tried Once',
            'Casual',
            'Regular',
            'Loyal',
            'Super Customer'
        ]
        
        df['engagement_level'] = np.select(conditions, choices, default='Unknown')
        return df
    
    def _calculate_risk(self, df):
        """Calculate churn risk score 0-100"""
        risk = 50  # Base risk
        
        # Risk by engagement level
        level_risk = {
            'Never Active': 95,
            'Tried Once': 80,
            'Casual': 60,
            'Regular': 40,
            'Loyal': 20,
            'Super Customer': 10
        }
        
        risk = df['engagement_level'].map(level_risk).fillna(50)
        
        # Add recency penalty
        risk = risk + (df['recency_days'] * 0.5)
        
        # Add trend penalty
        trend_penalty = df['frequency_trend'].map({
            'decreasing': 15,
            'stable': 0,
            'increasing': -10,
            'inactive': 20,
            'unknown': 0
        }).fillna(0)
        
        risk = risk + trend_penalty
        
        # Cap at 0-100
        return np.clip(risk, 0, 100)
    
    def _recommend_action(self, customer):
        """Recommend what to do with this customer"""
        
        risk = customer['churn_risk']
        level = customer['engagement_level']
        
        if risk > 85:
            return "🚨 URGENT: Personal phone call + 30% discount"
        elif risk > 70:
            return "⚠️ HIGH: Send personal email from CEO + 20% off"
        elif risk > 50:
            return "📧 MEDIUM: Re-engagement campaign with new features"
        elif risk > 30:
            return "📱 LOW: Regular newsletter + product recommendations"
        elif level == 'Super Customer':
            return "🌟 VIP: Ask for referral + early access to new products"
        else:
            return "✅ ON TRACK: Continue regular engagement"
    
    def _predict_ltv(self, customer):
        """Predict customer lifetime value"""
        level = customer['engagement_level']
        
        # Default values by level
        level_values = {
            'Never Active': 0,
            'Tried Once': 160,
            'Casual': 250,
            'Regular': 390,
            'Loyal': 510,
            'Super Customer': 630
        }
        
        base_value = level_values.get(level, 100)
        
        # Adjust based on risk (higher risk = lower remaining value)
        risk_factor = (100 - customer['churn_risk']) / 100
        
        return round(base_value * risk_factor, 2)
    
    def get_summary_stats(self, analysis_df):
        """Generate summary statistics for business users"""
        
        stats = {
            'total_customers': len(analysis_df),
            'at_risk_customers': len(analysis_df[analysis_df['churn_risk'] > 70]),
            'urgent_customers': len(analysis_df[analysis_df['urgent']]),
            'avg_risk': analysis_df['churn_risk'].mean(),
            'total_predicted_value': analysis_df['predicted_ltv'].sum(),
            'engagement_breakdown': analysis_df['engagement_level'].value_counts().to_dict()
        }
        
        # Calculate potential savings
        stats['potential_savings'] = round(
            stats['at_risk_customers'] * 160 * 0.3,  # 30% of one-time buyer value
            2
        )
        
        return stats
    
    def export_for_crm(self, analysis_df, output_path='exports/crm_upload.csv'):
        """Export in format CRM systems can import"""
        
        export_df = analysis_df[[
            'customer_id', 
            'engagement_level', 
            'churn_risk', 
            'recommended_action',
            'urgent'
        ]].copy()
        
        # Create CRM-friendly format
        export_df['status'] = export_df.apply(
            lambda x: 'URGENT' if x['urgent'] else x['engagement_level'],
            axis=1
        )
        
        export_df['next_action_date'] = datetime.now() + timedelta(days=1)
        export_df['campaign'] = export_df['recommended_action'].apply(
            lambda x: x.split(':')[0] if ':' in x else 'General'
        )
        
        # Save
        os.makedirs('exports', exist_ok=True)
        export_df.to_csv(output_path, index=False)
        print(f"✅ CRM export saved to {output_path}")
        
        return export_df


# Quick test
if __name__ == "__main__":
    # Test with sample data
    engine = ChurnEngine(company_name="TestCo", industry="ecommerce")
    
    # Create sample customers
    sample_customers = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005']
    })
    
    # Create sample activities
    sample_activities = pd.DataFrame({
        'customer_id': ['C001', 'C001', 'C002', 'C003', 'C003', 'C003'],
        'date': [
            '2024-03-01', '2024-03-15',  # C001 - casual
            '2024-02-01',                  # C002 - inactive
            '2024-03-01', '2024-03-10', '2024-03-20'  # C003 - active
        ],
        'duration': [10, 5, 20, 15, 25, 30],
        'value': [50, 30, 100, 75, 120, 200]
    })
    
    # Run analysis
    results = engine.analyze_customers(sample_customers, sample_activities)
    
    print("\n📋 RESULTS:")
    print(results[['customer_id', 'engagement_level', 'churn_risk', 'recommended_action']])
    
    print("\n📊 SUMMARY:")
    print(engine.get_summary_stats(results))