import pandas as pd
import os
from pathlib import Path
from pivot_generator import initialize_pivot_system

def test_pivot_generation():
    # Get the correct path to data file
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent.parent
    data_file = root_dir / 'Data' / 'Enchiridion - people.csv'
    
    try:
        print(f"Attempting to load data from: {data_file}")
        df = pd.read_csv(data_file)
        print("Data loaded successfully")
        print(f"Loaded {len(df)} rows of data")
        print(f"Columns available: {df.columns.tolist()}")
        
        # Generate pivots
        print("\nGenerating pivots...")
        pivots = initialize_pivot_system(df)
        
        # Check results
        print("\nPivot Generation Results:")
        for name, pivot in pivots.items():
            if pivot is not None:
                print(f"{name} pivot generated successfully with shape {pivot.shape}")
            else:
                print(f"Failed to generate {name} pivot")
                
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir(root_dir / 'Data')}")

if __name__ == "__main__":
    test_pivot_generation()