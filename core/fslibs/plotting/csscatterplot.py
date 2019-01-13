import itertools as it
import numpy as np
import json

from matplotlib import pyplot as plt

from core import validate
from core.fslibs import Logger
from plotlibs import (
    plottingbase,
    plotvalidators,
    )

log = Logger.FarseerLogger(__name__).setup_log()

_default_config = {
        
    "cols_page": 5,
    "rows_page": 8,
    
    "hspace": 0.5,
    "wspace": 0.5,
    
    "subtitle_fn": "Arial",
    "subtitle_fs": 8,
    "subtitle_pad": 0.98,
    "subtitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 6,
    "x_label_pad": 2,
    "x_label_weight": "normal",
    "x_label": "1H (ppm)",
    
    "y_label_fn": "Arial",
    "y_label_fs": 6,
    "y_label_pad": 10,
    "y_label_weight": "normal",
    "y_label": "15N (ppm)",
    
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 5,
    "x_ticks_pad": 1,
    "x_ticks_weight": "normal",
    "x_ticks_rot": 30,
    "x_ticks_len": 2,
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 5,
    "y_ticks_pad": 1,
    "y_ticks_weight": "normal",
    "y_ticks_rot": 0,
    "y_ticks_len": 2,
    
    "ticks_nbins": 5,
    "scale": 0.01,
    
    "mk_type": "color",
    "markers": [
        "^",
        ">",
        "v",
        "<",
        "s",
        "p",
        "h",
        "8",
        "*",
        "D"
        ],
    "mksize": 20,
    "mk_start_color": "#696969",
    "mk_end_color": "#000000",
    "mk_color": ["none"],
    "mk_edgecolors": ["black"],
    "mk_missing_color": "red",
    "hide_missing": False,
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
        x_axis_values,
        y_axis_values,
        i,
        c,
        config,
        suptitles,
        peak_status,
        ):
    """ subplot routine."""
    
    def set_tick_labels(nbins=4):
        ax.locator_params(axis='both', tight=True, nbins=nbins)
        ax.set_xticklabels(
            ax.get_xticks(),
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"],
            )
        ax.set_yticklabels(
            ax.get_yticks(),
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"],
            )
        ax.invert_xaxis()
        ax.invert_yaxis()
    
    # Draws subplot title
    ax.set_title(
        suptitles[i],
        y=c["subtitle_fs"],
        fontsize=c["subtitle_fs"],
        fontname=c["subtitle_fn"],
        fontweight=c["subtitle_weight"],
        )
    
    # Define X Axis
    ax.xaxis.tick_bottom()
    ax.tick_params(
        axis='x',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out',
        )
    ax.set_xlabel(
        c["x_label"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        fontname=c["x_label_fn"],
        weight=c["x_label_weight"],
        )
    
    # Define Y Axis
    ax.yaxis.tick_left()
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out',
        )
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        rotation=-90,
        )
    
    # writes unassigned in the center of the plot for unassigned peaks
    # and plots nothing
    if peak_status is not None and peak_status[i, 0] == 'unassigned':
        ax.text(
            0,
            0,
            'unassigned',
            fontsize=7,
            fontname='Arial',
            va='center',
            ha='center',
            )
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        set_tick_labels()
        
        return
    
    elif peak_status is not None and not(np.any(peak_status == "measured")):
        ax.text(
            0,
            0,
            'all data lost',
            fontsize=7,
            fontname='Arial',
            va='center',
            ha='center',
            )
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        set_tick_labels()
        
        return
    
    # Prepares colors and shapes of scatter points
    if c["mk_type"] == 'shape':
        # represents the points in different shapes
        mcycle = it.cycle(c["markers"])
        cedge = it.cycle(c["mk_edgecolors"])
        
    elif c["mk_type"] == 'color':
        # represents the points in different shapes
        mcycle = it.cycle("o")
        cedge = it.cycle("none")
    
    if c["mk_color"][0] == "none":
        ccycle = it.cycle(
            plottingbase.linear_gradient(
                c["mk_start_color"],
                finish_hex=c["mk_end_color"],
                n=len(x_axis_values),
                )
            )
    else:
        ccycle = it.cycle(c["mk_color"])
    
    c_list = [next(ccycle) for j in range(len(x_axis_values))]
    
    if peak_status is not None:
        c_list = [
            (c["mk_missing_color"] if peak_status[j] == "missing"
                else c_list[j])
            for j in range(len(x_axis_values))
            ]
    
    if peak_status is not None and c["hide_missing"]:
        alpha_list = [(0 if j == "missing" else 1) for j in peak_status[i]]
    
    else:
        alpha_list = [1] * len(x_axis_values)
    
    # plots data
    for j in range(x_axis_values):
        ax.scatter(
            x_axis_values[j],
            y_axis_values[j],
            marker=next(mcycle),
            s=c["mk_size"],
            c=c_list[i],
            edgecolors=next(cedge),
            alpha=alpha_list[i],
            )
    
    # adjust axes scales
    xlim = np.abs(x_axis_values).max() * 1.5
    ylim = np.abs(y_axis_values).max() * 1.5
    
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, xlim)
    
    # Further axis setup
    set_tick_labels(nbins=10)
    
    # draws axis 0 dotted line
    ax.hlines(
        0,
        -100,
        100,
        colors='black',
        linestyles='dotted',
        linewidth=0.25,
        )
    ax.vlines(
        0,
        -100,
        100,
        colors='black',
        linestyles='dotted',
        linewidth=0.25,
        )
    
    # draws scale
    # draws center scale
    ax.hlines(
        0,
        -c["scale"],
        c["scale"],
        colors='darkblue',
        linestyles='-',
        linewidth=1,
        )
    ax.vlines(
        0,
        -c["scale"],
        c["scale"],
        colors='darkblue',
        linestyles='-',
        linewidth=1,
        )
    
    return


def plot(
        x_axis_values,
        y_axis_values,
        header="",
        suptitles=None,
        peak_status=None,
        **kwargs,
        ):
    """
    Plots Chemical Shift Scatter Plot.
    
    It represents a grid of one subplot per each protein residue.
    
    The chemical shift differences along the two axes are represented,
    centered at the refence value (0,0) in the plot scale.
    
    Parameters
    ----------
    x_axis_values : np.ndarray with shape (y, x), dtype=float
        Values to plot along the X axis.
        
        Where X (axis=1) represents the evolution of the parameter
        to plot for the individual residues along the titration series,
        
        and Y (axis=0) represents the different residues sequentially
        ordered according to the protein sequence.
    
    y_axis_values : np.ndarray with shape (y, x), dtype=float
        Values to plot along the Y axis.
        Parameter details are the same as for <x_axis_values>
    
    header : str, optional
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space.
    
    suptitles : list of lenght Y (values.shape[0]), dtype=str, optional
        Suptitles for each subplot. Generally are the residue names:
            "1M", "2A", ...
        
        If None provided, range(values.shape[0]) is used.
    
    peak_status : np.ndarray shape (y, x), dtype=str, optional
        Peak status information according to core.utils.peak_status
        dictionary.
        
        If provided, "unnassigned" peaks will be displayed as an
        empty and identified subplot inside the subplots grid.
    
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
        
        >>> plot(some_values, some_labels, figure_path="my_plot.pdf")
    """
    
    suptitles = suptitles or [str(i) for i in range(x_axis_values.shape[0])]
    
    # validates type of positional arguments
    args2validate = [
        ("x_axis_values", x_axis_values, np.ndarray),
        ("y_axis_values", y_axis_values, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of named optional arguments
    args2validate = [
        ("suptitles", suptitles, list),
        ("peak_status", peak_status, np.ndarray),
        ]
    
    [validate.validate_types(t)
        for t in args2validate if t[1] is not None]
    
    # validates shapes and lenghts
    args2validate = [
        ("y_axis_values", y_axis_values),
        ("peak_status", peak_status),
        ]
    
    [plotvalidators.validate_shapes(x_axis_values, t)
        for t in args2validate if t[1] is not None]
    
    args2validate = [
        ("suptitles", suptitles),
        ]
    
    [plotvalidators.validate_len(x_axis_values[:, 0], t)
        for t in args2validate if t[1] is not None]
    
    # assigned and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="CS Scater Plot",
        )
    
    """Runs all operations to plot."""
    num_subplots = x_axis_values.shape[0]
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    for i in range(x_axis_values.shape[0]):
        _subplot(
            axs[i],
            x_axis_values[i],
            y_axis_values[i],
            i,
            config,
            suptitles,
            peak_status,
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
    
    print("I am CS Scater Plot")