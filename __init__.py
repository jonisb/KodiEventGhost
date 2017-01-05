# -*- coding: utf-8 -*-
"""
Kodi support plugin for EventGhost
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import eg

import KodiLib
import SSDPLib  # ToDo: Move after eg.RegisterPlugin()?

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

import types
import threading


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

        myEVT_SSDPResult = wx.NewEventType()
        EVT_SSDPResult = wx.PyEventBinder(myEVT_SSDPResult, 1)

        class SSDPResultEvent(wx.PyCommandEvent):
            """Event to signal that a count value is ready"""
            def __init__(self, etype, eid, value=None):
                """Creates the event object"""
                wx.PyCommandEvent.__init__(self, etype, eid)
                self._value = value

            def GetValue(self):
                """Returns the value from the event.
                @return: the value of this event

                """
                return self._value

        class SSDPScanThread(threading.Thread):
            def __init__(self, parent, clients):
                threading.Thread.__init__(self)
                self._parent = parent
                self.clients = clients

            def run(self):
                logger.info('Thread runs')
                for client in SSDPLib.ssdpSearchGen(self.clients):
                    logger.info('Create event')
                    evt = SSDPResultEvent(myEVT_SSDPResult, -1, client)
                    logger.info('Post event')
                    wx.PostEvent(self._parent, evt)
                logger.info('Thread ends')

        class SSDPSearchDialog(wx.Dialog):
            def __init__(self, parent, title):
                super(SSDPSearchDialog, self).__init__(parent, title=title, size=(500, 150))
                self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SUNKEN_BORDER)
                self.list_ctrl_1.InsertColumn(0, 'FriendlyName')
                self.list_ctrl_1.InsertColumn(1, 'Name')
                self.list_ctrl_1.InsertColumn(2, 'version')
                self.list_ctrl_1.InsertColumn(3, 'ip')
                self.list_ctrl_1.InsertColumn(4, 'port')
                self.list_ctrl_1.InsertColumn(5, 'id')
                self.index = 0
                self.ListCtrlData = {}

                self.okBtn = wx.Button(self, wx.ID_OK)
                self.okBtn.Disable()
                self.cancelBtn = wx.Button(self, wx.ID_CANCEL)
                self.rescanBtn = wx.Button(self, wx.ID_REFRESH)

                worker = SSDPScanThread(self, ('Kodi', 'XBMC Media Center'))
                logger.info('worker starts.')
                worker.start()
                # Attributes
#                worker = CountingThread(self, 1)
#                logger.info('worker starts.')
#                worker.start()
                #self.CreateStatusBar()

                # Layout
                self.__DoLayout()

                # Event Handlers
                self.Bind(EVT_SSDPResult, self.AddToListEvent)
                self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.ActivateListEvent)
                self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ITEM_SELECTED)
                self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.ITEM_DESELECTED)
                self.rescanBtn.Bind(wx.EVT_BUTTON, self.OnButton)

            def __DoLayout(self):
                Button1sizer = wx.BoxSizer(wx.HORIZONTAL)
                Button1sizer.Add(self.rescanBtn, 0)
                Button2sizer = wx.BoxSizer(wx.HORIZONTAL)
                Button2sizer.Add(self.okBtn, 0)
                Button2sizer.Add(self.cancelBtn, 0)

                Buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
                Buttonsizer.Add(Button1sizer, 1, wx.EXPAND)
                Buttonsizer.Add(Button2sizer, 0)

                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(self.list_ctrl_1, 1, wx.EXPAND)
                sizer.Add(Buttonsizer, 0, wx.EXPAND)
                self.SetSizer(sizer)

            def OnButton(self, evt):
                eg.PrintError("ReScan not implemented")

            def ActivateListEvent(self, evt):
                self.EndModal(wx.ID_OK)

            def ITEM_SELECTED(self, evt):
                self.okBtn.Enable()

            def ITEM_DESELECTED(self, evt):
                self.okBtn.Disable()

            def AddToListEvent(self, evt):
                self.list_ctrl_1.InsertStringItem(self.index, evt.GetValue()['friendlyName'])
                for i, label in enumerate(('name', 'version', 'ip', 'port', 'id'), 1):
                    self.list_ctrl_1.SetStringItem(self.index, i, evt.GetValue()[label])
                self.ListCtrlData[self.index] = evt.GetValue()
                self.list_ctrl_1.SetItemData(self.index, self.index)
                self.index += 1

        def OnButton(self, evt):
            logger.info('OnButton starts.')
            SSDPSearch = SSDPSearchDialog(self, "Searching for clients")
            res = SSDPSearch.ShowModal()
            if res == wx.ID_OK:
                value = SSDPSearch.list_ctrl_1.GetFirstSelected()
                server = self.Settings['server']
                network = server['network']
                ListCtrlData = SSDPSearch.ListCtrlData[value]
                network['address'] = ListCtrlData['ip']
                network['http']['port'] = ListCtrlData['port']
                server['friendlyName'] = ListCtrlData['friendlyName']
                server['name'] = ListCtrlData['name']
                server['version'] = ListCtrlData['version']
                network['upnp']['id'] = ListCtrlData['id']
            SSDPSearch.Destroy()
            logger.info('OnButton ends.')

        def initPanel(self):
            self.button = wx.Button(self, wx.ID_ANY, "Scan")

            setPanelProperties(self)
            doPanelLayout(self)

            # Events
            self.button.Bind(wx.EVT_BUTTON, self.OnButton)

        def setPanelProperties(self):
            pass

        def doPanelLayout(self):
            self.sizer.Add(self.button, 0, wx.ALIGN_CENTER, 0)

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

        def initPage(self):
            panel.dialog.notebook.AddPage(self, "Advanced")
            self.Settings = pluginSettings
            self.tree = LazyTree(self, style=wx.TR_HIDE_ROOT+wx.TR_LINES_AT_ROOT+wx.TR_HAS_BUTTONS)  # +wx.TR_EDIT_LABELS

            setPageProperties(self)
            doPageLayout(self)

        def setPageProperties(self):
            pass

        def doPageLayout(self):
            advanced_sizer = wx.BoxSizer(wx.VERTICAL)
            advanced_sizer.Add(self.tree, 1, wx.EXPAND, 0)
            self.SetSizer(advanced_sizer)

        panel = eg.ConfigPanel()
        panel.OnButton = types.MethodType(OnButton, panel)
        panel.Settings = pluginSettings
        initPanel(panel)

        panel.AdvancedPanel = wx.Panel(panel.dialog.notebook)
        initPage(panel.AdvancedPanel)

        while panel.Affirmed():
            #panel.SetResult(Settings)
            panel.SetResult(pluginSettings)
