import numpy as np
from math import ceil

from core import validate
from core.fslibs import Logger

log = Logger.FarseerLogger(__name__).setup_log()


def plot_threshold(
        ax,
        values,
        std=5,
        orientation='horizontal',
        threshold_color="red",
        threshold_linewidth=0.5,
        threshold_alpha=0.8,
        threshold_zorder=10,
        **kwargs,
        ):
    """
    Plots threshold line that identifies relevant perturnations.
    
    Parameters
    ----------
     ax : element of :obj:`matplotlib.pyplot.axes`
    
    values : np.ndarray
        Values to evaluate.
        
    std : int
        Standard deviation multiplier
    
    orientation : ['horizontal', 'vertical'], optional
        Wheter plotting in a vertical or horizontal plot.
        Defaults to 'horizontal'
    
    threshold_color :str
        Line color. Defaults to "red".
    
    threshold_linewidth : float
        Line width. Defaults to "0.5".
    
    threshold_alpha : float [0-1]
        Line's transparency.
    
    threshold_zorder : int
        The matplotlib zorder for the plot.
    """
    sorted_values = np.copy(np.sort(np.absolute(values)))
    parsed_values = sorted_values[np.logical_not(np.isnan(sorted_values))]
    firstdecile = parsed_values[0:ceil(0.1*len(parsed_values))]
    threshold = np.mean(firstdecile) + std*np.std(firstdecile)
    
    log.debug("Threshold defined: {}".format(threshold))
    
    line_details = {
        "color": threshold_color,
        "linewidth": threshold_linewidth,
        "alpha": threshold_alpha,
        "zorder": threshold_zorder,
        }
        
    if orientation == 'horizontal':
        ax.axhline(
            y=threshold,
            **line_details,
            )
        # in case there are negative numbers, plots the threshold,
        # if there are not negative numbers, this line is never displayed
        ax.axhline(
            y=-threshold,
            **line_details,
            )
    
    elif orientation == 'vertical':
        ax.axvline(
            x=threshold,
            **line_details,
            )
        # in case there are negative numbers, plots the threshold,
        # if there are not negative numbers, this line is never displayed
        ax.axvline(
            x=-threshold,
            **line_details,
            )
    
    return


