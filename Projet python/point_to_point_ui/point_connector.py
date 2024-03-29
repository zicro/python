# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PointConnector
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from point_connector_dialog import PointConnectorDialog
import os.path
import processing
from qgis.utils import *
import time
import codecs
import re



class PointConnector:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PointConnector_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PointConnectorDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Point Connector')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PointConnector')
        self.toolbar.setObjectName(u'PointConnector')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PointConnector', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/PointConnector/icon.png"), "PointConnector", self.iface.mainWindow())
        self.action.setWhatsThis("Connect points")
        self.action.setStatusTip("Connect points following a from-to list")

        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        if hasattr(self.iface, "addPluginToVectorMenu"):
            self.iface.addVectorToolBarIcon(self.action)
            self.iface.addPluginToVectorMenu("&PointConnector", self.action)
        else:
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&PointConnector", self.action)

    def unload(self):
        self.iface.removePluginVectorMenu("&PointConnector",self.action)
        self.iface.removeVectorToolBarIcon(self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
         # afficher le formulaire
        self.dlg.show()
        # et mettre son execution dans une boucle
        result = self.dlg.exec_()
        # si l'utilisateur appui sur ok
        if result == 1:
            pointPath = self.dlg.pointPathLineEdit.text()
            point_layer = QgsVectorLayer(pointPath, 'points', 'ogr') #créer instance du shapefile en le gardant ogr =  c a dire origine (file)
            point_layer_crs = point_layer.crs().authid() # récuper le code de sa projection
            lines_layer = QgsVectorLayer('LineString?crs='+point_layer_crs, 'lines', 'memory') # créer une shapefile de type ligne en utilisant projection du précendant et en le stockant dans la mémoir
            point_name_index = 0 # l'index du champ id est par defaut a 0
            pr = lines_layer.dataProvider() # récuper réference du shapefile crée

            #verifier si on réussi a ouvrir le shapefile
            try:
                p = open(pointPath, 'r')
                p.close()
            except IOError:
                QMessageBox.information(None, "Erreur", "Fichier de form introuvable , vérifier votre shapefile.")
                return

            #début de l'edition du shapefile line qui aura un seule champ c'est id
            lines_layer.startEditing()
            pr.addAttributes ([ QgsField('id', QVariant.Int)] )

            #creating point coordinate dict
            points = processing.features(point_layer)
            points_dict = {}
            i = 0
            for p in points:
                geom = p.geometry()  # récuper la geométrie du point
                attrs = p.attributes() # récuper ces attributs
                p = geom.asPoint()  # la considérant autant que piont
                time.sleep(0.01) #Had a problem in an early version that the script crashed during this loop. Adding this solved it. I don't dare deleting it now...
                points_dict[str(i)] = p
                i+=1
            QgsMapLayerRegistry().instance().addMapLayer(point_layer)


            #Progress bar widget
            progressMessageBar = iface.messageBar().createMessage("edition des lignes...")
            progress = QProgressBar()
            progress.setMaximum(len(points_dict))
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)

            i=1
            j=0
            for p in points_dict:
                
                if(i<len(points_dict)):
                    frPoint = points_dict[str(j)]
                    toPoint = points_dict[str(i)]
                    attrs = [j]
                    new_line = QgsGeometry.fromPolyline([QgsPoint(frPoint), QgsPoint(toPoint)])
                    feat = QgsFeature()
                    feat.setGeometry(new_line)
                    feat.setAttributes(attrs)
                    (res, outFeats) = pr.addFeatures([feat])
                    lines_layer.commitChanges()
                    progress.setValue(i)
                i+=1
                j+=1
                progress.setValue(i)

            iface.messageBar().clearWidgets()

                
                

                
       

            QgsMapLayerRegistry().instance().addMapLayer(lines_layer)
            QMessageBox.information(None, 'Success', 'All lines drawn without error')    



