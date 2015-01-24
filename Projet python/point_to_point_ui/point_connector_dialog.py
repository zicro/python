# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PointConnectorDialog
                                 A QGIS plugin
 Creating lines between points following a from-to list.
                             -------------------
        begin                : 2015-01-15
        copyright            : (C) 2015 by LPGA
        email                : LPGA20132015@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic, QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'point_connector_dialog_base.ui'))


class PointConnectorDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        #Constructor
        super(PointConnectorDialog, self).__init__(parent)
        self.settings = QtCore.QSettings("petahl", "PointConnector")
        self.setupUi(self)
        self.browsePointButton.clicked.connect(self.browsePointButton_clicked)            

        
    # Browse Point button
    def browsePointButton_clicked(self):
        lastShapeDir = self.settings.value("lastShapeDir", ".")
        pointFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File', lastShapeDir, 'ESRI Shape files (*.shp)')
        self.pointPathLineEdit.setText(pointFileName)
        (shpDir, shpFile) = os.path.split(pointFileName)
        self.settings.setValue("lastShapeDir", shpDir)


