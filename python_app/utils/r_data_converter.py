import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

def convert_r_data_to_python(r_data_path, output_path):
    """
    Convert R data files to Python pickle format using rpy2
    """
    try:
        # Load R data file
        robjects.r['load'](r_data_path)
        
        # Get the first object from the R environment
        r_data = robjects.globalenv[robjects.globalenv.keys()[0]]
        
        # Convert to pandas DataFrame
        with localconverter(robjects.default_converter + pandas2ri.converter):
            df = robjects.conversion.rpy2py(r_data)
        
        # Save as pickle
        with open(output_path, 'wb') as f:
            pickle.dump(df, f)
            
        return True
    except Exception as e:
        print(f"Error converting R data: {str(e)}")
        return False

def load_python_data(data_path):
    """
    Load Python pickle data
    """
    try:
        with open(data_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading Python data: {str(e)}")
        return None 