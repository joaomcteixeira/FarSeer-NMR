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
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from core.parsing import read_peaklist

from core.fslibs.Variables import Variables

class SideBar(QTreeWidget):

    variables = Variables()._vars

    def __init__(self, parent=None, gui_settings=None):
        QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.setMaximumWidth(320)
        self.setFixedHeight(gui_settings['sideBar_height'])
        self.peakLists = self.variables['peaklists']

        self.setSortingEnabled(True)
        self.update_from_config()
        # self.peakLists = self.variables['peakLists']


    def update_from_config(self):
        self.clear()
        used_peaklists = []
        print(self.variables.keys())
        self.peakLists = self.variables["peaklists"]

        if not all(
                x for v in self.variables["conditions"].values() for x in v):
            self.refresh_sidebar()

        else:
            for z in self.variables["conditions"]["z"]:
                for y in self.variables["conditions"]["y"]:
                    for x in self.variables["conditions"]["x"]:
                        used_peaklists.append(
                            self.variables["experimental_dataset"][z][y][x])

            unused_peaklists = [x for x, pl in self.variables[
                "peaklists"].items() if x not in used_peaklists]
            for peaklist in unused_peaklists:
                self.addItem(peaklist)


    def dragEnterEvent(self, event):
        event.accept()
        if not event.mimeData().hasUrls():

            item = self.itemAt(event.pos())
            if not item:
                pass
            text = item.text(0)
            event.mimeData().setText(text)

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
            filePaths = [url.path() for url in event.mimeData().urls()]
            for filePath in filePaths:
               self.load_from_path(filePath)



    def load_from_path(self, filePath):
        name = None
        if os.path.isdir(filePath):
            for root, dirs, filenames in os.walk(filePath):
                for filename in filenames:
                    try:
                        path = os.path.join(root, filename)
                        name, path = self.load_peaklist(path)
                    except IOError:
                        pass
        else:
            name, path = self.load_peaklist(filePath)
        if name:
            return name, path



    def refresh_sidebar(self):
        self.clear()
        for peaklist in self.peakLists.keys():
            self.addItem(peaklist)

    def load_peaklist(self, filePath):

        if os.path.isdir(filePath):
            return

        name = filePath.split('/')[-1].split('.')[0]

        if not name in self.peakLists.keys():
            peaklist = read_peaklist(filePath)
            if peaklist:
                pl_name = name


                item = self.addItem(pl_name)
                self.peakLists[item.text(0)] = peaklist
                self.peakLists[pl_name] = filePath

                return pl_name, filePath
            else:
                print("Invalid peak list file: %s" % filePath)
                return None, None
        else:
            print('Peaklist with name %s already exists.' % name)
            return None, None

    def addItem(self, name):
        newItem = QTreeWidgetItem(self)
        newItem.setFlags(newItem.flags() & ~(QtCore.Qt.ItemIsDropEnabled))
        newItem.setText(0, name)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        return newItem

    def removeItem(self, item_name):
        import sip
        result = self.findItems(item_name, QtCore.Qt.MatchRecursive, 0)
        if result:
            sip.delete(result[0])
