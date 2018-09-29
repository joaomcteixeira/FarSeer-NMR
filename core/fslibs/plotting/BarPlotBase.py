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
from math import ceil

class BarPlotBase:
    """
    Base class with methods common to all Bar Plot templates.
    
    Not functional on its own.
    """
    
    def plot(self):
        """Runs all operations to plot."""
        self.draw_figure() # from PlottingBase
        self.plot_subplots()
        self.adjust_subplots()
        self.clean_subplots()
        return
    
    def plot_subplots(self):
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
                self.axs[i],
                self.data[i],
                self.data_info[i],
                self.experiment_names[i],
                data_extra=data_extra
                )
    
    def adjust_subplots(self):
        self.figure.subplots_adjust(
            hspace=self.config["hspace"],
            wspace=self.config["wspace"]
            )
    
    def _draw_paramagnetic_tag(
            self,
            ax,
            tag_position,
            y_lim,
            plottype='h',
            tag_color='red',
            tag_ls='-',
            tag_lw=0.1
            ):
        """
        Draws paramagnetic tag tick on functionalized residue.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            tag_position (int): the residue number where the paramagnetic
                tag is placed.
            
            y_lim (float): plot's y axis limit
            
            plottype (str): {'h', 'v', 'hm'}, whether plot of type 
                horizontal, vertical or Heat Map. Defaults: 'h'.
            
            tag_color (str): the colour of the tag cartoon
            
            tag_ls (str): matplotlib linestyle kwarg for the tag tick
            
            tag_lw (float): tag tick line width.
        """
        
        y_lim = y_lim*0.1
        
        if plottype in ['h', 'DPRE_plot']:
            ax.vlines(
                tag_position,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
            ax.plot(
                tag_position,
                y_lim,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif plottype == 'v':
            ax.hlines(
                tag_position,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
            ax.plot(
                y_lim,
                tag_position,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif plottype == 'hm':
            ax.vlines(
                tag_position,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
        return
    
    def _plot_theo_pre(
            self,
            ax,
            values_x,
            values_y,
            plottype='h',
            pre_color='lightblue',
            pre_lw=1
            ):
        """
        Plots theoretical PRE.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            values_x (np.ndarray): X values to plot
            
            values_y (np.adrray): Y values to plot
            
            plottype (str): {'h', 'v'}, whether plot of type 
                horizontal, vertical or Heat Map. Defaults: 'h'.
            
            pre_color (str): the colour of plot line
            
            pre_lw (int): line width
            
        """
        
        if plottype == 'v':
            ax.plot(
                values_y,
                values_x,
                zorder=9,
                color=pre_color,
                lw=pre_lw
                )
        
        elif plottype == 'h':
            ax.plot(
                values_x,
                values_y,
                zorder=9,
                color=pre_color,
                lw=pre_lw
                )
        
        return
    
    def _plot_threshold(
            self,
            ax,
            values,
            color,
            lw,
            alpha,
            std=5,
            orientation='horizontal',
            zorder=5):
        """
        Plots threshold line that identifies relevant perturnations.
        
        Parameters:
            ax (matplotlib subplot axis): subplot where line is drawn.
            
            values (np.array of shape [x]): values to evaluate.
            
            color (str): line color.
            
            lw (int): line width.
            
            alpha (float): transparency.
            
            std (int): standard deviation multiplier
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal barplot.
            
            zorder (int): the matplotlib zorder kwarg.
        """
        sorted_values = np.copy(np.sort(np.absolute(values)))
        parsed_values = sorted_values[np.logical_not(np.isnan(sorted_values))]
        firstdecile = parsed_values[0:ceil(0.1*len(parsed_values))]
        threshold = np.mean(firstdecile) + std*np.std(firstdecile)
        
        self.logger.debug("Threshold defined: {}".format(threshold))
        
        if orientation == 'horizontal':
            ax.axhline(
                y=threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axhline(
                y=-threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
        
        elif orientation == 'vertical':
            ax.axvline(
                x=threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axvline(
                x=-threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
        
        return
    
    def _set_item_colors(self, items, values, d):
        """
        Colour codes conditions.
        
        Parameters:
            items (items obj): either plot bars, ticks, etc...
        
            values (np.array shape [x]):
                containing the 'Peak Status' information.
        
            d (dict): keys are conditions, and values are colours.
        
        Returns:
            None, series are changed in place.
        """
        
        for v, it in zip(values, items):
            if str(v) in d.keys():
                self.logger.debug("Setting color: {}".format(d[str(v)]))
                it.set_color(d[str(v)])
            
            else:
                continue
        return
    
    def _text_marker(
            self,
            ax,
            values_x,
            values_y,
            series,
            d,
            fs=3,
            orientation='horizontal'):
        """
        Places a text mark over the bars of a Bar Plot.
        
        Parameters:
            ax (matplotlib subplot axis): where maker is written.
            
            values_x (np.array): series with X axis information
            
            values_y (np.array): series with Y axis information
            
            series (np.array): series with information source.
            
            d (dict): translates information into marker.
            
            fs (int): font size
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal barplot.
        """
        self.logger.debug("Text marker series: {}".format(series))
        
        if orientation == 'vertical':
            
            for s, x, y in zip(series, values_x, values_y):
                if str(s) in d.keys():
                    
                    if np.nan_to_num(y) > 0:
                        ha='left'
                        
                    elif np.nan_to_num(y) < 0:
                        ha='right'
                    
                    else:
                        ha='center'
                    
                    ax.text(
                        np.nan_to_num(y),
                        np.nan_to_num(x),
                        d[str(s)],
                        ha=ha,
                        va='center',
                        fontsize=fs
                        )
        
        elif orientation == 'horizontal':
            
            for s, x, y in zip(series, values_x, values_y):
                if str(s) in d.keys():
                    
                    if np.nan_to_num(y) > 0:
                        va='bottom'
                        
                    elif np.nan_to_num(y) < 0:
                        va='top'
                    
                    else:
                        va='bottom'
                    
                    ax.text(
                        np.nan_to_num(x),
                        np.nan_to_num(y),
                        d[str(s)],
                        ha='center',
                        va=va,
                        fontsize=fs
                        )
        
        return
