import numpy as np
from core.fslibs.WetHandler import WetHandler
import core.fslibs.Logger as Logger

plotting_base_logger = Logger.FarseerLogger(__name__).setup_log()
plotting_base_logger.debug("Initiated barplot_base module")

def _finds_para_tag(data, tag_data, identifier="*"):
    """
    Finds the bar index where the tag tick should be drawn based
    on an <identifier>.
    
    Parameters:
        
        - data (iterator): data upon which the index will be searched
        
        - tag_data (np.array): contains information where the tag is
        
        - identifier (str): the identifier to look for.
    """
    if len(data) != len(tag_data):
        logger.debug("data and tag_data of different size!")
        return False
    
    logger.debug("Tag info: {}".format(tag_data))
    
    where_tag = np.where(tag_data==identifier)
    logger.debug("Tag position: {}".format(where_tag))
    
    tag_position = list(range(len(data)))[where_tag[0][0]]
    logger.debug("tag position: {}".format(tag_position))
    
    return tag_position

def draw_paramagnetic_tag(
        ax,
        tag_position,
        y_lim,
        plottype='h',
        tag_color='red',
        tag_ls='-',
        tag_lw=0.1
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
            colors=tag_color,
            linestyle=tag_ls,
            linewidth=tag_lw,
            zorder=10
            )
        ax.plot(
            tag_position,
            y_lim,
            'o',
            zorder=10,
            color='red',
            markersize=2
            )
    
    elif plottype == 'v':
        ax.hlines(
            tag_position,
            0,
            y_lim,
            colors=tag_color,
            linestyle=tag_ls,
            linewidth=tag_lw,
            zorder=10
            )
        ax.plot(
            y_lim,
            tag_position,
            'o',
            zorder=10,
            color='red',
            markersize=2
            )
    
    elif plottype == 'heatmap':
        
        tag_line = 2
        
        ax.vlines(
            tag_position,
            0,
            tag_line,
            colors=tag_color,
            linestyle=tag_ls,
            linewidth=tag_lw,
            zorder=10
            )
    return

def plot_theo_pre(
            ax,
            values_x,
            values_y,
            pre_color='lightblue',
            pre_lw=1,
            orientation='h',
            ):
    """
    Plots theoretical PRE.
    
    Parameters:
        axs (matplotlib subplot axis): where values are plot.
        
        values_x (np.ndarray): X values where to plot
        
        values_y (np.adrray): Y values to plot
        
        orientation (str): {'h', 'v'}, whether plot of type 
            horizontal, vertical or Heat Map. Defaults: 'h'.
        
        pre_color (str): the colour of plot line
        
        pre_lw (int): line width
        
    """
    
    if plottype == 'v':
        ax.plot(
            values_y,
            values_x,
            zorder=9,
            color=pre_color,
            lw=pre_lw
            )
    
    elif plottype == 'h':
        ax.plot(
            values_x,
            values_y,
            zorder=9,
            color=pre_color,
            lw=pre_lw
            )
    
    return
