import pandas as pd
from pivot_generator import initialize_pivot_system

def test_pivot_generation():
    # Load your data
    try:
        df = pd.read_csv('Data/Enchiridion - people.csv')
        print("Data loaded successfully")
        
        # Generate pivots
        pivots = initialize_pivot_system(df)
        
        # Check results
        for name, pivot in pivots.items():
            if pivot is not None:
                print(f"{name} pivot generated successfully")
            else:
                print(f"Failed to generate {name} pivot")
                
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_pivot_generation()