# MOVE HELPER FUNCTIONS FROM TEST_PYNUMERICS HERE

import pandas as pd
import math
from System import Array, Double

"""
Helper functions to compare Numerics results to Python package results.
Authors:
     Sadie Niblett, USACE Risk Management Center, sadie.s.niblett@usace.army.mil
"""

def convert_to_dotnet_array(pythonList):
    """
    Helper function to convert a Python list to a .NET array of doubles.
    Args:
        python_list: Python list of float values
    """
    dotnetArray = Array.CreateInstance(float, len(pythonList))
    for i, val in enumerate(pythonList):
        dotnetArray[i] = float(val)
    return dotnetArray

def convert_to_dotnet_2d_array(matrix):
    """Convert NumPy matrix to .NET 2D array.
    Args:
        matrix: 2D NumPy array"""
    rows, cols = matrix.shape
    net_array = Array.CreateInstance(Double, rows, cols)
    for i in range(rows):
        for j in range(cols):
            net_array[i, j] = float(matrix[i, j])
    return net_array
    
def assert_within_tolerance_pct(expected, actual, names, tolerancePct=0.05):
    """
    Helper function to assert that actual values is within a certain percentage tolerance of expected values.
    Args:
        expected: List of expected values (floats)
        actual: List of actual values (floats)
        name: List of names of the statistic being tested (for error message)
        tolerance_pct: Tolerance percentage (default 0.05 for 5%)
    """
    for i in range(len(expected)):
        tolerance = abs(expected[i] * tolerancePct)

        if abs(actual[i] - expected[i]) > tolerance:
            raise AssertionError(
                f"{names[i]}: Expected {expected[i]} ± {tolerance}, got {actual[i]}"
                )

def assert_within_tolerance(expected, actual, names, tolerance=0.05):
    """
    Helper function to assert that actual values is within a certain tolerance of expected values.
    Args:
        expected: List of expected values (floats)
        actual: List of actual values (floats)
        name: List of names of the statistic being tested (for error message)
        tolerance: Tolerance  (default 0.05)
    """
    for i in range(len(expected)):
        if abs(actual[i] - expected[i]) > tolerance:
            raise AssertionError(
                f"{names[i]}: Expected {expected[i]} ± {tolerance}, got {actual[i]}"
                )

def assert_within_tolerance_singular(expected, actual, name, tolerance=0.05):
    """
    Helper function to assert that actual value is within a certain tolerance of expected value.
    Args:
        expected: Expected value (float)
        actual: Actual value (float)
        name: Name of the statistic being tested (for error message)
        tolerance: Tolerance  (default 0.05)
    """
    if abs(actual - expected) > tolerance:
         raise AssertionError(
            f"{name}: Expected {expected} ± {tolerance}, got {actual}"
            )

def create_comparison_table(numericsResults, comparisonPackage, comparisonResults, parameterNames, numericsTime=float('nan'), comparisonTime=float('nan') ):
    """
    Helper function to create a comparison table between Numerics and comparison package results.
    Args:
        numericsResults: Array of results from Numerics
        comparisonPackage: Name of comparison package (for table formating)
        comparisonResults: Array of results from comparison package
        parameterNames: List of parameter names
        numericsTime: Execution time for Numerics (default nan for hard coded numerical tests)
        comparisonTime: Execution time for comparison package (default nan for hard coded numerical tests)
    Returns: 
        pandas DataFrame with comparison results
    """
    table = []
    for i, paramName in enumerate(parameterNames):
        pct_diff = ((numericsResults[i] - comparisonResults[i]) / comparisonResults[i] * 100) if comparisonResults[i] != 0 else 0
        table.append({'Parameter': paramName,
                        'Numerics Result': numericsResults[i],
                        f'{comparisonPackage} Result': comparisonResults[i],
                        'Difference': f'{pct_diff:.4f}%'
                        })

    if not math.isnan(numericsTime) and not math.isnan(comparisonTime):
        timeDiff = (numericsTime - comparisonTime) if comparisonTime != 0 else 0 
        table.append({'Parameter': 'Runtime (secs)',
                    'Numerics Result': f'{numericsTime:.4f}',
                    f'{comparisonPackage} Result': f'{comparisonTime:.4f}',
                    'Difference': f'{timeDiff:.4f}'
                    })

    df = pd.DataFrame(table)
    return df

def create_singular_comparison(numericsResult, comparisonPackage, comparisonResult, parameterName, numericsTime=float('nan'), comparisonTime=float('nan') ):
    """
    Helper function to create a singular comparison table between Numerics and comparison package results.
    Args:
        numericsResult: Result from Numerics
        comparisonPackage: Name of comparison package (for table formating)
        comparisonResult: Result from comparison package
        parameterName: Name of parameter
        numericsTime: Execution time for Numerics (default nan for hard coded numerical tests)
        comparisonTime: Execution time for comparison package (default nan for hard coded numerical tests) 
    Returns:
        pandas DataFrame with comparison results
        """
    pct_diff = ((numericsResult - comparisonResult) / comparisonResult * 100) if comparisonResult != 0 else 0
    table = [{'Parameter': parameterName,
                'Numerics Result': numericsResult,
                f'{comparisonPackage} Result': comparisonResult,
                'Difference': f'{pct_diff:.4f}%'
                }]
    if not math.isnan(numericsTime) and not math.isnan(comparisonTime):
        timeDiff = (numericsTime - comparisonTime) if comparisonTime != 0 else 0 
        table.append({'Parameter': 'Runtime (secs)',
                    'Numerics Result': f'{numericsTime:.4f}',
                    f'{comparisonPackage} Result': f'{comparisonTime:.4f}',
                    'Difference': f'{timeDiff:.4f}'
                    })
    df = pd.DataFrame(table)
    return df