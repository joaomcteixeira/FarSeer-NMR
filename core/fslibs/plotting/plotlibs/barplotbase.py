import numpy as np
from math import ceil
import inspect

from matplotlib.axes import Axes

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
        ):
    """
    Plots threshold line that identifies relevant perturnations.
    
    Parameters
    ----------
    ax : :obj:`matplotlib.axes.Axes`
    
    values : np.ndarray
        Values to evaluate.
        
    std : int, optional
        Standard deviation multiplier. Defaults to 5.
    
    orientation : ['horizontal', 'vertical'], optional
        Wheter plotting in a vertical or horizontal plot.
        Defaults to 'horizontal'
    
    threshold_color : str, optional
        Line color. Defaults to "red".
    
    threshold_linewidth : float, optional
        Line width. Defaults to "0.5".
    
    threshold_alpha : float [0-1], optional
        Line's transparency. Defaults to 0.8.
    
    threshold_zorder : int
        The matplotlib zorder for the plot.
        Defaults to 10, plots on top of everything.
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

def compacted_bar_xticks(num_of_bars, labels):
    
    try:
        labels.astype(int)
    except ValueError:
        labels_are_int = False
    else:
        labels_are_int = True
    
    if num_of_bars <= 10:
        xticks = np.arange(num_of_bars)
    
    else:
        number_of_ticks = num_of_bars
        mod_ = 10
        sanity_counter = 0
    
        if labels_are_int:
            tmp_labels = labels.astype(int)
            
            while number_of_ticks > 10 and sanity_counter < 100000:
                
                mask = np.where(tmp_labels % mod_ == 0)[0]
                
                xticks = np.arange(num_of_bars)[mask]
                xticks_labels = tmp_labels[mask]
                number_of_ticks = len(xticks)
    
                mod_ *= 10
                sanity_counter += 1
        
        elif not(labels_are_int):
            
            tmp_xticks = np.arange(num_of_bars)
    
            while number_of_ticks > 10 and sanity_counter < 100000:
                
                xticks = tmp_xticks[tmp_xticks % mod_ == 0]
                xticks_labels = labels[xticks]
                number_of_ticks = len(xticks)
    
                mod_ *= 10
                sanity_counter += 1
        
        log.debug("sanity_counter: {}".format(sanity_counter))
    
    log.debug("Setting xticks: {}".format([a for a in xticks]))
    log.debug("xticklabels: {}".format(xticks_labels))
    
    return xticks, xticks_labels

def _extended_bar_xticks(num_of_bars):
    """
    Algorythm to calculate the distribution of xticks
    in extended bar plots.
    
    Parameters
    ----------
    num_of_bars : int
        The number of bars in the plot.
    
    Returns
    -------
        int
            The spacer slicer to be used in numpy.ndarray objtes
            such as xticks, xticks_labels, and others.
            [::mod_]
    """
    
    # Define tick spacing
    for j in range(101,10000,100):
        if j > num_of_bars:
            mod_ = j // 100
            break
    
    log.debug("Tick spacing set to: {}".format(mod_))
    
    return mod_
