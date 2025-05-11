import os
from pathlib import Path
from utils.r_data_converter import convert_r_data_to_python

def convert_all_r_data():
    """
    Convert all R data files to Python format
    """
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Get all R data files
    r_data_dir = Path("../R")
    r_data_files = list(r_data_dir.glob("*.rda"))
    
    for r_file in r_data_files:
        # Create output path
        output_file = data_dir / f"{r_file.stem}.pkl"
        
        # Convert file
        print(f"Converting {r_file.name} to {output_file.name}...")
        success = convert_r_data_to_python(str(r_file), str(output_file))
        
        if success:
            print(f"Successfully converted {r_file.name}")
        else:
            print(f"Failed to convert {r_file.name}")

if __name__ == "__main__":
    convert_all_r_data() 