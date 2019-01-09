"""
Module with general functions that can be used to validate input,
    data, parameters, etc...
"""

def validate_types(xt):
    """
    Validates types. Raises TypeError if types are different
    from expected.
    
    Parameters
    ----------
    xt : tuple, list
        xt[0] : str, The name of the variable to report on Error
        xt[1] : :obj:, The variable itself
        xt[2] : :obj:, The expected type
    """
    if not(isinstance(xt[1], xt[2])): 
            raise TypeError(
                f"Parameter '{xt[0]}' not of type {xt[2]},"
                f" is {type(xt[1])}"
                )
