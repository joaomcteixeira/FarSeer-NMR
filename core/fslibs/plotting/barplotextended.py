
from plotlibs import plottingbase, experimentplotbase, barplotbase

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



def _subplot(
        ax,
        values,
        i,
        ):
    """Configures subplot."""
    
    ###################
    # configures vars
    c = self._config
    ydata = np.nan_to_num(values).astype(float)
    self.logger.debug("ydata: {}".format(ydata))
    num_of_bars = ydata.shape[0]
    self.logger.debug("Number of bars to represented: {}".format(num_of_bars))
    self.logger.debug("Subtitle: {}".format(subtitles[i]))
    
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
        zorder=4
        )
    
    self.logger.debug("Number of bars plotted: {}".format(len(bars)))
    self.logger.debug("Number of expected bars equals num of bars: {}".format(num_of_bars == len(bars)))
    
    ###################
    # Set subplot title
    ax.set_title(
        subtitles[i],
        y=c["subtitle_pad"],
        fontsize=c["subtitle_fs"],
        fontname=c["subtitle_fn"],
        weight=c["subtitle_weight"]
        )
    
    self.logger.debug("Subplot title set to : {}".format(subtitles[i]))
    
    ###################
    # Configures spines
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    self.logger.debug("Spines set: OK")
    
    ###################
    # Configures X ticks and axis
    
    # Define tick spacing
    for j in range(101,10000,100):
        if j>num_of_bars:
            mod_ = j//100
            break
    self.logger.debug("Tick spacing set to: {}".format(mod_))
    
    # set xticks and xticks_labels to be represented
    xticks = np.arange(len(bars))[0::mod_]
    xticks_labels = np.array(self.labels)[0::mod_]
    
    self.logger.debug("xticks represented: {}".format(xticks))
    self.logger.debug("xticks labels represented: {}".format(xticks_labels))
    
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
    self.logger.debug("Configured X tick params: OK")
    
    # Set X axis label
    ax.set_xlabel(
        c["x_label"],
        fontname=c["x_label_fn"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        weight=c["x_label_weight"],
        rotation=c["x_label_rotation"]
        )
    self.logger.debug("Set X label: OK")
    
    ###################
    # Configures Y ticks and axis
    
    # sets axis limits
    ymin = c["y_lims"][0]
    ymax = c["y_lims"][1]
    ax.set_ylim(ymin, ymax)
    self.logger.debug("Set y max {} and ymin {}".format(ymin, ymax))
    
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
    self.logger.debug("Set Y tick labels: OK")
    
    # sets y ticks params
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out'
        )
    self.logger.debug("Configured Y tick params: OK")
    
    # set Y label
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        rotation=c["y_label_rot"]
        )
    self.logger.debug("Set Y label: OK")
    
    ###################
    # Additional configurations
    # "is not None" is used in IF statements intentionally
    
    ax.margins(x=0.01, tight=True)
    
    # defines bars colors
    if self.peak_status is not None:
        self._set_item_colors(
            bars,
            self.peak_status[i],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"]
                }
            )
        self.logger.debug("set_item_colors: OK")
    
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
        self.logger.debug("Configured grid: OK")
    
    # defines xticks colors
    if self.peak_status is not None and c["x_ticks_color_flag"]:
        logger.debug("Configuring for x_ticks_color_flag...")
        self._set_item_colors(
            ax.get_xticklabels(),
            self.peak_status[i,0::mod_],
            {
                'measured':c["measured_color"],
                'missing':c["missing_color"],
                'unassigned':c["unassigned_color"]
                }
            )
        self.logger.debug("...Done")
    
    # Adds red line to identify significant changes.
    if c["threshold_flag"]:
        self.logger.debug("... Starting threshold draw")
        self._plot_threshold(ax, ydata)
        self.logger.debug("Threshold: OK")
    
    if self.letter_code is not None and c["mark_prolines_flag"]:
        self.logger.debug("... Starting Prolines Mark")
        self._text_marker(
            ax,
            range(num_of_bars),
            ydata,
            self.letter_code,
            {'P':c["mark_prolines_symbol"]},
            fs=c["mark_fontsize"]
            )
        self.logger.debug("Prolines Marked: OK")
    
    if self.details is not None and c["mark_user_details_flag"]:
        self.logger.debug("... Starting User Details Mark")
        self._text_marker(
            ax,
            range(num_of_bars),
            ydata,
            self.details[i],
            c["user_marks_dict"],
            fs=c["mark_fontsize"]
            )
        self.logger.debug("User marks: OK")
    
    if self.details is not None and c["color_user_details_flag"]:
        self.logger.debug("... Starting User Colors Mark")
        self._set_item_colors(
            bars,
            self.details[i],
            c["user_bar_colors_dict"]
            )
        self.logger.debug("Color user details: OK")
           
    if self.theo_pre is not None \
            and self.tag_position is not None \
            and c["plot_theoretical_pre"]:
        
        self._plot_theo_pre(
            ax,
            range(num_of_bars),
            self.theo_pre[i],
            orientation='h'
            )
        
        tag_found = self.finds_paramagnetic_tag(
            bars,
            self.tag_position[i]
            )
        
        if tag_found:
            self._draw_paramagnetic_tag(
                ax,
                tag_found,
                y_max,
                plottype='h'
                )
    
    return



@barplotbase.add_docstring
@experimentplotbase.add_docstring
@plottingbase.add_docstring
def plot(
        values,
        labels,
        header="",
        details=None,
        letter_code=None,
        peak_status=None,
        subtitles=None,
        tag_position=None,
        theo_pre=None,
        threshold=None,
        **kwargs,
        ):
    
    config = {**default_config, **kwargs}
    
    """Runs all operations to plot."""
    num_subplots = experimentplotbase.calc_num_subplots(values)
    
    figure, axs  = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        ) # from PlottingBase
    
    for i in range(values.shape[0]):
        
        logger.debug("Starting subplot no: {}".format(i))
        
        _subplot(axs[i], values[i], i, config)
    
    plottingbase.adjust_subplots(
        figure,
        config["hspace"],
        config["wspace"],
        ) # from PlottingBase
    
    plottingbase.clean_subplots(axs, num_subplots) # from PlottingBase
    
    plottingbase.save_figure(
        figure,
        config["figure_path"],
        header=header,
        header_fs=config["header_fontsize"],
        dpi=config["figure_dpi"],
        ) # from PlottingBase
    
    plt.close(figure)
    
    return
