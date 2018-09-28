"""
Copyright © 2017-2018 Farseer-NMR

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

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
import pandas as pd
from matplotlib import pyplot as plt
from math import ceil

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarExtended(PlottingBase, BarPlotBase):
    """
    Extended Bar plotting template.
    
    Parameters:
        - data (np.array(dtype=int) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                X) is the column containing the calculated or observed NMR
                    parameter to be used as Y axis in plots,
                Y) are rows containing the X information for each residue
                Z) is [Y,X] for each experiment.
            Data can be further treated with data_select() method.
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but for columns ResNo, 1-letter, 3-letter, Peak Status, Merit,
            Fit Method, Vol. Method, Details; in this order.
        
        - config (dict): a dictionary containing all the configuration
            parameters required for this plotting routine.
            Mandatory keys:
                - fig_height (float, inches)
                - fig_width (float, inches)
                - cols_per_page (int): columns of subplots per figure page
                - rows_per_page (int): rows of subplots per figure page
        
        - data_extra (opt, np.ndarray of shape [z,y,x]): extra ndarray to help
            on plotting the data passed as <data>.
                In the case of plotting theoretical PRE data, data_extra
                columns should be [Theo PRE, tag position].
        
        - partype (opt {'ppm', 'ratio'}, defaults None): 
            indicates the type of data that is being plotted, so that
            special option can be activated.
        
        - additional kwargs can be passed as **kwargs.
    
    """
    
    def __init__(self,
            data,
            data_info,
            config,
            data_extra=None,
            partype="",
            exp_names="",
            **kwargs
            ):
        super().__init__(data, data_info, data_extra, config, **kwargs)
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedHorizontal initiated")
        
        self.logger.debug("Column Selected: {}".format(partype))
        self.logger.debug("Configuration dictionary \n{}".format(self.config))
        self.logger.debug("Shape of data matrix: {}".format(self.data.shape))
        self.logger.debug("Kwargs: {}".format(self.kwargs))
        
        self.ppm_data = False
        self.ratio_data = False
        
        # for ('H1_delta', 'N15_delta', 'CSP')
        if partype == 'ppm' :
            self.ppm_data = True
        
        # for ('Height_ratio','Vol_ratio')
        elif partype == 'ratio':
            self.ratio_data = True
        
        self.logger.debug(
            "PPM and RATIO data types? {} and {}".format(
                self.ppm_data,
                self.ratio_data
                )
            )
        
        if exp_names:
            self.experiment_names = exp_names
        else:
            self.experiment_names = [str(i) for i in range(data.shape[0])]
            
        self.logger.debug("Experiment names: {}".format(self.experiment_names))
        
        self._calcs_numsubplots()
    
    def data_select(self):
        """dummy function to comply with ABC"""
        return
    
    def _calcs_numsubplots(self):
        """
        Calculates the total number of subplots to be plotted
        based on the user data.
        
        Returns:
            - None
            
        Stores:
            - self.num_subplots (int)
        """
        self.num_subplots = self.data.shape[0]
        self.logger.debug("Number of subplots: {}".format(self.num_subplots))
        
        return
    
    def _config_fig(self):
        """
        Calculates number of subplot rows per page based on
        user data and settings.
        
        Returns:
            - numrows (int): number of total rows
            - real_fig_height (float, inches): final figure height
        """
        
        numrows = ceil(self.num_subplots/self.config["cols_page"]) + 1 
        
        real_fig_height = \
            (self.config["fig_height"] / self.config["rows_page"]) \
                * numrows
        
        return numrows, real_fig_height
    
    def draw_figure(self, **kwargs):
        """
        Draws the figure architecture.
        
        Defines the size of the figure and subplots based
        on the data to plot.
        
        Returns:
            - None.
        
        Stores :
            - self.figure: Figure object.
            - self.axs: axes of the figure (in case matplotlib is used).
            - self.len_axs (int): the number of subplots created in the
                figure object.
        """
        
        numrows, real_fig_height = self._config_fig()
        
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        self.figure, self.axs = plt.subplots(
            nrows=numrows,
            ncols=self.config["cols_page"],
            figsize=(self.config["fig_width"], real_fig_height)
            )
        self.len_axs = len(self.axs)
        self.axs = self.axs.ravel()
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995],
            h_pad=real_fig_height/self.config["rows_page"]
            )
        
        return
    
    def plot_subplots(self, **kwargs):
        """
        Sends the specific data to each subplot.
        
        The way data is sliced from the whole data to plot matrix
        depends on the nature of the subplots.
        
        Returns:
            - None
        """
        
        for i in range(self.data.shape[0]):
            
            self.logger.debug("Starting subplot no: {}".format(i))
            
            if isinstance(self.data_extra, np.ndarray):
                data_extra = self.data_extra[i]
            else:
                data_extra = None
            
            self.subplot(
                i,
                self.data[i],
                self.data_info[i],
                data_extra=data_extra
                )
            
            
        self.figure.subplots_adjust(hspace=self.config["vspace"])
    
    def subplot(self, i, data_array, data_info, data_extra=None):
        """Configures subplot."""
        
        c = self.config
        col = self.info_cols
        self.logger.debug("Starting Subplot ###### {}".format(self.experiment_names[i]))
        self.logger.debug(data_array)
        self.logger.debug(data_info)
        self.logger.debug(data_extra)
        
        number_of_residues_to_plot = data_array.shape[0]
        
        self.logger.debug(
            "Number of residues to plot: {}".format(number_of_residues_to_plot)
            )
        
        bars = self.axs[i].bar(
            range(number_of_residues_to_plot),
            data_array,
            width=c["bar_width"],
            align='center',
            alpha=c["bar_alpha"],
            linewidth=c["bar_linewidth"],
            zorder=4
            )
        
        self.logger.debug("Created bar plot: OK")
        
        # ticks positions:
        # this is used to fit both applyFASTA=True or False
        # reduces xticks to 100 as maximum to avoid ticklabel overlap
        if number_of_residues_to_plot > 100:
            xtick_spacing = number_of_residues_to_plot//100
        
        else:
            xtick_spacing = 1
        
        self.logger.debug("xtick_spacing set to: {}".format(xtick_spacing))
        
        self.logger.debug("data ResNo: {}".format(data_info[0::xtick_spacing,col['ResNo']]))
        self.logger.debug("data 1-letter: {}".format(data_info[0::xtick_spacing,col['1-letter']]))
        
        ticklabels = \
            np.core.defchararray.add(
                np.copy(data_info[0::xtick_spacing,col['ResNo']]),
                np.copy(data_info[0::xtick_spacing,col['1-letter']])
                )
        
        self.logger.debug("Number of xticklabels: {}".format(len(ticklabels)))
        self.logger.debug("X Tick Labels. {}".format(ticklabels))
        
        # Configure XX ticks and Label
        self.axs[i].set_xticks(range(number_of_residues_to_plot))
        self.logger.debug("set_xticks: OK")
        
        ## https://github.com/matplotlib/matplotlib/issues/6266
        self.axs[i].set_xticklabels(
            ticklabels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        self.logger.debug("set_xticklabels: OK")
        
        # defines xticks colors
        if c["x_ticks_color_flag"]:
            self.logger.debug("Configuring x_ticks_color_flag...")
            self._set_item_colors(
                self.axs[i].get_xticklabels(),
                data_info[0::xtick_spacing,col['Peak Status']],
                {
                    'measured':c["measured_color"],
                    'missing':c["missing_color"],
                    'unassigned':c["unassigned_color"]
                    }
                )
            self.logger.debug("...Done")
        
        # Set subplot titles
        self.axs[i].set_title(
            self.experiment_names[i],
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            weight=c["subtitle_weight"]
            )
        self.logger.debug("Set title: OK")
        
        # defines bars colors
        self._set_item_colors(
            bars,
            data_info[:,col['Peak Status']],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"]
                }
            )
        self.logger.debug("set_item_colors: OK")
        
        # configures spines
        self.axs[i].spines['bottom'].set_zorder(10)
        self.axs[i].spines['top'].set_zorder(10)
        self.logger.debug("Spines set: OK")
        # cConfigures YY ticks
        self.axs[i].set_ylim(c["y_lims"][0], c["y_lims"][1])
        self.axs[i].locator_params(axis='y', tight=True, nbins=8)
        self.logger.debug("Set Y limits: OK")
        
        self.axs[i].set_yticklabels(
            ['{:.2f}'.format(yy) for yy in self.axs[i].get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        self.logger.debug("Set Y tick labels: OK")
        
        # configures tick params
        self.axs[i].margins(x=0.01)
        self.axs[i].tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        self.axs[i].tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        self.logger.debug("Configured X and Y tick params: OK")
            
        # Set axes labels
        self.axs[i].set_xlabel(
            'Residue',
            fontname=c["x_label_fn"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            weight=c["x_label_weight"],
            rotation=0
            )
        self.axs[i].set_ylabel(
            c["ylabel"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=c["y_label_rot"]
            )
        self.logger.debug("Configured X and Y labels")
        
        # Adds grid
        if c["y_grid_flag"]:
            self.axs[i].yaxis.grid(
                color=c["y_grid_color"],
                linestyle=c["y_grid_linestyle"],
                linewidth=c["y_grid_linewidth"],
                alpha=c["y_grid_alpha"],
                zorder=0
                )
            self.logger.debug("Configured grid: OK")
        
        # Adds red line to identify significant changes.
        if c["threshold_flag"] and self.ppm_data:
            self.logger.debug("... Starting Threshold draw")
            self._plot_threshold(
                self.axs[i],
                data_array,
                c["threshold_color"],
                c["threshold_linewidth"],
                c["threshold_alpha"],
                zorder=c["threshold_zorder"]
                )
            self.logger.debug("Threshold: OK")
        
        if c["mark_prolines_flag"]:
            self.logger.debug("... Starting Prolines Mark")
            self._text_marker(
                self.axs[i],
                bars,
                data_info[:,col['1-letter']],
                {'P':c["mark_prolines_symbol"]},
                c["y_lims"][1],
                fs=c["mark_fontsize"]
                )
            self.logger.debug("Prolines Marked: OK")
        
        if c["mark_user_details_flag"]:
            self.logger.debug("... Starting User Details Mark")
            self._text_marker(
                self.axs[i],
                bars,
                data_info[:,col['Details']],
                c["user_marks_dict"],
                c["y_lims"][1],
                fs=c["mark_fontsize"]
                )
            self.logger.debug("User marks: OK")
        
        if c["color_user_details_flag"]:
            self.logger.debug("... Starting User Colors Mark")
            self._set_item_colors(
                bars,
                data_info[:,col["Details"]],
                c["user_bar_colors_dict"]
                )
            self.logger.debug("Color user details: OK")
               
        if (self.kwargs["PRE_loaded"] and self.ratio_data):
            
            self.logger.debug("...Starting Theoretical PRE Plot")
            
            self.logger.debug("series_axis: {}".format(self.kwargs["series_axis"]))
            self.logger.debug("para_name: {}".format(self.kwargs["para_name"]))
            self.logger.debug("exp name: {}".format(self.experiment_names[i]))
            
            is_valid_for_PRE_plot_calc = \
                self.kwargs["series_axis"] == 'along_z' \
                    and self.kwargs["para_name"] == self.experiment_names[i]
            
            is_valid_for_PRE_plot_comp = \
                self.kwargs["series_axis"] == 'Cz' \
                    and (self.kwargs["next_dim"] in self.kwargs["paramagnetic_names"] \
                        or self.kwargs["prev_dim"] in self.kwargs["paramagnetic_names"])
            
            is_valid_for_PRE_plot = \
                is_valid_for_PRE_plot_calc or is_valid_for_PRE_plot_comp
            
            if is_valid_for_PRE_plot:
                # plot theoretical PRE
                self.logger.debug("... Starting Theoretical PRE Plot")
                
                self.logger.debug("data extra {}".format(data_extra[:,1]))
                where_tag = np.where(data_extra[:,1]=="*")
                self.logger.debug("where position: {}".format(where_tag))
                tag_position = list(range(number_of_residues_to_plot))[where_tag[0][0]]
                self.logger.debug("tag position: {}".format(tag_position))
                
                self._plot_theo_pre(
                    self.axs[i],
                    range(number_of_residues_to_plot),
                    data_extra[:,0],
                    tag_position,
                    c["y_lims"][1]*0.05,
                    bartype='h',
                    pre_color=c["theo_pre_color"],
                    pre_lw=c["theo_pre_lw"],
                    tag_color=c["tag_cartoon_color"],
                    tag_ls=c["tag_cartoon_ls"],
                    tag_lw=c["tag_cartoon_lw"]
                    )
                self.logger.debug("Theoretical PRE plotted: OK")
            else:
                self.logger.debug("Data is not valid for PRE Plot")
        
        return

if __name__ == "__main__":
    import os
    
    file_name = os.path.realpath(__file__)
    
    print("### testing {}".format(file_name))
    
    dataset_path = os.path.join(
        os.path.dirname(file_name),
        'testing',
        'csps'
        )
        
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
    
    config = {
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
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 6,
        "y_ticks_rot": 0,
        "y_ticks_pad": 1,
        "y_ticks_weight": "normal",
        "y_ticks_len": 2,
        "y_grid_flag": True,
        "y_grid_color": "lightgrey",
        "y_grid_linestyle": "-",
        "y_grid_linewidth": 0.2,
        "y_grid_alpha": 0.8,
        "vspace": 0.5,
        "theo_pre_color": "red",
        "theo_pre_lw": 1.0,
        "tag_cartoon_color": "black",
        "tag_cartoon_lw": 1.0,
        "tag_cartoon_ls": "-",
        "measured_color": "black",
        "status_color_flag": False,
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
        "cols_page": 1,
        "rows_page": 6,
        "x_ticks_fn": "monospace",
        "x_ticks_fs": 6,
        "x_ticks_rot": 90,
        "x_ticks_weight": "normal",
        "x_ticks_color_flag": True,
        "fig_dpi": 300,
        "fig_file_type": "pdf",
        "fig_height": 11.69,
        "fig_width": 8.69,
        "y_lims":(0,0.3),
        "ylabel":"CSPs"
    }
    
    plot = BarExtended(
        full_data_set[:,:,21].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        config,
        partype='ppm',
        exp_names=["0","25","50","100","200","400","500"],
        PRE_loaded=False
        )
    
    plot.plot()
    plot.save_figure("csps.pdf")
    
    dataset_path = os.path.join(
        os.path.dirname(file_name),
        'testing',
        'dpre'
        )
        
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
    
    config["y_lims"] = (0, 1.1)
    
    plot = BarExtended(
        full_data_set[:,:,19].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        config,
        data_extra=full_data_set[:,:,[21, 22]],
        partype='ratio',
        exp_names=["dia", "para"],
        **pre_args
        )
 
    plot.plot()
    plot.save_figure("dpre.pdf")
