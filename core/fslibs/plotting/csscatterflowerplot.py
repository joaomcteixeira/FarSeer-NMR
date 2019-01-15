"""
Chemical Shift Scatter Plot.
    
It represents a grid of one subplot per each protein residue.

The chemical shift differences along the two dimensions (axes) are
represented, centered at the refence value (0,0) in the plot scale.
"""
import itertools as it
import numpy as np
import json

from matplotlib import pyplot as plt

from core import validate
from core.fslibs import Logger
from core.fslibs.plotting.plotlibs import (
    plottingbase,
    plotvalidators,
    )

log = Logger.FarseerLogger(__name__).setup_log()

_default_config = {
    "cols_page": 2,
    "rows_page": 3,
    
    "x_label": "1H (ppm)",
    "y_label": "15N (ppm)",
    
    "xlim": 1,
    "ylim": 1,
    
    "mk_size": 8,
    
    "color_grad": True,
    "mk_start_color": "#696969",
    "mk_end_color": "#000000",
    "color_list": ["black"],
    "color_missing": "red",
    "hide_missing": False,
    
    "res_label_color": "gold",
    
    "x_label_fn": "Arial",
    "x_label_fs": 10,
    "x_label_pad": 5,
    "x_label_weight": "normal",
    
    "y_label_fn": "Arial",
    "y_label_fs": 10,
    "y_label_pad": 10,
    "y_label_weight": "normal",
    "y_label_rot": -90,
    
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 8,
    "x_ticks_pad": 1,
    "x_ticks_len": 2,
    "x_ticks_weight": "normal",
    "x_ticks_rot": 0,
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 8,
    "y_ticks_pad": 1,
    "y_ticks_len": 2,
    "y_ticks_weight": "normal",
    "y_ticks_rot": 0,
    
    "hspace": 0.1,
    "wspace": 0.1,
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
        residue_x_values,
        residue_y_values,
        i,
        c,
        peak_status,
        labels,
        ):
    """Plot subplot routine."""
    
    if peak_status is not None \
            and peak_status[i, 0] == "unassigned":
        return
    
    # transforms NaNs to zeros
    x_values = np.nan_to_num(residue_x_values).astype(float)
    y_values = np.nan_to_num(residue_y_values).astype(float)
    
    # set up marker colors
    if c["color_grad"]:
        mark_color_list = plottingbase.linear_gradient(
            c["mk_start_color"],
            finish_hex=c["mk_end_color"],
            n=residue_x_values.size,
            )['hex']
    
    else:
        colors_cycle = it.cycle(c["color_list"])
        mark_color_list = \
            [next(colors_cycle) for i in range(residue_x_values.size)]
    
    # filter colors according to peak_status
    if peak_status is not None:
        missing_mask = peak_status[i, :] == "missing"
        mark_color_list = \
            [c["missing_color"] if missing_mask[j] else mark_color_list[j]
                for j in range(len(mark_color_list))]
    
    # filter visibility according to user preferences
    if peak_status is not None and c["hide_missing"]:
        alpha_list = \
            [1.0 if condition else 0.0 for condition in missing_mask]
    else:
        alpha_list = [1.0 for i in range(x_values.size)]
        
    ax.scatter(
        x_values,
        y_values,
        c=mark_color_list,
        s=c["mk_size"],
        alpha=alpha_list,
        zorder=9,
        )
    
    ax.text(
        float(x_values[-1]) * 1.05,
        float(y_values[-1]) * 1.05,
        labels[i],
        fontsize=4,
        color=c["res_label_color"],
        zorder=10,
        )
    
    return


def _set_axis(ax, c):
    """
    Configures axes.
    """
    # Configure Axis Ticks
    ax.xaxis.tick_bottom()
    ax.tick_params(
        axis='x',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out'
        )
    ax.yaxis.tick_left()
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out'
        )
    # Configure axes labels
    ax.set_xlabel(
        c["x_label"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        fontname=c["x_label_fn"],
        weight=c["x_label_weight"]
        )
    # Configure YY ticks/label
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        rotation=c["y_label_rot"]
        )
    # draws axis 0 dotted line
    ax.hlines(
        0,
        -100,
        100,
        colors='black',
        linestyles='dotted',
        linewidth=0.25
        )
    ax.vlines(
        0,
        -100,
        100,
        colors='black',
        linestyles='dotted',
        linewidth=0.25
        )
    ax.set_xlim(-c["xlim"], c["xlim"])
    ax.set_ylim(-c["ylim"], c["ylim"])
    # remember in NMR spectra the ppm scale is 'inverted' :-)
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.locator_params(axis='both', tight=True, nbins=10)
    ax.set_xticklabels(
        ax.get_xticks(),
        fontname=c["x_ticks_fn"],
        fontsize=c["x_ticks_fs"],
        fontweight=c["x_ticks_weight"],
        rotation=c["x_ticks_rot"]
        )
    ax.set_yticklabels(
        ax.get_yticks(),
        fontname=c["y_ticks_fn"],
        fontsize=c["y_ticks_fs"],
        fontweight=c["y_ticks_weight"],
        rotation=c["y_ticks_rot"]
        )
    
    return


def plot(
        x_axis_values,
        y_axis_values,
        header="",
        peak_status=None,
        labels=None,
        **kwargs,
        ):
    """
    Plots Chemical Shift Scatter plot.
    
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
    
    peak_status : np.ndarray shape (y, x), dtype=str, optional
        Peak status information according to core.utils.peak_status
        dictionary.
        
        If provided, "unnassigned" peaks will be displayed as an
        empty and identified subplot inside the subplots grid.
    
    labels : np.ndarray shape (y,), dtype=str, optional
        Residue labels to represent at the end of the scatter series.
        Residue number is the most common usage.
    
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
    
    # validates type of positional arguments
    args2validate = [
        ("x_axis_values", x_axis_values, np.ndarray),
        ("y_axis_values", y_axis_values, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of named optional arguments
    args2validate = [
        ("header", header, str),
        ("peak_status", peak_status, np.ndarray),
        ("labels", labels, np.ndarray),
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
        ("labels", labels),
        ]
    
    [plotvalidators.validate_len(x_axis_values[:, 0], t)
        for t in args2validate if t[1] is not None]
    
    # assigned and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="CS Scater Flower Plot",
        )
    
    num_subplots = 1
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    axs = axs.ravel()
    
    for i in range(x_axis_values.shape[0]):
        
        _subplot(
            axs,
            x_axis_values[i],
            y_axis_values[i],
            i,
            config,
            peak_status,
            labels,
            )
    else:
        _set_axis(axs, config)
    
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
