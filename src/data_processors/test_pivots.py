import pandas as pd
import os
from pathlib import Path
from pivot_generator import initialize_pivot_system

def test_pivot_generation():
    # Updated path to the correct file
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent.parent
    data_file = root_dir / 'Data' / 'people_data_wave1.csv'
    
    try:
        print(f"Attempting to load data from: {data_file}")
        df = pd.read_csv(data_file)
        print("Data loaded successfully")
        print(f"Loaded {len(df)} rows of data")
        print(f"Columns available: {df.columns.tolist()}")
        
        # Generate pivots
        print("\nGenerating pivots...")
        pivots = initialize_pivot_system(df)
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")

if __name__ == "__main__":
    test_pivot_generation()