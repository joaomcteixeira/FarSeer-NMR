

def validate_barplot_data(values, labels):
    
    if len(labels) != values.shape[1] : raise ValueError(
            "Length of labels do not match the length of values (ydata)"
            )
    
    return


def validate_barplot_additional_data(values, **kwargs):
    """
    Validates Bar Plot related additional data against input values.
    
    If validations fail, Exception raises accordingly.
    
    Parameters
    ----------
    values : np.ndarray shape (y,x), dtype=float
        where X (axis=1) is the data to plot for each column,
        Y (axis=0) is the evolution of that data along the titration.
    
    **kwargs,
        Available validations:
            - checks type is np.ndarray, and shape == value.shape
                "peak_status",
                "details",
                "tag_position",
                "theo_pre",
            
            - checks if length == values.shape[1]
                "suptitles",
                "letter_code",
    """

    def check_shape(x):
        
        if kwargs[x] is None : return
        
        if not(isinstance(kwargs[x], np.ndarray)) : raise TypeError(
            f"Argument {x} is not of REQUIRED type numpy.ndarray"
            )
        
        if kwargs[x].shape != values.shape : raise ValueError(
            f"Shape of {x} ({kwargs[x].shape}) differs "
            f"from values shape ({values.shape})"
            )
    
    def check_len(x):
        
        if kwargs[x] is None: return
        
        if len(kwargs[x]) != values.shape[0] : raise ValueError(
            f"Length of {x} ({len(kwargs[x])}) differs "
            f"from values shape ({values.shape[1]})"
            )
    
    seq_params_to_evaluate = [
        "suptitles",
        "letter_code",
        ]
    
    array_params_to_evaluate = [
        "peak_status",
        "details",
        "tag_position",
        "theo_pre",
        ]
    
    list(map(check_len, seq_params_to_evaluate))
    list(map(check_shape, array_params_to_evaluate))
    
    return
