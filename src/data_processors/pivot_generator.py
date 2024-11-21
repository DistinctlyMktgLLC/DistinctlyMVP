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
        self.pivot_path = Path('data/pivots')
        self.pivot_path.mkdir(parents=True, exist_ok=True)
    
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
            
            # Save pivot
            filepath = self.pivot_path / "behavioral_insights_pivot.csv"
            pivot.to_csv(filepath)
            return pivot
            
        except Exception as e:
            print(f"Error creating behavioral pivot: {str(e)}")
            return None
    
    def create_family_influence_pivot(self):
        """Creates family influence analysis pivot"""
        try:
            pivot = pd.pivot_table(
                self.df,
                index=['How much do your familys opinions weigh in on your decisions'],
                columns=['Income Level'],
                values=['Score'],
                aggfunc='mean'
            ).round(2)
            
            filepath = self.pivot_path / "family_influence_pivot.csv"
            pivot.to_csv(filepath)
            return pivot
            
        except Exception as e:
            print(f"Error creating family influence pivot: {str(e)}")
            return None

    def create_geographical_pivot(self):
        """Creates geographical analysis pivot"""
        try:
            pivot = pd.pivot_table(
                self.df,
                index=['State'],
                values=['Score', 'Value'],
                aggfunc={
                    'Score': 'mean',
                    'Value': 'mean'
                }
            ).round(2)
            
            filepath = self.pivot_path / "geographical_pivot.csv"
            pivot.to_csv(filepath)
            return pivot
            
        except Exception as e:
            print(f"Error creating geographical pivot: {str(e)}")
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