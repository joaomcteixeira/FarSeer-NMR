"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

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

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarExtended(PlottingBase):
    """Extended Bar plotting template."""
    
    def __init__(self, data, config, selection_col):
        super.__init__(data, config, selection_col)
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logge.debug("BarExtendedHorizontal initiated")
        
        self.logger.debug("Column Selected: {}".format(self.sel))
        self.logger.debug("Configuration dictionary \n{}".format(self.config))
        self.logger.debug("Shape of data matrix: {}".format(self.data.shape))
        
        self.ppm_data = False
        self.ratio_data = False
        
        if self.sel in ('H1_delta', 'N15_delta', 'CSP'):
            self.ppm_data = True
        
        elif self.sel in ('Height_ratio','Vol_ratio'):
            self.ratio_data = True
        
        self.logger.debug("PPM and RATIO data types? {} and {}"\
            .format(self.ppm_data, self.ratio_data)
            
        self.experiment_names = self.data.items
        self.logger.debug("Experiment names: {}".format(self.experiment_names))
        
        self._calcs_numsubplots()
    
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
    
    def data_select(self):
        """
        Selects exact data to plot.
        
        Stores:
            - self.data_to_plot (np.array of shape [z,y,x]).
        """
        
        # fillna(0) is added because nan conflicts with text_maker()
        # in bar.get_height() which return nan
        self.data_to_plot = np.array(self.data.loc[:,:,self.sel].fillna(0))
        self.logger.debug(
            "Shape of selected data {}".format(self.data_to_plot.shape)
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
        
        for i, data_array in enumerate(self.data_to_plot):
            self.logger.debug("Starting subplot no: {}".format(i))
            data_info = self.data.iloc[i]
            self.subplot(data_array, data_info, i)
            
            
            #fig.subplots_adjust(hspace=hspace)
    
    def subplot(self, data_array, data_info, i):
        """Configures subplot."""
        
        c = self.config
        
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
        
        ticklabels = \
            data_info.loc[0::xtick_spacing,['ResNo','1-letter']].\
                apply(lambda x: ''.join(x), axis=1)
        
        self.logger.debug("Number of xticklabels: {}".format(len(ticklabels)))
        
        # Configure XX ticks and Label
        axs[i].set_xticks(number_of_residues_to_plot)
        self.logger.debug("set_xticks: OK")
        
        ## https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_xticklabels(
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
                axs[i].get_xticklabels(),
                data_info.loc[0::xtick_spacing,'Peak Status'],
                {
                    'measured':c["measured_color",
                    'missing':c["missing_color"],
                    'unassigned':c["unassigned_color"]
                    }
                )
            self.logger.debug("...Done")
        
        # Set subplot titles
        axs[i].set_title(
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
            data_info.loc[:,'Peak Status'],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"]
                }
            )
        self.logger.debug("set_item_colors: OK")
        
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        self.logger.debug("Spines set: OK")
        # cConfigures YY ticks
        axs[i].set_ylim(c["y_lims"][0], c["y_lims"][1])
        axs[i].locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
        self.logger.debug("Set Y limits: OK")
        
        axs[i].set_yticklabels(
            ['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        self.logger.debug("Set Y tick labels: OK")
        
        # configures tick params
        axs[i].margins(x=0.01)
        axs[i].tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        axs[i].tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        self.logger.debug("Configured X and Y tick params: OK")
            
        # Set axes labels
        axs[i].set_xlabel(
            'Residue',
            fontname=c["x_label_fn"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            weight=c["x_label_weight"],
            rotation=c["x_label_rot"]
            )
        axs[i].set_ylabel(
            ylabel,
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=c["y_label_rot"]
            )
        self.logger.debug("Configured X and Y labels")
        
        # Adds grid
        if y_grid_flag:
            axs[i].yaxis.grid(
                color=c["y_grid_color"],
                linestyle=c["y_grid_linestyle"],
                linewidth=c["y_grid_linewidth"],
                alpha=c["y_grid_alpha"],
                zorder=0
                )
            self.logger.debug("Configured grid: OK")
        
        # Adds red line to identify significant changes.
        if c["threshold_flag"] and self.ppm_data:
            self._plot_threshold(
                axs[i],
                data_array,
                c["threshold_color"],
                c["threshold_linewidth"],
                c["threshold_alpha"],
                zorder=c["threshold_zorder"]
                )
            self.logger.debug("Threshold: OK")
        
        if c["mark_prolines_flag"]:
            self._text_marker(
                axs[i],
                bars,
                data_info.loc[:,'1-letter'],
                {'P':c["mark_prolines_symbol"]},
                c["y_lims"][1],
                fs=c["mark_fontsize"]
                )
            self.logger.debug("Prolines Marked: OK")
        
        if c["mark_user_details_flag"]:
            self._text_marker(
                axs[i],
                bars,
                data_info.loc[:,'Details'],
                c["user_marks_dict"],
                c["y_lims"][1],
                fs=c["mark_fontsize"]
                )
            self.logger.debug("User marks: OK")
        
        if c["color_user_details_flag"]:
            self._set_item_colors(
                bars,
                data_info.loc[:,'Details'],
                c["user_bar_colors_dict"]
                )
            self.logger.debug("Color user details: OK")
        
        if self.data.PRE_loaded and self.ratio_data:
            self._plot_theo_pre(
                axs[i],
                self.experiment_names[i],
                c["y_lims"][1]*0.05,
                bartype='h',
                pre_color=c["theo_pre_color"],
                pre_lw=c["theo_pre_lw"],
                tag_color=c["tag_cartoon_color"],
                tag_ls=c["tag_cartoon_ls"],
                tag_lw=c["tag_cartoon_lw"]
                )
            self.logger.debug("DeltaPRE plotted: OK")
        
        return
