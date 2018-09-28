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
#from abc import ABCMeta, abstractmethod

from math import ceil
from matplotlib import pyplot as plt

import core.fslibs.Logger as Logger


class PlottingBase:#(metaclass=ABCMeta):
    """
    Plotting base class with methods common to all plots.
    
    Not functional on its own.
    
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
        
        - additional kwargs can be passed as **kwargs.
    """
    
    info_cols={
        "ResNo":0,
        "1-letter":1,
        "3-letter":2,
        "Peak Status":3,
        "Merit":4,
        "Fit Method":5,
        "Vol. Method":6,
        "Details":7
        }
    
    def __init__(self, data, data_info, **kwargs):
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ExperimentPlot initiated")
        
        self.data = data
        self.data_info = data_info
        self.kwargs = kwargs
        
        self.logger.debug("Shape of data matrix: {}".format(self.data.shape))
        self.logger.debug("Shape of data info: {}".format(self.data_info.shape))
        self.logger.debug("Kwargs: {}".format(self.kwargs))
        
        self.figure = None
        self.axs = None
        self.len_axs = None
        
        super().__init__()
    
    #@abstractmethod
    def data_select(self):
        """
        Selects the desired data to plot from the original input data.
        
        This function can be used to fine select the data to the ploted
        or transpose matrix coordinates or any other request that
        faciliates the task of .plot_subplots() method.
        
        Returns:
            - None.
            
        Stores:
            - self.data_to_plot (numpy.array): selected data to plot
        """
        pass
    
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
    
    def draw_figure(self):
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
        self._calcs_numsubplots()
        
        numrows, real_fig_height = self._config_fig()
        
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        self.figure, self.axs = plt.subplots(
            nrows=numrows,
            ncols=self.config["cols_page"],
            figsize=(self.config["fig_width"], real_fig_height)
            )        
        self.axs = self.axs.ravel()
        self.len_axs = len(self.axs)
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995]
            )
        
        return
    
    # @abstractmethod
    # def plot_subplots(self):
        # """
        # Sends the specific data to each subplot.
        
        # The way data is sliced from the whole data to plot matrix
        # depends on the nature of the subplots.
        
        # Returns:
            # - None
        # """
        # pass
    
    # @abstractmethod
    # def subplot(self):
        # """The routine that defines each subplot."""
        # pass
    
    # def plot(self):
        # """Runs all operations to plot."""
        # self.data_select()
        # self.draw_figure()
        # self.plot_subplots()
        # self.clean_subplots()
        # return
    
    def clean_subplots(self):
        """ Removes unsed subplots."""
        self.logger.debug("Length Axes: {}".format(self.len_axs))
        for i in range(self.num_subplots, self.len_axs):
            self.axs[i].remove()
    
    def save_figure(self, path=''):
        """Saves figure to path"""
        
        path = path or "plot.pdf"
        self.figure.savefig(path)
        self.logger.info("Saved {}".format(path))
        
        return
    
    
if __name__ == "__main__":
    
    print(__name__)
