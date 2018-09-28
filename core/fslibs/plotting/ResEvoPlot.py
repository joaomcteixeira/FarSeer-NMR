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
from matplotlib import pyplot as plt

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.ResiduePlot import ResiduePlot
from core.fslibs.WetHandler import WetHandler as fsw

class ResEvoPlot(ResiduePlot):
    """
    Represents the evolution of a given parameter along the whole series
    for each residue separately.
    """
    
    def __init__(self,
            data,
            data_info,
            config,
            data_extra=None,
            exp_names=None,
            **kwargs
            ):
        super().__init__(
            data,
            data_info,
            config,
            exp_names=exp_names,
            **kwargs
            )
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ResEvoPlot initiated")
        
        self.data_extra = data_extra
        
        return
    
    def subplot(self, ax, data, data_info):
        
        c = self.config
        col = self.info_cols
        
        # defines subplot title
        subtitle = \
            np.core.defchararray.add(
                np.copy(data_info[0,self.info_cols['ResNo']]),
                np.copy(data_info[0,self.info_cols['1-letter']])
                )
        
        
        # Draws subplot title
        ax.set_title(
            subtitle,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            fontweight=c["subtitle_weight"]
            )
        
        # if the user wants to represent the condition in the x axis
        # for the first dimension
        if c["set_x_values"] \
                and (self.kwargs["series_axis"] == 'along_x' \
                    or self.kwargs["dim_comparison"] == 'along_x'):
            
            if len(c["titration_x_values"]) != len(data):
                msg = \
"The number of coordinate values defined for fitting/data respresentation, \
<fitting_x_values> variable [{}], do not match the number of \
data points <along_x>, i.e. input peaklists. Please correct <fitting_x_values> \
variable or confirm you have not forgot any peaklist [{}].".\
                    format(c["titration_x_values"], data)
                
                wet = fsw(msg_title='ERROR', msg=msg, wet_num=5)
                wet.abort()
            
            x = np.array(c["titration_x_values"])
            xmin = x[0]
            xmax = x[-1]
            
        # for 2D and 3D analysis this option is not available
        elif (self.kwargs["series_axis"] in ['along_y', 'along_z']) \
                or (self.kwargs["dim_comparison"] in ['along_y', 'along_z']):
            x = np.arange(0, len(data))
            xmin = 0
            xmax = len(data)-1
            ax.set_xticks(x)
            xlabels = self.exp_names
            x_ticks_rot=45
        
        # just give a range for the x axis
        # in case representing the along_x without titration_x_values
        else:
            x = np.arange(0, len(data))
            ax.set_xticks(x)
            xmin = 0
            xmax = len(data)-1
            xlabels = x
        
        # Configure Axis Ticks
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(c["y_lims"][0], c["y_lims"][1])
        
        if c["set_x_values"] \
                and (self.kwargs["series_axis"] == 'along_x' \
                    or self.kwargs["dim_comparison"] == 'along_x'):
            ax.locator_params(axis='x', tight=True, nbins=c["x_ticks_nbins"])
            
            def eval_tick(x):
                if x >= 1:
                    if int(x) % x == 0:
                        return int(x)
                    elif int(x) % x != 0:
                        return str(x)
                else:
                    return str(x)
            
            xlabels = [eval_tick(n) for n in ax.get_xticks()]
        
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        ax.spines['left'].set_zorder(10)
        ax.spines['right'].set_zorder(10)
        ax.set_xticklabels(
            xlabels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
        ax.set_yticklabels(
            ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()
        ax.tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        ax.tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        ## Configure axes labels
        ax.set_xlabel(
            c["x_label"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            fontname=c["x_label_fn"],
            weight=c["x_label_weight"]
            )
        ## Configure YY ticks/label
        ax.set_ylabel(
            c["y_label"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"]
            )
        
        # writes unassigned in the center of the plot for unassigned peaks
        # and plots nothing
        if data_info[0,col['Peak Status']] == 'unassigned':
            ax.text(
                (x[0] + x[-1]) / 2,
                (c["y_lims"][0]+c["y_lims"][1])/2,
                'unassigned',
                fontsize=8,
                fontname='Arial',
                va='center', ha='center')
            
            return
        
        # do not represent the missing peaks.
        mes_mask = data_info[:,col['Peak Status']] != 'missing'
        data = data[mes_mask]
        x = x[mes_mask]
        # Plots data
        ax.plot(
            x,
            data,
            ls=c["line_style"],
            color=c["line_color"],
            marker=c["marker_style"],
            mfc=c["marker_color"],
            markersize=c["marker_size"],
            lw=c["line_width"],
            zorder=5
            )
        
        if c["fill_between"]:
            ax.fill_between(
                x,
                0,
                data,
                facecolor=c["fill_color"],
                alpha=c["fill_alpha"]
                )
        
        # fit_res_col = "{}_{}".format(calccol, res)
        
        # if self.kwargs["fit_performed"] \
                # and self.kwargs["series_axis"] == 'along_x'\
                # and self.kwargs["fit_okay"][fit_res_col]:
            # # plot fit
            # ax.plot(
                # self.xfit,
                # self.fit_plot_ydata[fit_res_col],
                # fit_line_style,
                # lw=fit_line_width,
                # color=fit_line_color, zorder=6
                # )
            # # write text
            # axs[i].text(
                # xmax*0.05,
                # y_lims[1]*0.97,
                # self.fit_plot_text[fit_res_col],
                # ha='left',
                # va='top',
                # fontsize=4
                # )
        
        # elif self.fit_performed and self.series_axis == 'along_x' \
                # and not(self.fit_okay[fit_res_col]):
            # axs[i].text(
                # xmax*0.05,
                # y_lims[1]*0.97,
                # self.fit_plot_text[fit_res_col],
                # ha='left',
                # va='top',
                # fontsize=4
                # )
        
        return
    
if __name__ == "__main__":
    
    import os
    
    config = {
        
        "cols_page": 5,
        "rows_page": 8,
        
        "y_lims":(0,0.3),
        "vspace":0.5,
        
        "subtitle_fn": "Arial",
        "subtitle_fs": 8,
        "subtitle_pad": 0.98,
        "subtitle_weight": "normal",
        
        "x_label_fn": "Arial",
        "x_label_fs": 6,
        "x_label_pad": 2,
        "x_label_weight": "normal",
        "x_label": "ligand ratio",
        
        "y_label_fn": "Arial",
        "y_label_fs": 6,
        "y_label_pad": 2,
        "y_label_weight": "normal",
        "y_label": "CSPs",
        
        "set_x_values": True,
        "titration_x_values": [0,25,50,100,200,400,500],
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 5,
        "x_ticks_pad": 1,
        "x_ticks_weight": "normal",
        "x_ticks_rot": 30,
        "x_ticks_len":2,
        "x_ticks_nbins": 5,
        
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 5,
        "y_ticks_pad": 1,
        "y_ticks_weight": "normal",
        "y_ticks_rot": 0,
        "y_ticks_len":2,
        "y_ticks_nbins":8,
        
        "line_style": "-",
        "line_width": 1,
        "line_color": "red",
        
        "marker_style": "o",
        "marker_color": "darkred",
        "marker_size": 3,
        
        "fill_between": True,
        "fill_color": "pink",
        "fill_alpha": 0.5,
        
        
        "perform_resevo_fitting": False,
        "fit_line_color": "black",
        "fit_line_width": 1,
        "fit_line_style": "-",
        
        "fig_height": 11.69,
        "fig_width": 8.69
    }
    
    file_name = os.path.realpath(__file__)
    
    ######################################################################## 1
    
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
    
    series_info = {
        "series_axis":"along_x",
        "dim_comparison":"along_x"
        }
    
    plot = ResEvoPlot(
        full_data_set[:,:,21].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        config,
        exp_names=["0","25","50","100","200","400","500"],
        **series_info
        )
    
    plot.plot()
    plot.save_figure('resevo_csp.pdf')
