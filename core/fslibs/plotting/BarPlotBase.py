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
    Class with methods common to all Bar Plot templates.
    """
    
    def _plot_theo_pre(
            self,
            axs,
            values_x,
            values_y,
            tag_position,
            y_lim,
            bartype='h',
            pre_color='lightblue',
            pre_lw=1,
            tag_color='red',
            tag_ls='-',
            tag_lw=0.1
            ):
        """
        Plots theoretical PRE.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            values_x (np.ndarray): X values to plot
            
            values_y (np.adrray): Y values to plot
            
            tag_position (int): the residue number where the paramagnetic
                tag is placed.
            
            y_lim (float): plot's y axis limit
            
            bartype (str): {'h', 'v', 'hm'}, whether plot of type 
                horizontal, vertical or Heat Map. Defaults: 'h'.
            
            pre_color (str): the colour of plot line
            
            pre_lw (int): line width
            
            tag_color (str): the colour of the tag cartoon
            
            tag_ls (str): matplotlib linestyle kwarg for the tag tick
            
            tag_lw (float): tag tick line width.
        """
            
        # x_axis_values = np.arange(
            # float(self.loc[exp,:,'ResNo'].head(n=1))-1,
            # float(self.loc[exp,:,'ResNo'].tail(n=1)),
            # 1,
            # )
        
        if bartype == 'v':
            axs.plot(
                values_y,
                values_x,
                zorder=9,
                color=pre_color,
                lw=pre_lw
                )
        
        elif bartype == 'h':
            axs.plot(
                values_x,
                values_y,
                zorder=9,
                color=pre_color,
                lw=pre_lw
                )
        
        xtag = tag_position# - 1
        
        if bartype in ['h', 'DPRE_plot']:
            axs.vlines(
                xtag,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
            axs.plot(
                xtag,
                y_lim,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif bartype == 'v':
            axs.hlines(
                xtag,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
            axs.plot(
                y_lim,
                xtag,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif bartype == 'hm':
            axs.vlines(
                xtag,
                0,
                y_lim,
                colors=tag_color,
                linestyle=tag_ls,
                linewidth=tag_lw,
                zorder=10
                )
    
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
            axbar,
            series,
            d,
            yy_scale,
            fs=3,
            orientation='horizontal'):
        """
        Places a text mark over the bars of a Bar Plot.
        
        Parameters:
            ax (matplotlib subplot axis): where maker is written.
            
            axbar (matplotlib object): bars of plot.
            
            series (np.array): series with information source.
            
            d (dict): translates information into marker.
            
            yy_scale (float): vertical scale calibrates marker position
            
            fs (int): font size
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal barplot.
        """
        #elf.logger.debug("Bars series: {}".format(axbar))
        self.logger.debug("Text marker series: {}".format(series))
        m = len(series) == len(axbar)
        self.logger.debug("Length Bars and Series match: {}".format(m))
        
        
        def vpos_sign(x, y):
            """Scales to the vertical position - positive and negative."""
            if y>=0:
                return np.nan_to_num(x)
            elif y<0:
                return (x*-1)-(yy_scale/20)
            else:
                return 0
        
        def hpos_sign(x, y):
            """Scales to the horizontal position - positive and negative."""
            if y > 0:
                return x+(yy_scale/20)
            elif y<0:
                return (x*-1)-(yy_scale/20)
            else:
                return 0
        
        for v, bar in zip(series, axbar):
            if str(v) in d.keys():
                x0, y0 = bar.xy
                self.logger.debug("{},{}".format(x0, y0))
                if orientation == 'vertical':
                    self.logger.debug("bar_width: {}".format(bar.get_width()))
                    hpos = hpos_sign(bar.get_width(), x0)
                    vpos = bar.get_y() + bar.get_height()/2
                    vaa='center'
                
                elif orientation == 'horizontal':
                    self.logger.debug("bar_height: {}".format(bar.get_height()))
                    vpos = vpos_sign(bar.get_height(), y0)
                    hpos = bar.get_x() + bar.get_width() / 2.5
                    vaa='bottom'
                
                self.logger.debug("Drawing {},{},{}".format(type(hpos),type(vpos),type(d[str(v)])))
                self.logger.debug("Drawing {},{},{}".format(hpos,vpos,d[str(v)]))
                
                ax.text(
                    hpos,
                    vpos,
                    d[str(v)],
                    ha='center',
                    va=vaa,
                    fontsize=fs
                    )
            else:
                continue
        
        return
