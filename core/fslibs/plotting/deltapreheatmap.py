import numpy as np
import json

from matplotlib import pyplot as plt

from core.fslibs import Logger
from plotlibs import (
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
    
    "top_margin":0.9,
    "right_margin": 0.22,
    "bottom_margin": 0,
    
    "cbar_font_size": 4,
    
    "tag_line_color": "red",
    "tag_line_ls": "-",
    "tag_line_lw": 0.8,
    
    "hspace": 0,
    "rightspace": 0.3,
    }


def _validate_config(config):
    """
    Validate config dictionary for DeltaPRE Heat Map Plot template.
    
    Loops over config keys and checks if values' type are the
    expected. Raises ValueError otherwise.
    
    Parameters
    ----------
    config : dict
        The configuration dictionary
    """
    
    def eval_types(key, value):
        
        a = type(config[key])
        b = type(value)
        
        if not(a == b):
             msg = (
                f"Argument '{key}' in DetalPRE Heat Map Plot is not of "
                f"correct type, is {a}, should be {b}."
                )
             log.info(msg)
             raise TypeError(msg)
    
    
    for key, value in _default_config.items():
        eval_types(key, value)
    
    msg = "Parameters type for DeltaPRE Heat Map Plot evaluated successfully"
    log.debug(msg)
    return


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
                plottype = 'heatmap',
                )
        else:
            log.debug("Paramagnetic tag not found, ignoring...")

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
    Plots according to the DetalPRE Heat Map Plot Template.
    
    The DetalPRE Heat Map Plot template draws wide Bar plots that are
    designed to fit one page with. Bar Plots represent parameters
    for each residue individually in the form of bars.
    
    Subplots, one for each peaklist, i.e. experiment, are stacked
    sequentially from top to bottom.
    
    Parameters
    ----------
    values : np.ndarray shape (y,x), dtype=float
        where X (axis=1) is the data to plot for each column,
        Y (axis=0) is the evolution of that data along the titration.
        
    labels : sequence type of length values.shape[1]
        Bar labels which are drawn as xtick labels.
    
    header : str, optional
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space. 
    
    suptitles : iterable type of strings, optional
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
    
    plotvalidators.validate_barplot_data(values, labels)
    
    suptitles = suptitles or [str(i) for i in range(values.shape[0])]
    
    plotvalidators.validate_barplot_additional_data(
        values,
        suptitles=suptitles,
        letter_code=letter_code,
        peak_status=peak_status,
        details=details,
        tag_position=tag_position,
        theo_pre=theo_pre,
        )
    
    config = {**_default_config, **kwargs}
    
    _validate_config(config)
    
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
            i,
            config,
            suptitles,
            letter_code,
            peak_status,
            details,
            tag_position,
            theo_pre,
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
    
    print_config()
    
    ######################################################################## 1
    ############ Short data set
    
    values = np.full((7,15), 0.2)
    labels = np.arange(1, len(values[0])+1).astype(str)
    
    c = {"figure_path": 1}
    plot(values, labels, header="oh my headeR!!!", **c)
