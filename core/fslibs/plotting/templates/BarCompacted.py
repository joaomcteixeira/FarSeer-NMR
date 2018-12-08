"""
Copyright © 2017-2018 Farseer-NMR Project

Find us at:

- J. BioMol NMR Publication:
    https://link.springer.com/article/10.1007/s10858-018-0182-5

- GitHub: https://github.com/Farseer-NMR

- Mail list: https://groups.google.com/forum/#!forum/farseer-nmr
    email: farseer-nmr@googlegroups.com

- Research Gate: https://goo.gl/z8dPJU

- Twitter: https://twitter.com/farseer_nmr

This file is part of the Farseer-NMR Project.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from matplotlib import pyplot as plt
from math import ceil

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.ExperimentPlot import ExperimentPlot
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarCompacted(BarPlotBase):
    """
    Compacted Bar plotting template.
    
    Parameters:
        - data (np.array(dtype=int) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                X) length=1. Is the column containing the calculated or observed NMR
                    parameter to be used as Y axis in plots,
                Y) are rows containing the X information for each residue
                Z) is [Y,X] for each experiment.
            Data can be further treated with data_select() method.
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but for columns ResNo, 1-letter, 3-letter, Peak Status, Merit,
            Fit Method, Vol. Method, Details; in this order.
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuraton. Access the default configuration
            via the default_config class attribute.
        
        - data_extra (opt, np.ndarray of shape [z,y,x]): extra ndarray to help
            on plotting the data passed as <data>.
                In the case of plotting theoretical PRE data, data_extra
                columns should be [Theo PRE, tag position].
        
        - partype (opt {'ppm', 'ratio'}, defaults None): 
            indicates the type of data that is being plotted, so that
            special option can be activated.
        
        - exp_names (opt, sequence type): list of the experiment names.
        
        - additional kwargs can be passed as **kwargs.
    
    """
    
    _default_config = {
        "cols_page": 3,
        "rows_page": 5,

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
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 6,
        "x_ticks_rot": 0,
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
        
        "unassigned_shade": True,
        "unassigned_shade_alpha": 0.5,
        
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
        
        "figure_header":"No header provided",
        "header_fontsize":5,
        
        "figure_path":"bar_extended_horizontal.pdf",
        "figure_dpi":300,
        "fig_height": 11.69,
        "fig_width": 8.69

        }
    
    def __init__(
            self,
            values,
            labels=None,
            config={},
            **kwargs
            ):
        
        # initializes logger
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedHorizontal initiated")
        
        # sets labels
        # CompactedBar plot does not requires labels specifically
        # yet BarPlotBase requires labels to be passed
        #
        # is not None avoids
        # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        labels = labels if labels is not None \
            else np.arange(1, values.shape[1]+1, step=1)
        
        # sets configuration
        self.logger.debug("Config received: {}".format(config))
        self._config = BarCompacted._default_config.copy()
        self._config.update(config)
        self.logger.debug("Config updated: {}".format(self._config))
        
        super().__init__(
            values,
            labels,
            config=self._config.copy(),
            **kwargs
            )
        
        return
    
    
    def subplot(self, ax, values, subtitle, i):
        """Configures subplot."""
        
        ###################
        # configures vars
        c = self._config
        ydata = np.nan_to_num(values).astype(float)
        self.logger.debug("ydata: {}".format(ydata))
        num_of_bars = ydata.size
        self.logger.debug("Number of bars to represented: {}".format(num_of_bars))
        self.logger.debug("Subtitle: {}".format(subtitle))
        
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
            subtitle,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            weight=c["subtitle_weight"]
            )
        
        self.logger.debug("Subplot title set to : {}".format(subtitle))
        
        ###################
        # Configures spines
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        self.logger.debug("Spines set: OK")
        
        ###################
        # Configures X ticks and X ticks labels
        
        try:
            self.labels.astype(int)
        except ValueError:
            labels_are_int = False
        else:
            labels_are_int = True
        
        if num_of_bars <= 10:
            xticks = np.arange(num_of_bars)
        
        else:
            number_of_ticks = num_of_bars
            mod_ = 10
            sanity_counter = 0
        
            if labels_are_int:
                tmp_labels = self.labels.astype(int)
                
                while number_of_ticks > 10 and sanity_counter < 100000:
                    
                    mask = np.where(tmp_labels % mod_ == 0)[0]
                    
                    xticks = np.arange(num_of_bars)[mask]
                    xticks_labels = tmp_labels[mask]
                    number_of_ticks = len(xticks)
        
                    mod_ *= 10
                    sanity_counter += 1
            
            elif not(labels_are_int):
                
                tmp_xticks = np.arange(num_of_bars)
        
                while number_of_ticks > 10 and sanity_counter < 100000:
                    
                    xticks = tmp_xticks[tmp_xticks % mod_ == 0]
                    xticks_labels = self.labels[xticks]
                    number_of_ticks = len(xticks)
        
                    mod_ *= 10
                    sanity_counter += 1
                
        self.logger.debug("sanity_counter: {}".format(sanity_counter))
        
        # set xticks and xticks_labels to be represented
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def subplot(self, ax, data, data_info, exp_name, data_extra=None):
        # """Configures subplot."""
        
        # c = self.config
        # col = self.info_cols
        # self.logger.debug("Starting Subplot ###### {}".format(exp_name))
        
        # data = np.nan_to_num(data)
        
        # self.logger.debug(data)
        # self.logger.debug(data_info)
        # self.logger.debug(data_extra)
        
        # number_of_residues_to_plot = data.shape[0]
        
        # self.logger.debug(
            # "Number of residues to plot: {}".format(number_of_residues_to_plot)
            # )
        
        # bars = ax.bar(
            # range(number_of_residues_to_plot),
            # data,
            # width=c["bar_width"],
            # align='center',
            # alpha=c["bar_alpha"],
            # linewidth=c["bar_linewidth"],
            # zorder=4
            # )
        
        # self.logger.debug("Created bar plot: OK")
        
        # for i in range(100,10000,100):
            # if i>number_of_residues_to_plot:
                # mod_ = i//10
                # break
        # self.logger.debug("tick mod: {}".format(mod_))
        
        # xticks = list()
        # xticklabels = list()
        # for k, m in zip(
                # range(number_of_residues_to_plot),
                # data_info[:,col["ResNo"]]
                # ):
            
            # if int(m)%mod_==0:
                # xticks.append(k)
                # xticklabels.append(m)
        
        # self.logger.debug("Setting xticks: {}".format(xticks))
        # self.logger.debug("xticklabels: {}".format(xticklabels))
        
        # ax.set_xticks(xticks)
        # self.logger.debug("set_xticks: OK")
        
        # ## https://github.com/matplotlib/matplotlib/issues/6266
        # ax.set_xticklabels(
            # xticklabels,
            # fontname=c["x_ticks_fn"],
            # fontsize=c["x_ticks_fs"],
            # fontweight=c["x_ticks_weight"],
            # rotation=c["x_ticks_rot"]
            # )
        # self.logger.debug("set_xticklabels: OK")
        
        # if c["unassigned_shade"]:
            # unassignedmask = \
                # data_info[:, col['Peak Status']] == 'unassigned'
            
            # for res, m in enumerate(unassignedmask):
                # if m:
                    # res -= 0.5
                    # ax.axvspan(
                        # res,
                        # res+1,
                        # color=c["unassigned_color"],
                        # alpha=c["unassigned_shade_alpha"],
                        # lw=0
                        # )
        
        # # Set subplot titles
        # ax.set_title(
            # exp_name,
            # y=c["subtitle_pad"],
            # fontsize=c["subtitle_fs"],
            # fontname=c["subtitle_fn"],
            # weight=c["subtitle_weight"]
            # )
        # self.logger.debug("Set title: OK")
        
        # # defines bars colors
        # self._set_item_colors(
            # bars,
            # data_info[:,col['Peak Status']],
            # {
                # 'measured': c["measured_color"],
                # 'missing': c["missing_color"],
                # 'unassigned': c["unassigned_color"]
                # }
            # )
        # self.logger.debug("set_item_colors: OK")
        
        # # configures spines
        # ax.spines['bottom'].set_zorder(10)
        # ax.spines['top'].set_zorder(10)
        # self.logger.debug("Spines set: OK")
        # # cConfigures YY ticks
        # ax.set_ylim(c["y_lims"][0], c["y_lims"][1])
        # ax.locator_params(axis='y', tight=True, nbins=8)
        # self.logger.debug("Set Y limits: OK")
        
        # ax.set_yticklabels(
            # ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
            # fontname=c["y_ticks_fn"],
            # fontsize=c["y_ticks_fs"],
            # fontweight=c["y_ticks_weight"],
            # rotation=c["y_ticks_rot"]
            # )
        # self.logger.debug("Set Y tick labels: OK")
        
        # # configures tick params
        # ax.margins(x=0.01)
        # ax.tick_params(
            # axis='x',
            # pad=c["x_ticks_pad"],
            # length=c["x_ticks_len"],
            # direction='out'
            # )
        # ax.tick_params(
            # axis='y',
            # pad=c["y_ticks_pad"],
            # length=c["y_ticks_len"],
            # direction='out'
            # )
        # self.logger.debug("Configured X and Y tick params: OK")
            
        # # Set axes labels
        # ax.set_xlabel(
            # 'Residue',
            # fontname=c["x_label_fn"],
            # fontsize=c["x_label_fs"],
            # labelpad=c["x_label_pad"],
            # weight=c["x_label_weight"],
            # rotation=0
            # )
        # ax.set_ylabel(
            # c["ylabel"],
            # fontsize=c["y_label_fs"],
            # labelpad=c["y_label_pad"],
            # fontname=c["y_label_fn"],
            # weight=c["y_label_weight"],
            # rotation=c["y_label_rot"]
            # )
        # self.logger.debug("Configured X and Y labels")
        
        # # Adds grid
        # if c["y_grid_flag"]:
            # ax.yaxis.grid(
                # color=c["y_grid_color"],
                # linestyle=c["y_grid_linestyle"],
                # linewidth=c["y_grid_linewidth"],
                # alpha=c["y_grid_alpha"],
                # zorder=0
                # )
            # self.logger.debug("Configured grid: OK")
        
        # # Adds red line to identify significant changes.
        # if c["threshold_flag"] and self.ppm_data:
            # self.logger.debug("... Starting Threshold draw")
            # self._plot_threshold(
                # ax,
                # data,
                # c["threshold_color"],
                # c["threshold_linewidth"],
                # c["threshold_alpha"],
                # zorder=c["threshold_zorder"]
                # )
            # self.logger.debug("Threshold: OK")
        
        # if c["mark_prolines_flag"]:
            # self.logger.debug("... Starting Prolines Mark")
            # self._text_marker(
                # ax,
                # range(number_of_residues_to_plot),
                # data,
                # data_info[:,col['1-letter']],
                # {'P':c["mark_prolines_symbol"]},
                # fs=c["mark_fontsize"]
                # )
            # self.logger.debug("Prolines Marked: OK")
        
        # if c["mark_user_details_flag"]:
            # self.logger.debug("... Starting User Details Mark")
            # self._text_marker(
                # ax,
                # range(number_of_residues_to_plot),
                # data,
                # data_info[:,col['Details']],
                # c["user_marks_dict"],
                # fs=c["mark_fontsize"]
                # )
            # self.logger.debug("User marks: OK")
        
        # if c["color_user_details_flag"]:
            # self.logger.debug("... Starting User Colors Mark")
            # self._set_item_colors(
                # bars,
                # data_info[:,col["Details"]],
                # c["user_bar_colors_dict"]
                # )
            # self.logger.debug("Color user details: OK")
        
        # self.logger.debug("PRE_Loaded Flag: {}".format(self.kwargs.get("PRE_loaded")))
        # self.logger.debug("Partype to be evaluated: {}".format(self.ratio_data))
        # if (self.kwargs.get("PRE_loaded") and self.ratio_data):
            
            # self.logger.debug("Passed first PRE test")
            # self._plot_pre_info(ax, data, data_info, data_extra, exp_name, orientation='h')
        
        # return

if __name__ == "__main__":
    import os
    
    file_name = os.path.realpath(__file__)
    
    print("### testing {}".format(file_name))
    
    ######################################################################## 1
    
    testing_path = os.path.join(
        os.path.dirname(file_name),
        os.pardir,
        'testing'
        )
    
    print("testing path: {}".format(testing_path))
    
    dataset_path = os.path.join(testing_path, 'csps')
        
    print("testing dataset: {}".format(dataset_path))
    
    a = []
    for f in sorted(os.listdir(dataset_path)):
        print("reading: {}".format(f))
        a.append(
            np.genfromtxt(
                os.path.join(dataset_path, f),
                delimiter=',',
                skip_header=1,
                dtype=str,
                missing_values='NaN'
                )
            )
    
    full_data_set = np.stack(a, axis=0)
    print("dataset shape: {}".format(full_data_set.shape))
    
    plot = BarCompacted(
        full_data_set[:,:,21].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        partype='ppm',
        exp_names=["0","25","50","100","200","400","500"]
        )
    
    plot.plot()
    plot.save_figure("csps.pdf")
    
    ########################################### 1.5
    
    plot = BarCompacted(
        full_data_set[:,:,19].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        partype='ppm',
        exp_names=["0","25","50","100","200","400","500"]
        )
    
    plot.config["y_lims"] = (-0.3,0.3)
    plot.plot()
    plot.save_figure("1H_delta.pdf")
    
    ######################################################################## 1
    
    dataset_path = os.path.join(testing_path, 'csps_not_complete')
        
    print("testing dataset: {}".format(dataset_path))
    
    a = []
    for f in sorted(os.listdir(dataset_path)):
        print("reading: {}".format(f))
        a.append(
            np.genfromtxt(
                os.path.join(dataset_path, f),
                delimiter=',',
                skip_header=1,
                dtype=str,
                missing_values='NaN'
                )
            )
    
    full_data_set = np.stack(a, axis=0)
    print("dataset shape: {}".format(full_data_set.shape))
    
    plot = BarCompacted(
        full_data_set[:,:,21].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        partype='ppm',
        exp_names=["400","500"]
        )
    
    plot.plot()
    plot.save_figure("csps_not_complete.pdf")
    
    ######################################################################## 2
    
    dataset_path = os.path.join(testing_path, 'dpre')
        
    print("testing dataset: {}".format(dataset_path))
    
    a = []
    for f in sorted(os.listdir(dataset_path)):
        print("reading: {}".format(f))
        a.append(
            np.genfromtxt(
                os.path.join(dataset_path, f),
                delimiter=',',
                skip_header=1,
                dtype=str,
                missing_values='NaN'
                )
            )
    
    full_data_set = np.stack(a, axis=0)
    print("dataset shape: {}".format(full_data_set.shape))
    
    pre_args = {
        "PRE_loaded":True,
        "series_axis":'along_z',
        "para_name":"para"
        }
    
    plot = BarCompacted(
        full_data_set[:,:,19].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        data_extra=full_data_set[:,:,[21, 22]],
        partype='ratio',
        exp_names=["dia", "para"],
        **pre_args
        )
    
    plot.config["y_lims"] = (0, 1.1)
    plot.plot()
    plot.save_figure("dpre.pdf")
    
    ######################################################################## 3
    
    dataset_path = os.path.join(testing_path, 'dpre_not_complete')
        
    print("testing dataset: {}".format(dataset_path))
    
    a = []
    for f in sorted(os.listdir(dataset_path)):
        print("reading: {}".format(f))
        a.append(
            np.genfromtxt(
                os.path.join(dataset_path, f),
                delimiter=',',
                skip_header=1,
                dtype=str,
                missing_values='NaN'
                )
            )
    
    full_data_set = np.stack(a, axis=0)
    print("dataset shape: {}".format(full_data_set.shape))
    
    pre_args = {
        "PRE_loaded":True,
        "series_axis":'along_z',
        "para_name":"para"
        }
    
    plot = BarCompacted(
        full_data_set[:,:,19].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        data_extra=full_data_set[:,:,[21, 22]],
        config={"y_lims":(0,1.1)},
        partype='ratio',
        exp_names=["dia", "para"],
        **pre_args
        )
    
    plot.plot()
    plot.save_figure("dpre_not_complete.pdf")
