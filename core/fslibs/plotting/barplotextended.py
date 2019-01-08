import numpy as np

from core.fslibs import Logger
from plotlibs import (
    plottingbase,
    experimentplotbase,
    barplotbase,
    plotdecorators,
    )

log = Logger.FarseerLogger(__name__).setup_log()

_default_config = {
    
    "cols_page": 1,
    "rows_page": 6,
    
    "y_lims":(0,0.3),
    "x_label":"Residues",
    "y_label":"your labels goes here",
    
    "subtitle_fn": "Arial",
    "subtitle_fs": 8,
    "subtitle_pad": 0.99,
    "subtitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 8,
    "x_label_pad": 2,
    "x_label_weight": "bold",
    "x_label_rotation":0,
    
    "y_label_fn": "Arial",
    "y_label_fs": 8,
    "y_label_pad": 3,
    "y_label_weight": "bold",
    "y_label_rot":90,
    
    "x_ticks_pad": 2,
    "x_ticks_len": 2,
    "x_ticks_fn": "monospace",
    "x_ticks_fs": 6,
    "x_ticks_rot": 90,
    "x_ticks_weight": "normal",
    "x_ticks_color_flag":True,
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 6,
    "y_ticks_rot": 0,
    "y_ticks_pad": 1,
    "y_ticks_weight": "normal",
    "y_ticks_len": 2,
    "y_ticks_nbins":8,
    
    "y_grid_flag": True,
    "y_grid_color": "lightgrey",
    "y_grid_linestyle": "-",
    "y_grid_linewidth": 0.2,
    "y_grid_alpha": 0.8,
    
    "measured_color": "black",
    "missing_color": "red",
    "unassigned_color": "lightgrey",
    
    "bar_width": 0.8,
    "bar_alpha": 1,
    "bar_linewidth": 0,
    
    "mark_fontsize": 4,
    "mark_prolines_flag": False,
    "mark_prolines_symbol": "P",
    "mark_user_details_flag": False,
    "color_user_details_flag": False,
    "user_marks_dict": {
        "foo": "f",
        "bar": "b",
        "boo": "o"
    },
    "user_bar_colors_dict": {
        "foo": "green",
        "bar": "yellow",
        "boo": "magenta"
    },
    
    "threshold_flag": True,
    "threshold_color": "red",
    "threshold_linewidth": 0.5,
    "threshold_alpha": 0.8,
    "threshold_zorder":10,
    
    "plot_theoretical_pre":False,
    "theo_pre_color": "red",
    "theo_pre_lw": 1.0,
    "tag_id":"*",
    
    "tag_cartoon_color": "black",
    "tag_cartoon_ls": "-",
    "tag_cartoon_lw": 1.0,
    
    "hspace": 0.5,
    "wspace": 0.5,
    
    "header_fontsize":5,
    
    "figure_path":"bar_extended_horizontal.pdf",
    "figure_dpi":300,
    "fig_height": 11.69,
    "fig_width": 8.69
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
    
    if not(isinstance(indent, int)) :
            raise ValueError("indent should be int type")
    if not(isinstance(sort_keys, bool)) :
            raise ValueError("sort_keys should be bool type")
    
    print(json.dumps(_default_config, indent=indent, sort_keys=sort_keys))
    
    return


def _subplot(
        ax,
        values,
        labels,
        i,
        c,
        ):
    """Subplot routine."""
    
    ###################
    # configures vars
    ydata = np.nan_to_num(values).astype(float)
    log.debug("ydata: {}".format(ydata))
    num_of_bars = ydata.shape[0]
    log.debug("Number of bars to represented: {}".format(num_of_bars))
    log.debug("Suptitle: {}".format(suptitles[i]))
    
    ###################
    # Plots bars
    bars = ax.bar(
        range(num_of_bars),
        ydata,
        width=c["bar_width"],
        align='center',
        alpha=c["bar_alpha"],
        linewidth=c["bar_linewidth"],
        color='black',
        zorder=4,
        )
    
    log.debug("Number of bars plotted: {}".format(len(bars)))
    log.debug(
        f"Num of expected bars equals num of bars: {num_of_bars == len(bars)}"
        )
    
    ###################
    # Set subplot title
    ax.set_title(
        suptitles[i],
        y=c["subtitle_pad"],
        fontsize=c["subtitle_fs"],
        fontname=c["subtitle_fn"],
        weight=c["subtitle_weight"],
        )
    
    log.debug("Subplot title set to : {}".format(suptitles[i]))
    
    ###################
    # Configures spines
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    log.debug("Spines set: OK")
    
    ###################
    # Configures X ticks and axis
    
    # Define tick spacing
    for j in range(101,10000,100):
        if j>num_of_bars:
            mod_ = j//100
            break
    log.debug("Tick spacing set to: {}".format(mod_))
    
    # set xticks and xticks_labels to be represented
    xticks = np.arange(len(bars))[0::mod_]
    xticks_labels = np.array(labels)[0::mod_]
    
    log.debug("xticks represented: {}".format(xticks))
    log.debug("xticks labels represented: {}".format(xticks_labels))
    
    # Set X ticks
    ax.set_xticks(xticks)
    
    # Set X ticks labels
    ## https://github.com/matplotlib/matplotlib/issues/6266
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
        direction='out'
        )
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
    
    ax.margins(x=0.01, tight=True)
    
    # defines bars colors
    if peak_status is not None:
        experimentplotbase.set_item_colors(
            bars,
            peak_status[i],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"],
                },
            )
        log.debug("set_item_colors: OK")
    
    ###################
    # Additional representation features
    
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
    
    # defines xticks colors
    if peak_status is not None and c["x_ticks_color_flag"]:
        log.debug("Configuring for x_ticks_color_flag...")
        experimentplotbase.set_item_colors(
            ax.get_xticklabels(),
            peak_status[i,0::mod_],
            {
                'measured':c["measured_color"],
                'missing':c["missing_color"],
                'unassigned':c["unassigned_color"],
                },
            )
        log.debug("...Done")
    
    # Adds red line to identify significant changes.
    if c["threshold_flag"]:
        log.debug("... Starting threshold draw")
        barplotbase.plot_threshold(ax, ydata)
        log.debug("Threshold: OK")
    
    if letter_code is not None and c["mark_prolines_flag"]:
        log.debug("... Starting Prolines Mark")
        experimentplotbase.text_marker(
            ax,
            range(num_of_bars),
            ydata,
            letter_code,
            {'P':c["mark_prolines_symbol"]},
            fs=c["mark_fontsize"],
            )
        log.debug("Prolines Marked: OK")
    
    if details is not None and c["mark_user_details_flag"]:
        log.debug("... Starting User Details Mark")
        experimentplotbase.text_marker(
            ax,
            range(num_of_bars),
            ydata,
            details[i],
            c["user_marks_dict"],
            fs=c["mark_fontsize"],
            )
        log.debug("User marks: OK")
    
    if details is not None and c["color_user_details_flag"]:
        log.debug("... Starting User Colors Mark")
        experimentplotbase.set_item_colors(
            bars,
            details[i],
            c["user_bar_colors_dict"],
            )
        log.debug("Color user details: OK")
           
    if theo_pre is not None \
            and tag_position is not None \
            and c["plot_theoretical_pre"]:
        
        experimentplotbase.plot_theo_pre(
            ax,
            range(num_of_bars),
            theo_pre[i],
            orientation='h',
            )
        
        tag_found = experimentplotbase.finds_paramagnetic_tag(
            bars,
            tag_position[i],
            )
        
        if tag_found:
            experimentplotbase.draw_paramagnetic_tag(
                ax,
                tag_found,
                y_max,
                plottype='h',
                )
    
    return


@plotdecorators.check_barplot_args
def plot(
        values,
        labels,
        header="",
        suptitles=None,
        letter_code=None,
        peak_status=None,
        details=None,
        threshold=None,
        tag_position=None,
        theo_pre=None,
        **kwargs,
        ):
    """
    Plots according to the Extended Bar Plot Template.
    
    The Extended Bar Plot template draws wide Bar plots that are
    designed to fit one page with. Bar Plots represent parameters
    for each residue individually in the form of bars.
    
    Subplots, one for each peaklist, i.e. experiment, are stacked
    sequentially from top to bottom.
    
    Parameters
    ----------
    values : np.array shape (y,x), dtype=float
        where X (axis=1) is the data to plot for each column,
        Y (axis=0) is the evolution of that data along the titration.
        
    labels : sequence type of length values.shape[1]
        Bar labels which are drawn as xtick labels.
    
    header : str
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space.
    
    suptitles : iterable type of strings
        Titles of each subplot, length must be equal to values.shape[0].

    letter_code : sequence type
        1-letter code of the protein sequence, should have length equal
        to <labels>.

    peak_status : np.array shape (y,x), dtype=str
        Peak status information according to core.utils.peak_status
        dictionary.

    details : np.array shape (y,x), dtype=str
        Peaklist Details column information.
    
    threshold : float
        The Y value of the threshold line.
    
    theo_pre : np.array shape (y,x), dtype=str
        Information on theoretical PRE data.

    tag_position : np.array shape (y,x), dtype=str
        Null values where tag not present, "*" character denotes
        the position of the of the paramagnetic tag.
    
    **kwargs : accepts **kwargs
        Plot details (colors, shapes, fonts, ...) can be highly
        configured through additional kwargs parameters.
        
        The available kwargs are stored in a default configuratio
        dictionary that can be obtained through the module's
        .get_config() or .prin_config() functions.
        
        This dictionary can be modified and passed enterilly to the
        function call, do not forget the unpacking operator (**),
        or, instead if individual arguments are passed, those will
        update the default configuration.
        
        If no **kwargs are provided, the default configuration dictionary 
        is used.
    """
    
    config = {**_default_config, **kwargs}
    
    """Runs all operations to plot."""
    num_subplots = experimentplotbase.calc_num_subplots(values)
    
    figure, axs  = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    for i in range(values.shape[0]):
        
        log.debug("Starting subplot no: {}".format(i))
        # other parameters are not passed because they are None by default
        # and may lead to IndexError
        _subplot(
            axs[i],
            values[i],
            labels,
            config,
            i,
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
