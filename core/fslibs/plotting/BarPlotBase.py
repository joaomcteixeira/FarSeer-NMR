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
from matplotlib import pyplot as plt

from core.fslibs.plotting.ExperimentPlot import ExperimentPlot
from core.fslibs.WetHandler import WetHandler
import core.fslibs.Logger as Logger


class BarPlotBase(ExperimentPlot):
    """
    Base class with methods common to all Bar Plot templates.
    
    Each value in <values> is represented by a bar and each bar is labeled
    according to <labels>.
    
    Not functional on its own.
    
    PARAMETERS:
    
        - values (np.array shape (y,x), dtype=float): where X (axis=1)
            is the data to plot for each column and Y (axis=0) is the evolution
            of that data along the titration series.
            
        - labels (np.array shape (x,), dtype=str): Bar labels presented
            sequentially and synchronized with <values>.
            <labels> axis 0 equals <values> axis 1.
        
    """
    _default_config = {}
    
    def __init__(
            self,
            values,
            labels,
            config={},
            **kwargs
            ):
        
        # initializes logger
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarPlotBase initialized")
        
        
        self._config = BarPlotBase._default_config.copy()
        self._config.update(config)
        self.logger.debug("Configured configure: {}".format(self._config))
        
        # check input
        self.values = self._check_values(values)
        self.labels = self._check_labels(labels)
        
        super().__init__(config=self._config.copy(), **kwargs)
        

    def _check_values(self, values):
        """
        Checks if values:
            - is np.array
            - has shape (y,x)
            - can be converted to float
        """
        if self._check_instance(np.ndarray, values):
            
            if len(values.shape) == 2:
            
                try:
                    values.astype(float)
                except ValueError as e:
                    msg = "A value in <values> can't be converted to type float"
                    wet = WetHandler(msg=msg, msg_title="ERROR", wet_num=0)
                    self.logger.info(wet.wet)
                    wet.abort()
                except Exception:
                    msg = "Something is wrong in the input <values>, can't convert to float"
                    wet = WetHandler(msg=msg, wet_num=0, msg_title="ERROR")
                    self.logger.info(wet.wet)
                    wet.abort()
                
                return values
            
            else:
                msg = "Input <values> should be of shape (y,x)"
                wet = WetHandler(msg=msg, wet_num=0, msg_title="ERROR")
                self.logger.info(wet.wet)
                wet.abort()
        else:
            msg = "Input <values> are not of type numpy.ndarray"
            wet = WetHandler(msg=msg, wet_num=0, msg_title="ERROR")
            self.logger.info(wet.wet)
            wet.abort()
        
    def _check_labels(self, labels):
        """
        Checks if labels:
            - is np.array
            - has shape (x,)
            - shape length equals self.values axis=1 length.
        """
        if self._check_instance(np.ndarray, labels):
            if len(labels.shape) == 1:
                if self._check_equality(labels.shape[0], self.values.shape[1]):
                    return labels
                
            else:
                msg = "Input <labels> should be of shape (x,)"
                wet = WetHandler(msg=msg, wet_num=0, msg_title="ERROR")
                self.logger.info(wet.wet)
                wet.abort()
        else:
            msg = "Input <labels> are not of type numpy.ndarray"
            wet = WetHandler(msg=msg, wet_num=0, msg_title="ERROR")
            self.logger.info(wet.wet)
            wet.abort()
    
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
    
    def plot(self):
        """Runs all operations to plot."""
        self.draw_figure() # from PlottingBase
        self.plot_subplots() # from self
        self.adjust_subplots() # from PlottingBase
        self.clean_subplots() # from PlottingBase
        self.save_figure() # from PlottingBase
        plt.close(self.figure)
        return
    
    def plot_subplots(self):
        """
        Sends the specific data to each subplot.
        Requires self.figure and self.axs
        
        Returns:
            - None
        """
        self.logger.debug("Starting plot activity")
        
        if not(self.figure) and not(self.axs):
            self.logger.info("figure and axs are not yet created. None is returned")
            return None
        
        for i in range(self.values.shape[0]):
            
            self.logger.debug("Starting subplot no: {}".format(i))
            
            self.subplot(
                self.axs[i],
                self.values[i],
                self.subtitles[i],
                i
                )
        
        # returns the final index
        # useful for some subplots
        return i
    
