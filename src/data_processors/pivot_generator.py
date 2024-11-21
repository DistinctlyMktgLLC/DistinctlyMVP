import pandas as pd
import numpy as np
from pathlib import Path

class PivotGenerator:
    def __init__(self, df):
        """
        Initialize PivotGenerator with a pandas DataFrame
        Args:
            df (pd.DataFrame): Input DataFrame with PeopleFindR data
        """
        self.df = df
        self.pivot_path = Path('Data/pivots')
        self.pivot_path.mkdir(parents=True, exist_ok=True)
        
        # Clean up Income Level data - handle 'Prefer not to say'
        self.df['Income Level'] = self.df['Income Level'].fillna('Not Specified')
    
    def create_behavioral_pivot(self):
        """Creates behavioral insights pivot focused on decision-making patterns"""
        behavioral_columns = [
            'Do first impressions tend to stick with you for a long time',
            'Does your mood ever color the way you make decisions',
            'If somethings all the rage are you more likely to give it a go',
            'Do friends recommendations sway your choices a lot'
        ]
        
        try:
            pivot = pd.pivot_table(
                self.df,
                index=['Distinctly Segment Name'],
                values=behavioral_columns + ['Score'],
                aggfunc={
                    **{col: 'count' for col in behavioral_columns},
                    'Score': 'mean'
                }
            ).round(2)
            
            filepath = self.pivot_path / "behavioral_insights_pivot.csv"
            pivot.to_csv(filepath)
            print(f"Successfully saved behavioral pivot to {filepath}")
            return pivot
            
        except Exception as e:
            print(f"Error creating behavioral pivot: {str(e)}")
            return None
    
    def create_family_influence_pivot(self):
        """Creates family influence analysis pivot"""
        try:
            # First, create a simplified family influence metric
            family_data = self.df[['How much do your familys opinions weigh in on your decisions', 
                                 'Income Level', 'Score']].copy()
            
            # Ensure we have clean data
            family_data = family_data.dropna(subset=['How much do your familys opinions weigh in on your decisions'])
            
            pivot = pd.pivot_table(
                family_data,
                index=['How much do your familys opinions weigh in on your decisions'],
                columns=['Income Level'],
                values=['Score'],
                aggfunc='mean',
                fill_value=0
            ).round(2)
            
            filepath = self.pivot_path / "family_influence_pivot.csv"
            pivot.to_csv(filepath)
            print(f"Successfully saved family influence pivot to {filepath}")
            return pivot
            
        except Exception as e:
            print(f"Error creating family influence pivot: {str(e)}")
            print(f"Available columns: {self.df.columns.tolist()}")
            return None

    def create_geographical_pivot(self):
        """Creates geographical analysis pivot"""
        try:
            # Create a numeric score for geographical analysis
            geo_data = self.df[['State', 'Score', 'Value']].copy()
            
            # Ensure numeric values
            geo_data['Score'] = pd.to_numeric(geo_data['Score'], errors='coerce')
            geo_data['Value'] = pd.to_numeric(geo_data['Value'], errors='coerce')
            
            pivot = pd.pivot_table(
                geo_data,
                index=['State'],
                values=['Score', 'Value'],
                aggfunc={
                    'Score': 'mean',
                    'Value': 'sum'
                }
            ).round(2)
            
            filepath = self.pivot_path / "geographical_pivot.csv"
            pivot.to_csv(filepath)
            print(f"Successfully saved geographical pivot to {filepath}")
            return pivot
            
        except Exception as e:
            print(f"Error creating geographical pivot: {str(e)}")
            print(f"Data types: {geo_data.dtypes}")
            return None

    def generate_all_pivots(self):
        """
        Generate all pivot tables and save them to files
        Returns:
            dict: Dictionary containing all generated pivots
        """
        pivots = {}
        
        # Generate each pivot
        pivots['behavioral'] = self.create_behavioral_pivot()
        pivots['family'] = self.create_family_influence_pivot()
        pivots['geographical'] = self.create_geographical_pivot()
        
        return pivots

# Helper function to initialize the system
def initialize_pivot_system(df):
    """
    Initialize the pivot system with data
    Args:
        df (pd.DataFrame): Input DataFrame
    Returns:
        dict: Generated pivots
    """
    generator = PivotGenerator(df)
    return generator.generate_all_pivots()