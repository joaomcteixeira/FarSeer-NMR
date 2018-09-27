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
        - data (pd.Panel or np.array): multidimensional array containain
            the dataset to be plot. This dataset can be further selected
            by the self.data_select() method.
        
        - config (dict): a dictionary containing all the configuration
            parameters required for this plotting routine.
    """
    def __init__(self, data, config, args*):
        
        self.original_data = data
    
    @abstractmethod
    def data_select(self, *args):
        """
        Selects the desired data to plot from the original input data.
        
        Returns:
            - None. Creates a self.data_to_plot attribute of numpy.array
                type.
        """
        pass
    
    @abstractmethod
    def draw_figure(self, *args):
        """
        Draws the figure architecture.
        
        Defines the size of the figure and subplots based
        on the data to plot.
        
        Returns:
            - None.
        
        Stores :
            - self.figure: Figure object.
            - self.axs: axes of the figure (in case matplotlib is used).
            - self.num_subplots (int): the number of subplots to be used
            - self.len_axs (int): the number of subplots created in the
                figure object.
        """
        pass
    
    @abstractmethod
    def plot_subplots(self, args*):
        """
        Sends the specific data to each subplot.
        
        The way data is sliced from the whole data to plot matrix
        depends on the nature of the subplots.
        
        Returns:
            - None
        """
    
    @abstractmethod
    def subplot(self):
        """The routine that defines each subplot."""
    
    def clean_subplots(self):
        """ Removes unsed subplots."""
        
        for i in range(self.num_subplots, self.len_axs):
            self.axs[i].remove()
    
    
