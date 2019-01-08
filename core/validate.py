"""
Module with general functions that can be used to validate input,
    data, parameters, etc...
"""

def validate_types(xt):
    if not(isinstance(xt[0], xt[1])) : 
            raise ValueError(f"{xt[0]} not of type {xt[1]}")
