def calc_num_subplots(values):
    """
    Calculates the total number of subplots to be plotted
    based on the user data.
    
    Returns:
        - None
        
    Stores:
        - self.num_subplots (int)
    """
    num_subplots = values.shape[0]
    logger.debug(f"Number of subplots: {num_subplots}")
    
    return num_subplots

def draw_paramagnetic_tag(
        ax,
        tag_position,
        y_lim,
        plottype='h',
        tag_cartoon_color="black",
        tag_cartoon_ls="-",
        tag_cartoon_lw=1.0,
        ):
    """
    Draws paramagnetic tag tick on functionalized residue.
    
    Parameters:
        axs (matplotlib subplot axis): where values are plot.
        
        tag_position (int): the residue number where the paramagnetic
            tag is placed.
        
        y_lim (float): plot's y axis limit
        
        plottype (str): {'h', 'v', 'hm'}, whether plot of type 
            horizontal, vertical or Heat Map. Defaults: 'h'.
        
        tag_color (str): the colour of the tag cartoon
        
        tag_ls (str): matplotlib linestyle kwarg for the tag tick
        
        tag_lw (float): tag tick line width.
    """
    
    y_lim = y_lim*0.1
    
    if plottype in ['h', 'DPRE_plot']:
        ax.vlines(
            tag_position,
            0,
            y_lim,
            colors=tag_cartoon_color,
            linestyle=tag_cartoon_ls,
            linewidth=tag_cartoon_lw,
            zorder=10,
            )
        ax.plot(
            tag_position,
            y_lim,
            'o',
            zorder=10,
            color='red',
            markersize=2,
            )
    
    elif plottype == 'v':
        ax.hlines(
            tag_position,
            0,
            y_lim,
            colors=tag_cartoon_color,
            linestyle=tag_cartoon_ls,
            linewidth=tag_cartoon_lw,
            zorder=10,
            )
        ax.plot(
            y_lim,
            tag_position,
            'o',
            zorder=10,
            color='red',
            markersize=2,
            )
    
    elif plottype == 'heatmap':
        
        tag_line = 2
        
        ax.vlines(
            tag_position,
            0,
            tag_line,
            colors=tag_cartoon_color,
            linestyle=tag_cartoon_ls,
            linewidth=tag_cartoon_lw,
            zorder=10,
            )
    return

def finds_para_tag(data, tag_data, tag_id="*"):
    """
    Finds the bar index where the tag tick should be drawn based
    on an <identifier>.
    
    Parameters:
        
        - data (iterator): data upon which the index will be searched
        
        - tag_data (np.array): contains information where the tag is
    
    Returns:
        - index where Tag is located
    """
    if len(data) != len(tag_data):
        logger.info("*** Data and tag_data size equal: FALSE")
        return False
    
    logger.debug("Tag info: {}".format(tag_data))
    
    where_tag = np.where(tag_data==tag_id)
    logger.debug("Tag mask found: {}".format(where_tag))
    
    tag_position = list(range(len(data)))[where_tag[0][0]]
    logger.debug("Tag bar index position: {}".format(tag_position))
    
    return tag_position

def plot_theo_pre(
        ax,
        values_x,
        values_y,
        plottype='h',
        theo_pre_color="red",
        theo_pre_lw=1,
        **kargs,
        ):
    """
    Plots theoretical PRE.
    
    Parameters:
        axs (matplotlib subplot axis): where values are plot.
        
        values_x (np.ndarray): X values to plot
        
        values_y (np.adrray): Y values to plot
        
        plottype (str): {'h', 'v'}, whether plot of type 
            horizontal, vertical or Heat Map. Defaults: 'h'.
        
    """
    
    if plottype == 'v':
        ax.plot(
            values_y,
            values_x,
            zorder=9,
            color=theo_pre_color,
            lw=theo_pre_lw,
            )
    
    elif plottype == 'h':
        ax.plot(
            values_x,
            values_y,
            zorder=9,
            color=theo_pre_color,
            lw=theo_pre_lw,
            )
    
    return

def set_item_colors(items, values, d):
    """
    Colour codes <items> according to conditions in <values>
    as described by <d>.
    
    Parameters:
        items (items obj): either plot bars, ticks, etc...
    
        values (np.array shape (x,)):
            containing the condition information.
    
        d (dict): keys are conditions, and values are colours.
    
    Returns:
        None, series are changed in place.
    """
    
    logger.debug("Setting colours: {}".format(values))
    
    for v, it in zip(values, items):
        if str(v) in d.keys():
            it.set_color(d[str(v)])
    return

def text_marker(
        ax,
        values_x,
        values_y,
        series,
        d,
        fs=3,
        orientation='horizontal',
        **kwargs,
        ):
    """
    Places a text mark over the bars of a Bar Plot.
    
    Parameters:
        ax (matplotlib subplot axis): where maker is written.
        
        values_x (np.array): series with X axis information
        
        values_y (np.array): series with Y axis information
        
        series (np.array): series with information source to
            convert to text mark.
        
        d (dict): translates information into marker.
        
        fs (int): font size
        
        orientation (str): {'horizontal', 'vertical'}
            wheter plotting in a vertical or horizontal plot.
            Defaults to 'horizontal'
    """
    logger.debug(f"Text marker series: {series}")
    
    if orientation == 'vertical':
        
        for s, x, y in zip(series, values_x, values_y):
            if str(s) in d.keys():
                
                if np.nan_to_num(y) > 0:
                    ha='left'
                    
                elif np.nan_to_num(y) < 0:
                    ha='right'
                
                else:
                    ha='center'
                
                ax.text(
                    np.nan_to_num(y),
                    np.nan_to_num(x),
                    d[str(s)],
                    ha=ha,
                    va='center',
                    fontsize=fs
                    )
    
    elif orientation == 'horizontal':
        
        for s, x, y in zip(series, values_x, values_y):
            if str(s) in d.keys():
                
                if np.nan_to_num(y) > 0:
                    va='bottom'
                    
                elif np.nan_to_num(y) < 0:
                    va='top'
                
                else:
                    va='bottom'
                
                ax.text(
                    np.nan_to_num(x),
                    np.nan_to_num(y),
                    d[str(s)],
                    ha='center',
                    va=va,
                    fontsize=fs
                    )
    
    return
