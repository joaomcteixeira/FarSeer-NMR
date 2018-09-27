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
from abc import ABCMeta, abstractmethod

class PlottingBase(metaclass=ABCMeta):
    """
    Plotting base class.
    
    To implement a new plotting routine create a class that inherits
    PlottingBase and define its specific functions (@abstractmethod).
    
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
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): additional
            info.
        
        - config (dict): a dictionary containing all the configuration
            parameters required for this plotting routine.
            Mandatory keys:
                - fig_height (float, inches)
                - fig_width (float, inches)
                - cols_per_page (int): columns of subplots per figure page
                - rows_per_page (int): rows of subplots per figure page
        
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
    
    def __init__(self, data, data_info, data_extra, config, **kwargs):
        
        self.data = data
        self.data_info = data_info
        self.data_extra = data_extra
        self.config = config
        self.kwargs = kwargs
        
        self.data_to_plot = None
        self.figure = None
        self.axs = None
        self.num_subplots = None
        self.len_axs = None
    
    @abstractmethod
    def data_select(self, **kwargs):
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
    
    @abstractmethod
    def _calcs_numsubplots(self):
        """
        Calculates the total number of subplots to be plotted
        based on the user data.
        
        Returns:
            - None
            
        Stores:
            - self.num_subplots (int)
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
        
        numrows = ceil(self.num_subplots/self.config["cols_per_page"]) + 1 
        
        real_fig_height = \
            (self.config["fig_height"] / self.config["rows_per_page"]) \
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
            ncols=self.config["cols_per_page"],
            figsize=(self.config["fig_width"], real_fig_height)
            )
        self.len_axs = len(self.axs)
        self.axs = self.axs.ravel()
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995],
            h_pad=real_fig_height/self.config["rows_per_page"]
            )
        
        return
    
    @abstractmethod
    def plot_subplots(self, **kwargs):
        """
        Sends the specific data to each subplot.
        
        The way data is sliced from the whole data to plot matrix
        depends on the nature of the subplots.
        
        Returns:
            - None
        """
    
    @abstractmethod
    def subplot(self, **kwargs):
        """The routine that defines each subplot."""
    
    def clean_subplots(self):
        """ Removes unsed subplots."""
        
        for i in range(self.num_subplots, self.len_axs):
            self.axs[i].remove()
    
    
