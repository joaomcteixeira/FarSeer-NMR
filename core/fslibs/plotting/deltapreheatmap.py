"""
DeltaPRE HeatMap Plot.

Represents DeltaPRE data in heat maps, according to:

Arbesú, M. et al. The Unique Domain Forms a Fuzzy Intramolecular 
    Complex in Src Family Kinases. Structure 25, 630–640.e4 (2017).

Subplots, one for each peaklist, i.e. experiment, are stacked
sequentially from top to bottom.
"""
import numpy as np
import json

from matplotlib import pyplot as plt

from core import validate
from core.fslibs import Logger
from core.fslibs.plotting.plotlibs import (
    plottingbase,
    experimentplotbase,
    barplotbase,
    plotvalidators,
    )

log = Logger.FarseerLogger(__name__).setup_log()

_default_config = {
    
    "cols_page": 1,
    "rows_page": 20,
    
    "vmin": 0.05,
    "vmax": 1.0,
    
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 4,
    "x_ticks_pad": 1,
    "x_ticks_len": 1.5,
    "x_ticks_weight": "normal",
    "x_ticks_rot": 0,
    
    "y_label_fn": "Arial",
    "y_label_fs": 3,
    "y_label_pad": 2,
    "y_label_weight": "bold",
    
    "top_margin": 0.9,
    "right_margin": 0.22,
    "bottom_margin": 0,
    
    "cbar_font_size": 4,
    
    "tag_line_color": "red",
    "tag_line_ls": "-",
    "tag_line_lw": 0.8,
    
    "hspace": 0,
    "rightspace": 0.3,
    }


def get_config():
    """
    Returns the module's default config dictionary.
    """
    return _default_config


def print_config(indent=4, sort_keys=True):
    """
    Nicely prints module's default config.
    
    Parameters
    ----------
    indent : int, optional
        Indentation for sublevels. Defaults to 4.
    
    sort_keys : bool, optional
        Sorts config keys. Default to True.
    """
    
    if not(isinstance(indent, int)):
        raise ValueError("indent should be int type")
    
    if not(isinstance(sort_keys, bool)):
        raise ValueError("sort_keys should be bool type")
    
    print(json.dumps(_default_config, indent=indent, sort_keys=sort_keys))
    
    return


def _subplot(
        ax,
        values,
        i,
        c,
        suptitles,
        tag_position,
        ):
    """Subplot routine."""
    
    vmin = c["vmin"]
    vmax = c["vmax"]
    
    Dcmap = np.array((np.nan_to_num(values), np.nan_to_num(values)))
    
    cleg = ax.pcolor(Dcmap, cmap='binary', vmin=vmin, vmax=vmax)
    
    # configure tick params
    ax.tick_params(axis='y', left='off')
    ax.tick_params(axis='x', bottom='off')
    
    # http://stackoverflow.com/questions/2176424/hiding-axis-text-in-matplotlib-plots
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_visible(False)
    
    ax.set_ylabel(
        suptitles[i],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        )
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    
    if tag_position is not None:
        tag_found = experimentplotbase.finds_paramagnetic_tag(
            ax.get_xaxis(),
            tag_position[i],
            )
            
        if tag_found:
            experimentplotbase.draw_paramagnetic_tag(
                ax,
                tag_found + 0.5,
                tag_cartoon_color=c["tag_cartoon_color"],
                tag_cartoon_ls=c["tag_cartoon_ls"],
                tag_cartoon_lw=c["tag_cartoon_lw"],
                plottype='heatmap',
                )
        else:
            log.debug("Paramagnetic tag not found, ignoring...")

    return cleg


def _final_subplot(ax, values, labels, c, figure, cleg):
        
        vmin = c["vmin"]
        vmax = c["vmax"]
        
        bottom_margin = 1 / values.size
        
        cbar = plt.colorbar(
            cleg,
            ticks=[vmin, vmax / 4, vmax / 4 * 2, vmax / 4 * 3, vmax],
            orientation='vertical',
            cax=figure.add_axes(
                [
                    c["rightspace"] + 0.01,
                    bottom_margin,
                    0.01,
                    c["top_margin"] - bottom_margin,
                    ]
                )
            )
        
        cbar.ax.tick_params(labelsize=c["cbar_font_size"])
        ax.get_xaxis().set_visible(True)
        ax.tick_params(
            axis='x',
            bottom='on',
            length=c["x_ticks_len"],
            pad=c["x_ticks_pad"],
            )
        
        xticks, xticks_labels = barplotbase.compacted_bar_xticks(
            len(values),
            labels,
            )
        
        ax.set_xticks(xticks)
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        ax.set_xticklabels(
            xticks_labels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"],
            )
        log.debug("set_xticklabels: OK")
        
        return


def plot(
        values,
        labels,
        header="",
        suptitles=None,
        tag_position=None,
        **kwargs,
        ):
    """
    Plots DetalPRE Heat Map plot.
    
    Parameters
    ----------
    values : np.ndarray shape (y,x), dtype=float
        Where X (axis=1) is the data to plot for each bar (residue),
        Y (axis=0) is the evolution of that data along the titration
        series.
        
    labels : np.ndarray shape (x,), dtype=str
        Bar labels which are drawn as xtick labels.
    
    header : str, optional
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space.
    
    suptitles : list of str, optional
        Titles of each subplot, length must be equal to values.shape[0].
        Defaults to a range of values.shape[0], ["0", "1", "2", ...
    
    Bellow Parameters Assigned to None if not provided
    --------------------------------------------------

    tag_position : np.ndarray shape (y,x), dtype=str, optional
        Null values where tag not present, "*" character denotes
        the position of the of the paramagnetic tag.
        If None provided, Tag tick is not drawn.
    
    Plot Configuration Parameters
    -----------------------------
    
    **kwargs :
        Plot details (colors, shapes, fonts, ...) can be highly
        configured through additional named parameters.
        
        The available options for named parameters are stored in a
        default configuration dictionary that can be obtained through
        the module's .get_config() (see also .prin_config()) functions.
        
        This dictionary can be modified and passed enterilly to the
        function call, do not forget the unpacking operator (**),
        or, instead if individual arguments are passed, those will
        update the default configuration.
        
        If no **kwargs are provided, the default configuration
        dictionary is used.
        
        Example:
        
        >>> my_config_dict = {"figure_path": "super_plot.pdf"}
        >>> plot(some_values, some_labels, **my_config_dict)
        
        or
        
        >>> plot(some_values, some_labels, figure_path="super_plot.pdf")
    """
    suptitles = suptitles or [str(i) for i in range(values.shape[0])]
    
    # validates type of positional arguments
    args2validate = [
        ("values", values, np.ndarray),
        ("labels", labels, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of optional named arguments
    args2validate = [
        ("header", header, str),
        ("suptitles", suptitles, list),
        ("tag_position", tag_position, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate if t[1] is not None]
    
    # validates shapes and lengths of arguments
    plotvalidators.validate_shapes(values, ("tag_position", tag_position))
    
    plotvalidators.validate_len(values[0, :], ("labels", labels))
    plotvalidators.validate_len(values[:, 0], ("suptitles", suptitles))
    
    # assigns and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="DeltaPRE HeatMap",
        )
    
    """Runs all operations to plot."""
    num_subplots = experimentplotbase.calc_num_subplots(values)
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    for i in range(values.shape[0]):
        
        log.debug("Starting subplot no: {}".format(i))
        
        cleg = _subplot(
            axs[i],
            values[i],
            labels,
            i,
            config,
            suptitles,
            tag_position,
            )
    else:
        _final_subplot(
            axs[i],
            values[i],
            labels,
            config,
            figure,
            cleg,
            )
    
    plottingbase.adjust_subplots(
        figure,
        config["hspace"],
        config["wspace"],
        )
    
    plottingbase.clean_subplots(axs, num_subplots)
    
    plottingbase.save_figure(
        figure,
        config["figure_path"],
        header=header,
        header_fs=config["header_fontsize"],
        dpi=config["figure_dpi"],
        )
    
    plt.close(figure)
    
    return


if __name__ == "__main__":
    
    print("I am DeltaPRE HeatMap Plot")
