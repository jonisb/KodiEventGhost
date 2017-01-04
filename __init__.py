# -*- coding: utf-8 -*-
"""
Kodi support plugin for EventGhost
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import eg

import KodiLib

import logging  # TODO: Move after eg.RegisterPlugin()?

logger = logging.getLogger(__name__)  # TODO: Move after eg.RegisterPlugin()?

logger.critical('Register plugin with EventGhost.')
eg.RegisterPlugin(
    name="Kodi",
    author="Joni Borén",
    version="0.7.0",
    kind="program",
    guid="{8C8B850C-773F-4583-AAD9-A568262B7934}",  # TODO: change guid.
    canMultiLoad=True,
    createMacrosOnAdd=False,
    url="http://www.eventghost.net/forum/viewtopic.php?f=10&t=1562",  # TODO: usenew url?.
    description="""Adds actions/buttons to control <a href='http://www.kodi.org/'>Kodi</a>.

Test description.""",  # TODO: Add description, use <rst>?
    icon=(  # TODO: check/change icon.
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsRAAALEQF/ZF+RAAAA"
            "BGdBTUEAALGeYUxB9wAAACBjSFJNAAB6fAAAfosAAPoBAACHPAAAbUoAAPFDAAA2IAAAHlNX4WK7"
            "AAACYElEQVR42tTTPW8ScQDH8d/9n44HESgFKQjFWku1rUYdTEAT0sGHSU10cHZz0piYjqYxbia6"
            "+hB3Y0w3kzq0scaojdZqYiMp1dQWAlLg4A7ugbvzRXTy8wK+21dyXRe7QbBLuw6wG3ceJnJnLuTL"
            "279DrutySBIhEnUopSbjtMsYVzkXLSFEU5Y9dY/XW5Nlr207DpRWE+zzp6VHxWLpstpWKaEA5RT9"
            "XgCcC/jDDihjOpWI6vF4WkLweigULgdD4R/p4ZH30X1Dr6XhbK4i/OH43qSKVikJLhhGz26AEo61"
            "+Qz0roWR8RDWixtIJKP4/mUVA5EgkvvjOHEy/1FKj+XnwpHMxdipIhJH29C2o0hMVmH1KJQyxWTw"
            "FuKhKYCbaDUVOI4LwzKxOD8PAvkrMazOW1uSUH43ilCqgUYphvJyBitzKUyfLiCVBe7PPkVzp4l7"
            "dx9g+lwB5T9bePPqJTIjB4v0uqmVi4cHbx67UkFteRjRAx30mgEcym9iZz2NpRcyfAM6Om0Nruui"
            "sr2F8SNZuIQjEhl6Lj0LAY8Hcwtq6nwhStuQJB8sWOh3fTClBgIDOhj1wDAtcEFRq/5FW+shPRRF"
            "diyTYJNe4Kr1bfaJHiv0qAtBKTgX4D6CAJXAbQIhaYhyG16iIxvpwEfW0BITM75YrsJm3Ah6SnfB"
            "kCtzWmLikmabYLYAIRxO34Zp6nAs9VdX6xSVRn2lb7QWe2b3w9RxplwLy2AL8AOMIa5s3vb6gzUm"
            "+5mh1XXL0Lq2pVRVQ2z66J6fpLdaMqu6KjwUXo8XnFH0+w6k/3+mfwMAzwT87LI0qNEAAAAASUVO"
            "RK5CYII="
    ),
)
logger.critical('Finished registering plugin with EventGhost.')

logger.info('Importing "OrderedDict" module.')
try:
    from collections import OrderedDict
except ImportError:
    logger.warning('Failed to import "OrderedDict" module, trying local module.')
    try:
        from .ordereddict import OrderedDict
    except ImportError:
        logger.exception('Failed to import local "OrderedDict" module, aborting.')
        raise
logger.info('Importing "OrderedDict" module, done.')


def DefaultSettings(Data=None):
    """ """  # TODO
    if isinstance(Data, KodiLib.SettingsClass):
        Settings = Data
        Data = None
        Settings.addDefault(KodiLib.DefaultSettings())
    else:
        Settings = KodiLib.DefaultSettings()

    Settings.addDefault([
        ('client', [
            ('name', 'EventGhost')
        ]),
    ])
    if Data != None:
        Settings.addData(Data)
    return Settings


class Kodi(eg.PluginClass):
    """ """  # TODO
    def __init__(self):  # TODO:
        """ """  # TODO
        pass

    #def __start__(self, pluginConfig, *args):  # TODO:
    def __start__(self, pluginSettings):  # TODO:
        """ """  # TODO
        print(pluginSettings['client']['name'])
        pass

    def __stop__(self):  # TODO:
        """ """  # TODO
        pass

    def __close__(self):  # TODO:
        """ """  # TODO
        pass

    #def Configure(self, pluginConfig=None, *args):
    def Configure(self, pluginSettings=None):
        """ """  # TODO
        pluginSettings = DefaultSettings(pluginSettings)

        class test(object):
            def __init__(self, Item):
                """ """  # TODO
                self.Item = Item

            def GetItem(self):
                return self.Item

        class LazyTree(wx.TreeCtrl):
            ''' LazyTree is a simple "Lazy Evaluation" tree, that is, it only adds
                items to the tree view when they are needed.'''

            def __init__(self, *args, **kwargs):
                super(LazyTree, self).__init__(*args, **kwargs)
                self.__collapsing = False
                root = self.AddRoot('Settings', data=wx.TreeItemData(args[0].Settings))
                self.SetItemHasChildren(root)
                self.OnExpandItem(test(root))

                self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
                self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)
                self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._addNodeToSchema)

            def _addNodeToSchema(self, event):
                def ChangeValue(Item):
                    """ """  # TODO
                    setting = self.GetItemText(Item).split(' = ')[0]
                    myDlg = wx.TextEntryDialog(self, setting, "Change value", self.GetPyData(Item))
                    res = myDlg.ShowModal()
                    if res == wx.ID_OK:
                        value = myDlg.GetValue()
                        Dict = self.GetPyData(self.GetItemParent(Item))
                        Dict[setting] = value
                        self.SetItemText(Item, "{0} = {1}".format(setting, value))
                        self.SetItemData(Item, wx.TreeItemData(value))
                    myDlg.Destroy()

                if not isinstance(self.GetPyData(event.GetItem()), dict):
                    ChangeValue(event.GetItem())
                else:
                    event.Skip()

            def OnExpandItem(self, event):
                # Add a random number of children and randomly decide which
                # children have children of their own.
                ItemData = self.GetPyData(event.GetItem())
                try:
                    for setting in ItemData.Default.iterkeys():
                        if isinstance(ItemData[setting], dict):
                            child = self.AppendItem(event.GetItem(), setting, data=wx.TreeItemData(ItemData[setting]))
                            self.SetItemHasChildren(child, len(ItemData[setting].Default))
                        else:
                            self.AppendItem(event.GetItem(), "{0} = {1}".format(setting, ItemData[setting]), data=wx.TreeItemData(ItemData[setting]))
                except AttributeError:
                    #child = self.AppendItem(event.GetItem(), unicode(ItemData), data=wx.TreeItemData(ItemData))
                    eg.PrintError("Should not happen.")

            def OnCollapseItem(self, event):
                # Be prepared, self.CollapseAndReset below may cause
                # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
                if self.__collapsing:
                    event.Veto()
                else:
                    self.__collapsing = True
                    item = event.GetItem()
                    self.CollapseAndReset(item)
                    self.SetItemHasChildren(item)
                    self.__collapsing = False

        def initPanel(self):
            setPanelProperties(self)
            doPanelLayout(self)

        def setPanelProperties(self):
            pass
#
        def doPanelLayout(self):
            #self.sizer.Add(self.button, 1, wx.ALIGN_CENTER, 0)
            pass

        def initPage(self):
            panel.dialog.notebook.AddPage(self, "Advanced")
            self.Settings = pluginSettings
            self.tree = LazyTree(self, style=wx.TR_HIDE_ROOT+wx.TR_LINES_AT_ROOT+wx.TR_HAS_BUTTONS+wx.TR_EDIT_LABELS)

            setPageProperties(self)
            doPageLayout(self)

        def setPageProperties(self):
            pass

        def doPageLayout(self):
            advanced_sizer = wx.BoxSizer(wx.VERTICAL)
            advanced_sizer.Add(self.tree, 1, wx.EXPAND, 0)
            self.SetSizer(advanced_sizer)

        panel = eg.ConfigPanel()
        initPanel(panel)
        panel.AdvancedPanel = wx.Panel(panel.dialog.notebook)
        initPage(panel.AdvancedPanel)

        while panel.Affirmed():
            #panel.SetResult(Settings)
            panel.SetResult(pluginSettings)
