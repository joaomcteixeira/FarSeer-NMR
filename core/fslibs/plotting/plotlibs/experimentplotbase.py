import numpy as np

from core.fslibs import Logger

log = Logger.FarseerLogger(__name__).setup_log()


def calc_num_subplots(values):
    """
    Calculates the total number of subplots to be plotted
    based on the user data.
    
    Parameters
    ----------
    values : np.ndarray shape (y,x), dtype=float
        where X (axis=1) is the data to plot for each column,
        Y (axis=0) is the evolution of that data along the titration.
    """
    num_subplots = values.shape[0]
    log.debug(f"Number of subplots: {num_subplots}")
    
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
    
    Parameters
    ----------
    ax : :obj:`matplotlib.axes.Axes`
        
    tag_position : int
        The bar index where the paramagnetic tag is placed.
        Bar index can be obtained via .finds_para_tag()
        
    y_lim : float
        Plot's y axis limit
        
    plottype : ['h', 'v', 'hm'], optional
        Whether plot of type horizontal, vertical or Heat Map.
        Defaults: 'h'
        
    tag_cartoon_color : str, optional
        The colour of the tag cartoon. Defaults to "black".
        
    tag_cartoon_ls : str, optional
        matplotlib's linestyle kwarg for the tag tick. Defaults to "-".
        
    tag_cartoon_lw : float, optional
        Tag tick line width. Defaults to 1.0.
    """
    
    y_lim = y_lim * 0.1
    
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


def finds_paramagnetic_tag(
        data,
        tag_data,
        tag_id="*",
        ):
    """
    Finds the bar index where the tag tick should be drawn based
    on <tag_id>.
    
    Parameters
    ----------
    data : iterator type
        data upon which the index will be searched
        
    tag_data : np.ndarray, dtype=str
        Null values where tag not present, <identifier> character
        denotes the position of the of the paramagnetic tag.
    
    tag_id : str, optional
        The tag identifier. Defaults to "*".
    
    Returns
    -------
        int
            The index where tag is located
    """
    
    if len(data) != len(tag_data):
        _ = "*** Data and tag_data size equal: FALSE"
        log.info(_)
        raise ValueError(_)
    
    log.debug("Tag info: {}".format(tag_data))
    
    where_tag = np.where(tag_data == tag_id)
    log.debug("Tag mask found: {}".format(where_tag))
    
    tag_position = list(range(len(data)))[where_tag[0][0]]
    log.debug("Tag bar index position: {}".format(tag_position))
    
    return tag_position


def plot_theo_pre(
        ax,
        values_x,
        values_y,
        plottype='h',
        theo_pre_color="red",
        theo_pre_lw=1.0,
        ):
    """
    Plots theoretical PRE.
    
    Parameters
    ----------
    ax : :obj:`matplotlib.axes.Axes`
        
    values_x : np.ndarray
        X values to plot
        
    values_y : np.ndarray
        Y values to plot
        
    plottype : ['h', 'v'], optional
        Whether the plot is of horizontal or vertical type.
        Defaults: 'h'.
    
    theo_pre_color : str, optional
        Plot line color. Defaults "red"
    
    theo_pre_lw : float, optional
        Plot line width. Defaults to 1.0.
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
    
    Parameters
    ----------
    items : matplotib's items obj
        Either plot bars, ticks, etc...
    
    values : np.ndarray of shape (x,)
        Containing the condition information.
    
    d : dict
        Keys are conditions matching <values>, and values are colours.
    """
    
    log.debug("Setting colours: {}".format(values))
    
    for v, item_ in zip(values, items):
        if str(v) in d.keys():
            item_.set_color(d[str(v)])
    return


def text_marker(
        ax,
        values_x,
        values_y,
        series,
        d,
        fs=3,
        orientation='horizontal',
        ):
    """
    Places a text mark over the bars of a Bar Plot.
    
    Parameters
    ----------
    ax : :obj:`matplotlib.pyplot.axes`.
        
    values_x : np.ndarray of shape (x,)
        X values to plot.
        
    values_y : np.ndarray of shape (x,)
        Y values to plot.
        
    series : np.ndarray of shape (x,)
        Series with information source to convert to text mark.
        
    d : dict
        Keys are conditions matching <series>, and values are
            the text markers.
        
    fs : float, optional
        Text mark font size.
        
    orientation : ['horizontal', 'vertical'], optional
        Wheter plotting in a vertical or horizontal plot.
        Defaults to 'horizontal'
    """
    
    log.debug(f"Text marker series: {series}")
    
    if orientation == 'vertical':
        
        for s, x, y in zip(series, values_x, values_y):
            if str(s) in d.keys():
                
                if np.nan_to_num(y) > 0:
                    ha = 'left'
                    
                elif np.nan_to_num(y) < 0:
                    ha = 'right'
                
                else:
                    ha = 'center'
                
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
                    va = 'bottom'
                    
                elif np.nan_to_num(y) < 0:
                    va = 'top'
                
                else:
                    va = 'bottom'
                
                ax.text(
                    np.nan_to_num(x),
                    np.nan_to_num(y),
                    d[str(s)],
                    ha='center',
                    va=va,
                    fontsize=fs
                    )
    
    return
