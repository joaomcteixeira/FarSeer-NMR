def plot_threshold(
        ax,
        values,
        std=5,
        orientation='horizontal',
        threshold_color="red",
        threshold_linewidth=0.5
        threshold_alpha=0.8,
        threshold_zorder=10,
        **kwargs,
        ):
    """
    Plots threshold line that identifies relevant perturnations.
    
    Parameters:
        ax (matplotlib subplot axis): subplot where line is drawn.
        
        values (np.array of shape [x]): values to evaluate.
        
        color (str): line color.
        
        lw (int): line width.
        
        alpha (float): transparency.
        
        std (int): standard deviation multiplier
        
        orientation (str): {'horizontal', 'vertical'}
            wheter plotting in a vertical or horizontal barplot.
        
        zorder (int): the matplotlib zorder kwarg.
    """
    sorted_values = np.copy(np.sort(np.absolute(values)))
    parsed_values = sorted_values[np.logical_not(np.isnan(sorted_values))]
    firstdecile = parsed_values[0:ceil(0.1*len(parsed_values))]
    threshold = np.mean(firstdecile) + std*np.std(firstdecile)
    
    logger.debug("Threshold defined: {}".format(threshold))
    
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

def plot_subplots(values, axs, subtitles, func):
    """
    Sends the specific data to each subplot.
    Requires self.figure and self.axs
    
    Returns:
        - None
    """
    logger.debug("Starting plot activity")
    
    for i in range(values.shape[0]):
        
        logger.debug("Starting subplot no: {}".format(i))
        
        func(
            self.axs[i],
            self.values[i],
            self.suptitles[i],
            i
            )
    
    # returns the final index
    # useful for some subplots
    return i
