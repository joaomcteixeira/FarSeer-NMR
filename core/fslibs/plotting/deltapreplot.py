import itertools as it
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
    "rows_page": 6,
    
    "ymax": 1,
    "y_label": "$\\Delta$PRE$_(rc-exp)$",
    
    "subtitle_fn": "Arial",
    "subtitle_fs": 8,
    "subtitle_pad": 0.99,
    "subtitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 8,
    "x_label_pad": 2,
    "x_label_weight": "bold",
    "x_label_rot": 0,
    
    "y_label_fn": "Arial",
    "y_label_fs": 8,
    "y_label_pad": 3,
    "y_label_weight": "bold",
    "y_label_rot": 90,
    
    "x_ticks_pad": 0.5,
    "x_ticks_len": 2,
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 6,
    "x_ticks_rot": 0,
    "x_ticks_weight": "normal",
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 6,
    "y_ticks_rot": 0,
    "y_ticks_pad": 1,
    "y_ticks_weight": "normal",
    "y_ticks_len": 2,
    "y_ticks_nbins": 8,
    
    "y_grid_flag": True,
    "y_grid_color": "lightgrey",
    "y_grid_linestyle": "-",
    "y_grid_linewidth": 0.2,
    "y_grid_alpha": 0.8,
    
    "tag_cartoon_color": "black",
    "tag_cartoon_lw": 1.0,
    "tag_cartoon_ls": "-",
    
    "dpre_ms": 2,
    "dpre_alpha": 0.5,
    "smooth_lw": 1,
    "ref_color": "black",
    "color_init": "#000080",
    "color_end": "#FFD700",
    "grid_color": "grey",
    "shade": False,
    "shade_regions": [
        [
            0,
            10,
            ],
        [
            20,
            25,
            ]
        ],
    "res_highlight": False,
    "res_hl_list": [
        1,
        2
        ],
    "res_highlight_fs": 4,
    "res_highlight_y": 0.9,
    
    "hspace": 0.5,
    "wspace": 0.5,
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
        pre_values,
        smoothed_pre,
        labels,
        i,
        c,
        suptitles,
        letter_code,
        tag_position,
        color,
        ):
    """Subplot routine."""
    
    ###################
    # configures vars
    pre_values_ref = np.nan_to_num(pre_values[0]).astype(float)
    pre_values_i = np.nan_to_num(pre_values[i]).astype(float)
    
    smooth_values_ref = np.nan_to_num(smoothed_pre[0]).astype(float)
    smooth_values_i = np.nan_to_num(smoothed_pre[i]).astype(float)
    
    log.debug("pre_values_i: {}".format(pre_values_i))
    log.debug("smooth_values_i: {}".format(smooth_values_i))
    
    num_of_items = smooth_values_ref.size
    log.debug("Number of bars to represented: {}".format(num_of_items))
    log.debug("Suptitle: {}".format(suptitles[i]))
    
    ###################
    # Plots
    # plots reference data
    if i > 0:
        ax.plot(
            range(num_of_items),
            pre_values_ref,
            ls='o',
            markersize=c["dpre_ms"],
            markeredgewidth=0.0,
            c=c["ref_color"],
            alpha=c["dpre_alpha"],
            zorder=10,
            )
        
        ax.plot(
            range(num_of_items),
            smooth_values_ref,
            ls='-',
            lw=c["smooth_lw"],
            c=c["ref_color"],
            zorder=10,
            )
    
    plot_i_1 = ax.plot(
        range(num_of_items),
        pre_values_i,
        ls='o',
        markersize=c["dpre_ms"],
        markeredgewidth=0.0,
        c=color,
        alpha=c["dpre_alpha"],
        zorder=10,
        )
        
    plot_i_2 = ax.plot(
        range(num_of_items),
        smooth_values_i,
        ls='-',
        lw=c["smooth_lw"],
        c=color,
        zorder=10,
        )
    
    log.debug(f"Number of plot_i_1 plotted: {len(plot_i_1)}")
    log.debug(
        "Number of expected bars equals num of bars: "
        f"{num_of_items == len(plot_i_1)}"
        )
    
    ###################
    # Set subplot title
    ax.set_title(
        suptitles[i],
        y=c["suptitle_pad"],
        fontsize=c["suptitle_fs"],
        fontname=c["suptitle_fn"],
        weight=c["suptitle_weight"],
        )
    
    log.debug("Subplot title set to : {}".format(suptitles[i]))
    
    ###################
    # Configures spines
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    log.debug("Spines set: OK")
    
    ###################
    # Configures X ticks and X ticks labels
    
    xticks, xticks_labels = barplotbase.compacted_bar_xticks(
        num_of_items,
        labels,
        )
    
    # Set X ticks
    ax.set_xticks(xticks)
    
    # Set X ticks labels
    # https://github.com/matplotlib/matplotlib/issues/6266
    ax.set_xticklabels(
        xticks_labels,
        fontname=c["x_ticks_fn"],
        fontsize=c["x_ticks_fs"],
        fontweight=c["x_ticks_weight"],
        rotation=c["x_ticks_rot"],
        )
    
    # Set xticks params
    ax.tick_params(
        axis='x',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out',
        )
    ax.margins(x=0.01, tight=True)
    log.debug("Configured X tick params: OK")
    
    # Set X axis label
    ax.set_xlabel(
        c["x_label"],
        fontname=c["x_label_fn"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        weight=c["x_label_weight"],
        rotation=c["x_label_rotation"],
        )
    log.debug("Set X label: OK")
    
    ###################
    # Configures Y ticks and axis
    
    # sets axis limits
    ymin = c["y_lims"][0]
    ymax = c["y_lims"][1]
    ax.set_ylim(ymin, ymax)
    log.debug("Set y max {} and ymin {}".format(ymin, ymax))
    
    # sets number of y ticks
    ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
    
    # sets y tick labels
    ax.set_yticklabels(
        ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
        fontname=c["y_ticks_fn"],
        fontsize=c["y_ticks_fs"],
        fontweight=c["y_ticks_weight"],
        rotation=c["y_ticks_rot"],
        )
    log.debug("Set Y tick labels: OK")
    
    # sets y ticks params
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out',
        )
    log.debug("Configured Y tick params: OK")
    
    # set Y label
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        rotation=c["y_label_rot"],
        )
    log.debug("Set Y label: OK")
    
    ###################
    # Additional configurations
    # "is not None" is used in IF statements intentionally
    
    ###################
    # Additional representation features
    
    if c["shade"]:
        for lmargin, rmargin in c["shade_regions"]:
            ax.fill(
                [lmargin, rmargin, rmargin, lmargin],
                [0, 0, 2, 2],
                c["grid_color"],
                alpha=0.2,
                )
    
    if c["res_highlight"]:
        for rr in c["res_hl_list"]:
            ax.axvline(x=rr, ls=':', lw=0.3, color=c["grid_color"])
            
            # this implementation is possible because
            # x values are range(num_of_items)
            rrindex = np.argwhere(labels == str(rr))
            ax.text(
                rr,
                c["ymax"] * c["res_highlight_y"],
                int(rrindex),
                ha='center',
                va='center',
                fontsize=c["res_highlight_fs"],
                )
    
    # Adds grid
    if c["y_grid_flag"]:
        ax.yaxis.grid(
            color=c["y_grid_color"],
            linestyle=c["y_grid_linestyle"],
            linewidth=c["y_grid_linewidth"],
            alpha=c["y_grid_alpha"],
            zorder=0,
            )
        log.debug("Configured grid: OK")
           
    if tag_position is not None:
        
        tag_found = experimentplotbase.finds_paramagnetic_tag(
            plot_i_2,
            tag_position[i],
            )
        
        if tag_found:
            experimentplotbase.draw_paramagnetic_tag(
                ax,
                tag_found,
                c["ymax"],
                tag_cartoon_color=c["tag_cartoon_color"],
                tag_cartoon_ls=c["tag_cartoon_ls"],
                tag_cartoon_lw=c["tag_cartoon_lw"],
                )
    
    return


def plot(
        pre_values,
        smoothed_pre,
        labels,
        header="",
        suptitles=None,
        letter_code=None,
        tag_position=None,
        **kwargs,
        ):
    """
    Plots according to the Delta PRE Plot Template.
    
    The Delta PRE Plot template draws wide subplots
    designed to fit half page with individually.
    
    Bar Plots represent parameters for each residue individually
    in the form of bars.
    
    Subplots, one for each peaklist, i.e. experiment, are stacked
    sequentially in grid from top to bottom.
    This arrangement can be used directly as a supplementary figure.
    
    Parameters
    ----------
    pre_values : np.ndarray shape (y,x), dtype=float
        Information on observed PRE values, to be plotted as dots.
        Where X (axis=1) is the data to plot for each bar (residue),
        Y (axis=0) is the evolution of that data along the titration
        series.
    
    smoothed_pre : np.ndarray shape (y,x), dtype=float
        Smoothed PRE data to be plotted as a line.
    
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
    
    letter_code : np.ndarray shape (x,), dtype=str, optional
        1-letter code of the protein sequence, should have length equal
        to <labels>.

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
    
    suptitles = suptitles or [str(i) for i in range(pre_values.shape[0])]
    
    # validates type of positional arguments
    args2validate = [
        ("label", labels, np.ndarray),
        ("pre_values", pre_values, np.ndarray),
        ("smoothed_pre", smoothed_pre, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of optional named arguments
    args2validate = [
        ("header", header, str),
        ("suptitles", suptitles, list),
        ("letter_code", letter_code, np.ndarray),
        ("tag_position", tag_position, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate if t[1] is not None]
    
    # validates shapes and lenghts of arguments
    args2validate = [
        ("smoothed_pre", smoothed_pre),
        ("tag_position", tag_position),
        ]
    
    [plotvalidators.validate_shapes(pre_values, t)
        for t in args2validate if t[1] is not None]
    
    args2validate = [
        ("labels", labels),
        ("letter_code", letter_code),
        ]
    
    [plotvalidators.validate_len(pre_values[0, :], t)
        for t in args2validate if t[1] is not None]
    
    plotvalidators.validate_len(pre_values[:, 0], ("suptitles", suptitles))
    
    # assigns and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="DeltaPRE Plot",
        )
    
    """Runs all operations to plot."""
    num_subplots = pre_values.shape[0]
    log.debug(f"number of subplots: {num_subplots}")
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    dp_colors = plottingbase.linear_gradient(
        config['color_init'],
        config['color_end'],
        n=pre_values.shape[1]
        )
    
    dp_color = it.cycle(dp_colors['hex'])
    
    for i in range(pre_values.shape[0]):
        
        log.debug("Starting subplot no: {}".format(i))
        # other parameters are not passed because they are None by default
        # and may lead to IndexError
        _subplot(
            axs[i],
            pre_values,
            smoothed_pre,
            labels,
            i,
            config,
            suptitles,
            letter_code,
            tag_position,
            next(dp_color),
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
    
    print("I am DPRE Plot")
