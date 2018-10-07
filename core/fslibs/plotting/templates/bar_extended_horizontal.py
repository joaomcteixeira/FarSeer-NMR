import numpy as np
from matplotlib import pyplot as plt

from core.fslibs.plotting import plot_base
from core.fslibs.plotting import residue_plots_base
from core.fslibs.plotting import barplot_base
from core.fslibs.plotting import plotting_checks

import core.fslibs.Logger as Logger
from core.utils import aal1tol3


default_config = {
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
    
    "plot_theoretical_pre":False,
    "theo_pre_color": "red",
    "theo_pre_lw": 1.0,
    "tag_id":"*",
    
    "tag_cartoon_color": "black",
    "tag_cartoon_lw": 1.0,
    "tag_cartoon_ls": "-",
    
    "measured_color": "black",
    "missing_color": "red",
    "unassigned_color": "lightgrey",
    
    "bar_width": 0.8,
    "bar_alpha": 1,
    "bar_linewidth": 0,
    
    "threshold_flag": True,
    "threshold_color": "red",
    "threshold_linewidth": 0.5,
    "threshold_alpha": 0.8,
    "threshold_zorder":10,
    
    "mark_fontsize": 4,
    "mark_prolines_flag": True,
    "mark_prolines_symbol": "P",
    "mark_user_details_flag": True,
    "color_user_details_flag": True,
    "user_marks_dict": {
        "foo": "f",
        "mal": "m",
        "bem": "b"
    },
    "user_bar_colors_dict": {
        "foo": "green",
        "mal": "yellow",
        "bem": "magenta"
    },
    
    "hspace": 0.5,
    "wspace": 0.5,
    
    "figure_header":"No header provided",
    "header_fontsize":5,
    
    "figure_path":"bar_extended_horizontal.pdf",
    "figure_dpi":300,
    "fig_height": 11.69,
    "fig_width": 8.69
}

def _check_data_info_1letter(array):
    for char in array:
        if not(char in aal1tol3.keys()):
            return False
    else:
        return True
    
    

def bar_extended_horizontal(
        values,
        labels,
        config=None,
        data_extra=None,
        subtitles=None
        ):
    """
    Plots the Horizontal Bar Plot template.
    
    Subplots have the width of the figure and one subplot is plotted for
    each experiment. Each value in <values> is represented by a bar and
    each bar is labeled according to <labels>.
    
    Parameters:
    
        - values (np.array shape (z,y), dtype=str,float): where the second (y)
            axis encloses the Y data information for each bar and the first
            (z) axis the evolution of that data along a series of experiments.
            
        - labels (np.array shape (x,), dtype=str): Bar labels presented
            sequentially and synchronized with values.
            
        - config (opt, dict): a config dictionary that updates the
            module.default_config. Default values will be used for keys
            not provided.
        
        - data_extra (opt, np.array of shape (z,y,x)): contains additional
            information that can be used to improve data representation.
            Z and Y axis have the same meaning as for <labels>. X represent
            information-rich columns. Axis 0 (x, columns) data should be
            provided according to the order:
                ["1-letter",
                "Peak Status",
                "Details" (opt),
                "Theoretical PRE" (opt),
                "tag position" (opt)]
        
        - subtitles (list of strings): titles of each subplot, length must
            be equal to values.shape[0].
    """
    
    logger = Logger.FarseerLogger(__name__).setup_log()
    logger.info("Starting Bar Extended Plot")
    
    # initiates bool variables
    # set to False until confirmation of validity
    info = False
    _1letter = False
    peak_status = False
    details = False
    theo_pre = False
    logger.debug("All information params set to False")
    
    # updates configuration dictionary
    c = default_config.update(config).copy()
    
    # calculates the number of subplots the figure will contain
    num_subplots = residue_plots_base.calcs_subplots()
    
    # creates figure and subplot axes
    fig, axs = plotbase.build_figure(num_subplots)
    
    for i in range(values.shape[1]):
        
        logger.debug("Starting Subplot ###### {}".format(i))
        
        ###################
        # configures vars
        ax = axs[i]
        ydata = np.nan_to_num(values[:,i])
        logger.debug("ydata: {}".format(ydata))
        num_of_bars = ydata.shape[0]
        logger.debug("Number of bars to represented: {}".format(num_of_bars))
        subtitle = subtitles[i]
        logger.debug("Subtitle: {}".format(subtitle))
        
        if data_extra:
            info = data_extra[i,:,:]
            
            _1letter = plotting_checks.check_info_1letter(info[:,0])
            logger.debug("1-letter info valid: {}".format(_1letter))
            
            peak_status = plotting_checks.check_info_peak_status(info[:,1])
            logger.debug("Peak Status info valid: {}".format(peak_status))
            
            if info.shape[-1] >= 3:
                details = plotting_checks.check_info_details(info[:,2])
                logger.debug("Details info valid: {}".format(details))
            
            if data_extra.shape[-1] >= 4:
                theo_pre = plotting_checks.check_info_theo_pre(info[:,3])
                logger.debug("Theor. PRE info valid: {}".format(theo_pre))
            
            logger.debug("Is all info valid?: {}".format(info_valid)
        
        ###################
        # Plots bars
        bars = ax.bar(
            range(num_of_bars),
            ydata,
            width=c["bar_width"],
            align='center',
            alpha=c["bar_alpha"],
            linewidth=c["bar_linewidth"],
            zorder=4
            )
        
        logger.debug("Number of bars plotted: {}".format(len(bars)))
        logger.debug("Number of expected bars equals num of bars: {}".format(num_of_bars == len(bars)))
        
        ###################
        # Set subplot title
        ax.set_title(
            subtitle,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            weight=c["subtitle_weight"]
            )
        
        logger.debug("Subplot title set to : {}".format(subtitle))
        
        ###################
        # Configures spines
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        logger.debug("Spines set: OK")
        
        ###################
        # Configures X ticks and axis
        
        # Define tick spacing
        for i in range(100,10000,100):
            if i>num_of_bars:
                mod_ = i//100
                break
        logger.debug("Tick spacing set to: {}".format(mod_))
        
        # get xticks and xticks_labels to be represented
        xticks = ydata[0::mod_]
        xticks_labels = labels[0::mod_]
        
        logger.debug("xticks represented: {}".format(xticks))
        logger.debug("xticks labels represented: {}".format(xtick_labels))
        
        # Set X ticks
        ax.set_xticks(xticks)
        
        # Set X ticks labels
        ## https://github.com/matplotlib/matplotlib/issues/6266
        ax.set_xticklabels(
            xticks_labels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        
        # Set xticks params
        ax.tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        logger.debug("Configured X tick params: OK")
        
        # Set X axis label
        ax.set_xlabel(
            c["x_label"],
            fontname=c["x_label_fn"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            weight=c["x_label_weight"],
            rotation=0
            )
        logger.debug("Set X label: OK")
        
        ###################
        # Configures Y ticks and axis
        
        # sets axis limits
        ymin = c["y_lims"][0]
        ymax = c["y_lims"][1]
        ax.set_ylim(ymin, ymax)
        logger.debug("Set y max {} and ymin {}".format(ymin, ymax))
        
        # sets number of y ticks
        ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
        
        # sets y tick labels
        ax.set_yticklabels(
            ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        logger.debug("Set Y tick labels: OK")
        
        # sets y ticks params
        ax.tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        logger.debug("Configured Y tick params: OK")
        
        # set Y label
        ax.set_ylabel(
            c["y_label"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=c["y_label_rot"]
            )
        logger.debug("Set Y label: OK")
        
        ###################
        # Additional configurations
        ax.margins(x=0.01, tight=True)
        
        # defines bars colors
        if peak_status:
            barplot_base.set_item_colors(
                bars,
                info[:,1],
                {
                    'measured': c["measured_color"],
                    'missing': c["missing_color"],
                    'unassigned': c["unassigned_color"]
                    }
                )
            logger.debug("set_item_colors: OK")
        
        ###################
        # Additional representation features
        
        # Adds grid
        if c["y_grid_flag"]:
            ax.yaxis.grid(
                color=c["y_grid_color"],
                linestyle=c["y_grid_linestyle"],
                linewidth=c["y_grid_linewidth"],
                alpha=c["y_grid_alpha"],
                zorder=0
                )
            logger.debug("Configured grid: OK")
        
        # defines xticks colors
        if peak_status and c["x_ticks_color_flag"]:
            logger.debug("Configuring for x_ticks_color_flag...")
            barplot_base.set_item_colors(
                ax.get_xticklabels(),
                info[0::mod_,1],
                {
                    'measured':c["measured_color"],
                    'missing':c["missing_color"],
                    'unassigned':c["unassigned_color"]
                    }
                )
            logger.debug("...Done")
        
        # Adds red line to identify significant changes.
        if c["threshold_flag"]:
            logger.debug("... Starting threshold draw")
            barplot_base.plot_threshold(
                ax,
                ydata,
                c["threshold_color"],
                c["threshold_linewidth"],
                c["threshold_alpha"],
                zorder=c["threshold_zorder"]
                )
            logger.debug("Threshold: OK")
        
        if _1letter and c["mark_prolines_flag"]:
            logger.debug("... Starting Prolines Mark")
            barplot_base.text_marker(
                ax,
                range(num_of_bars),
                ydata,
                info[:,0],
                {'P':c["mark_prolines_symbol"]},
                fs=c["mark_fontsize"]
                )
            logger.debug("Prolines Marked: OK")
        
        if details and c["mark_user_details_flag"]:
            logger.debug("... Starting User Details Mark")
            barplot_base.text_marker(
                ax,
                range(num_of_bars),
                data,
                info[:,2],
                c["user_marks_dict"],
                fs=c["mark_fontsize"]
                )
            logger.debug("User marks: OK")
        
        if details and c["color_user_details_flag"]:
            logger.debug("... Starting User Colors Mark")
            barplot_base.set_item_colors(
                bars,
                info[:,2],
                c["user_bar_colors_dict"]
                )
            logger.debug("Color user details: OK")
               
        if theo_pre and c["plot_theoretical_pre"]:
            
            barplot_base.plot_theo_pre(
                ax,
                range(num_of_bars),
                info[:,3],
                pre_color=c["theo_pre_color"],
                pre_lw=c["theo_pre_lw"],
                orientation='h'
                )
            
            tag_position = barplot_base.finds_paramagnetic_tag(
                bars,
                info[:,4],
                identifier=c["tag_id"]
                )
            
            if tag_position:
                barplot_base.draw_paramagnetic_tag(
                    ax,
                    tag_position,
                    y_max,
                    plottype='h',
                    tag_color=c["tag_cartoon_color"],
                    tag_ls=c["tag_cartoon_ls"],
                    tag_lw=c["tag_cartoon_lw"]
                    )
    else:
        plot_base.clean_subplots(num_subplots, len(axs))
        plot_base.save_figure(
            path=c["figure_path"],
            dpi=c["figure_dpi"],
            height=c["fig_height"],
            width=c["fig_width"]
            )
    return
