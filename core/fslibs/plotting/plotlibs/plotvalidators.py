from core.fslibs import Logger

log = Logger.FarseerLogger(__name__).setup_log()


def validate_config(ref, target, name="some config"):
    """
    Validate config dictionary for DeltaPRE Heat Map Plot template.
    
    Loops over config keys and checks if values' type are the
    expected. Raises ValueError otherwise.
    
    Parameters
    ----------
    ref : dict
        The reference configuration dictionary.
    
    target : dict
        The target configuration dictionary.
    
    name : str, optional
        The name of the dict for Error identification.
    """
    
    def eval_types(key, value):
        
        a = type(target[key])
        b = type(value)
        
        if not(a == b):
            msg = (
                f"Argument '{key}' in {name} Plot is not of "
                f"correct type, is {a}, should be {b}."
                )
            log.info(msg)
            raise TypeError(msg)
    
    for key, value in ref.items():
        eval_types(key, value)
    
    msg = f"Parameters type for {name} evaluated successfully"
    log.debug(msg)
    
    return


def validate_shapes(reference, target_tuple):
    
    if target_tuple[1].shape != reference.shape:
        raise ValueError(
            f"Shape of {target_tuple[0]} ({target_tuple[1].shape}) differs "
            f"from reference shape ({reference.shape})"
            )
    

def validate_len(reference, target_tuple):
    """
    Validates len of args against len of reference.
    """
    
    if len(target_tuple[1]) != len(reference):
        raise ValueError(
            f"Length of '{target_tuple[0]}' parameter ({len(target_tuple[1])})"
            f" differs from reference length ({len(reference)})"
            )
