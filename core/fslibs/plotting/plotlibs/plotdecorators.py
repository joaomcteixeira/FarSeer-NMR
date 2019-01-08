from functools import wraps

def check_barplot_args(func):
    """
    Checks arguments passed to parameters common in all Bar Plot
    templates.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
    
        def check_shape(x):
            
            if kwargs[x] is None : return
            
            if not(isinstance(kwargs[x], np.ndarray)) : raise ValueError(
                f"Argument {x} is not of REQUIRED type numpy.ndarray"
                )
            
            if kwargs[x].shape != values.shape : raise AttributeError(
                f"Shape of {x} ({kwargs[x].shape}) differs "
                f"from values shape ({values.shape})"
                )
        
        def check_len(x):
            
            if kwargs[x] is None: return
            
            if len(kwargs[x]) != values.shape[1] : raise AttributeError(
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
        
        if len(labels) != values.shape[1] : raise AttributeError(
            "Length of labels do not match the length of values (ydata)"
            )
        
        list(map(check_len, seq_params_to_evaluate))
        list(map(check_shape, array_params_to_evaluate))
        
        return func(*args, **kwargs)
    
    return wrapper
