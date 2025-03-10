"""Example module in subpackage."""


def example_function(param1: str, param2: int) -> bool:
    """Example function with Google-style docstring.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Boolean result
        
    Raises:
        ValueError: When parameters are invalid
    """
    if not param1 or param2 < 0:
        raise ValueError("Invalid parameters")
    return True
