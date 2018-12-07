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

import core.fslibs.Logger as Logger
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarExtendedHorizontal(BarPlotBase):
    """
    Plots the Extended Horizontal Bar Plot template.
    
    Subplots have the width of the figure and one subplot is plotted for
    each experiment. Each value in <values> is represented by a bar and
    each bar is labeled according to <labels>.
    """
    
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
            labels,
            config={},
            **kwargs
            ):
        
        # initializes logger
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedHorizontal initiated")
        
        # sets configuration
        self.logger.debug("Config received: {}".format(config))
        self._config = BarExtendedHorizontal._default_config.copy()
        self._config.update(config)
        self.logger.debug("Config updated: {}".format(self._config))
        
        super().__init__(
            values,
            labels,
            config=self._config.copy(),
            **kwargs
            )
    
    def subplot(self, ax, values, subtitle, i):
        """Configures subplot."""
        
        ###################
        # configures vars
        c = self._config
        ydata = np.nan_to_num(values).astype(float)
        self.logger.debug("ydata: {}".format(ydata))
        num_of_bars = ydata.shape[0]
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
        # Configures X ticks and axis
        
        # Define tick spacing
        for j in range(101,10000,100):
            if j>num_of_bars:
                mod_ = j//100
                break
        self.logger.debug("Tick spacing set to: {}".format(mod_))
        
        # get xticks and xticks_labels to be represented
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
            print(i)
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

if __name__ == "__main__":
    
    ######################################################################## 1
    ############ Short data set
    
    values = np.full((7,15), 0.2)
    labels = np.arange(1, len(values[0])+1).astype(str)
    
    c = {"figure_path": "bar_extended_1_short.pdf"}
    plot1 = BarExtendedHorizontal(values, labels, config=c)
    plot1.plot()
    
    ######################################################################## 2
    ############ Large data set
    
    values = np.full((2,765), 0.2)
    labels = np.arange(1, len(values[0])+1).astype(str)
    
    c = {"figure_path": "bar_extended_2_large.pdf"}
    plot1 = BarExtendedHorizontal(values, labels, config=c)
    plot1.plot()
    
    ######################################################################## 2
    ############ Mark details
    
    values = np.random.random((3,100)) - 0.5
    labels = np.arange(1, len(values[0])+1).astype(str)
    aa = ['P','A']
    letter = np.random.choice(aa, values.shape[1], p=[0.1,0.9])
    mask = np.where(letter=='P')
    values[:,mask] = np.nan
    
    dd = ['None','foo','bar','boo']
    details = np.random.choice(dd, values.shape[1])
    details = np.stack([details, details, details], axis=0)
    print(details.shape == values.shape)
    details[:, mask] = "None"
    
    c = {
        "y_lims":(-1,1),
        "figure_path": "bar_extended_3_mark.pdf",
        "mark_prolines_flag": True,
        "mark_user_details_flag": True,
        "color_user_details_flag": True,
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
            }
    
    plot1 = BarExtendedHorizontal(
        values, labels, config=c, letter_code=letter, details=details)
    plot1.plot()
    
    
    # import os
    
    # file_name = os.path.realpath(__file__)
    
    # ######################################################################## 1
    
    # print("### testing {}".format(file_name))
    
    # dataset_path = os.path.join(
        # os.path.dirname(file_name),
        # 'testing',
        # 'csps'
        # )
        
    # print("testing dataset: {}".format(dataset_path))
    
    # a = []
    # for f in sorted(os.listdir(dataset_path)):
        # print("reading: {}".format(f))
        # a.append(
            # np.genfromtxt(
                # os.path.join(dataset_path, f),
                # delimiter=',',
                # skip_header=1,
                # dtype=str,
                # missing_values='NaN'
                # )
            # )
    
    # full_data_set = np.stack(a, axis=0)
    # print("dataset shape: {}".format(full_data_set.shape))
    
    # plot = BarExtendedHorizontal(
        # full_data_set[:,:,21].astype(float),
        # full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        # partype='ppm',
        # exp_names=["0","25","50","100","200","400","500"]
        # )
    
    # plot.plot()
    # plot.save_figure("csps.pdf")
    
    # ################################## 1.2
    
    # plot = BarExtendedHorizontal(
        # full_data_set[:,:,19].astype(float),
        # full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        # partype='ppm',
        # exp_names=["0","25","50","100","200","400","500"],
        # PRE_loaded=False
        # )
    
    # plot.config["y_lims"] = (-0.3,0.3)
    # plot.plot()
    # plot.save_figure("1H_delta.pdf")
    
    # ######################################################################## 2
    
    # dataset_path = os.path.join(
        # os.path.dirname(file_name),
        # 'testing',
        # 'dpre'
        # )
        
    # print("testing dataset: {}".format(dataset_path))
    
    # a = []
    # for f in sorted(os.listdir(dataset_path)):
        # print("reading: {}".format(f))
        # a.append(
            # np.genfromtxt(
                # os.path.join(dataset_path, f),
                # delimiter=',',
                # skip_header=1,
                # dtype=str,
                # missing_values='NaN'
                # )
            # )
    
    # full_data_set = np.stack(a, axis=0)
    # print("dataset shape: {}".format(full_data_set.shape))
    
    # pre_args = {
        # "PRE_loaded":True,
        # "series_axis":'along_z',
        # "para_name":"para"
        # }
    
    # plot = BarExtendedHorizontal(
        # full_data_set[:,:,19].astype(float),
        # full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        # data_extra=full_data_set[:,:,[21, 22]],
        # partype='ratio',
        # exp_names=["dia", "para"],
        # **pre_args
        # )
    
    # plot.config["y_lims"] = (0, 1.1)
    # plot.plot()
    # plot.save_figure("dpre.pdf")
    
    # ######################################################################## 3
    
    # dataset_path = os.path.join(
        # os.path.dirname(file_name),
        # 'testing',
        # 'dpre_not_complete'
        # )
        
    # print("testing dataset: {}".format(dataset_path))
    
    # a = []
    # for f in sorted(os.listdir(dataset_path)):
        # print("reading: {}".format(f))
        # a.append(
            # np.genfromtxt(
                # os.path.join(dataset_path, f),
                # delimiter=',',
                # skip_header=1,
                # dtype=str,
                # missing_values='NaN'
                # )
            # )
    
    # full_data_set = np.stack(a, axis=0)
    # print("dataset shape: {}".format(full_data_set.shape))
    
    # pre_args = {
        # "PRE_loaded":True,
        # "series_axis":'along_z',
        # "para_name":"para"
        # }
    
    # plot = BarExtendedHorizontal(
        # full_data_set[:,:,19].astype(float),
        # full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        # data_extra=full_data_set[:,:,[21, 22]],
        # partype='ratio',
        # exp_names=["dia", "para"],
        # **pre_args
        # )
    
    # plot.config["y_lims"] = (0, 1.1)
    # plot.plot()
    # plot.save_figure("dpre_not_complete.pdf")
