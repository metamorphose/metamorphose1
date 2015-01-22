# -*- coding: utf-8 -*-

# This is the item picker panel in the main
# application's notebook.

"""
Copyright (C) 2005-2008 Ianaré Sévi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

ianare@gmail.com
"""

import wx
import os
import re
import sys
import platform
import sre_constants

[wxID_PICKERPANEL, wxID_PICKERPANELBROWSE, wxID_SELECTIONAREADIRPICKER,
 wxID_PICKERPANELDIVIDER1, wxID_PICKERPANELFILESON,
 wxID_PICKERPANELFILETYPE, wxID_PICKERPANELFOLDERSON, wxID_PICKERPANELNOT_TYPE,
 wxID_PICKERPANELOK, wxID_PICKERPANELPATH, wxID_PICKERPANELPATH_HELP,
 wxID_SELECTIONAREAFPICKER, wxID_PICKERPANELSELECT, wxID_PICKERPANELSELECT_ALL,
 wxID_PICKERPANELSELECT_NONE, wxID_PICKERPANELSTATICTEXT1,
 wxID_PICKERPANELWALKIT, wxID_PICKERPANELFILTERBYRE, wxID_SELECTIONAREA,
wxID_PICKERPANELIGNORECASE, wxID_PICKERPANELUSELOCALE
] = [wx.NewId() for _init_ctrls in range(21)]

# the custom dirCrtl class:
class DirControl(wx.GenericDirCtrl):
    def __init__(self, parent, ID, name):
        self.parent = parent.GetParent()
        wx.GenericDirCtrl.__init__(self, parent, ID, name,
          defaultFilter=0, filter='', style=wx.DIRCTRL_DIR_ONLY)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        # closed folder:
        il.Add(wx.Bitmap(main.realPath(u'icons/folder.ico'),wx.BITMAP_TYPE_ICO))
        # open folder:
        il.Add(wx.Bitmap(main.realPath(u'icons/folder_open.ico'),wx.BITMAP_TYPE_ICO))
        # root of filesystem (linux):
        il.Add(wx.Bitmap(main.realPath(u'icons/root.ico'),wx.BITMAP_TYPE_ICO))
        # drive letter (windows):
        il.Add(wx.Bitmap(main.realPath(u'icons/hdd.ico'),wx.BITMAP_TYPE_ICO))
        # cdrom drive:
        il.Add(wx.Bitmap(main.realPath(u'icons/cdrom.ico'),wx.BITMAP_TYPE_ICO))
        # removable drive on win98:
        il.Add(wx.Bitmap(main.realPath(u'icons/floppy.ico'),wx.BITMAP_TYPE_ICO))
        # removable drive (floppy, flash, etc):
        il.Add(wx.Bitmap(main.realPath(u'icons/floppy.ico'),wx.BITMAP_TYPE_ICO))
        self.il = il
        self.GetTreeCtrl().SetImageList(il)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.dirChange)


    def dirChange(self,event):
        self.parent.path.SetValue(self.GetPath())
        self.parent.ShowPicker(event)

    def devNull(self, event):
        pass



class pickerPanel(wx.Panel):
    def sizer(self):
        PathSizer = wx.BoxSizer(wx.HORIZONTAL)
        SelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # right to left languages
        if main.langLTR:
            PathSizer.Add(self.BROWSE,0,wx.ALL, 5)
            PathSizer.Add(self.OK,0,wx.ALL, 5)
            PathSizer.Add(self.path,1,wx.ALIGN_CENTER|wx.RIGHT, 5)

            SelectSizer.Add(self.staticText1,0,wx.ALIGN_CENTER)
            SelectSizer.Add(self.not_type,0,wx.ALIGN_CENTER|wx.LEFT,4)
            SelectSizer.Add(self.fileType,1,wx.ALIGN_CENTER)
            SelectSizer.Add(self.filterByRE,0,wx.ALIGN_CENTER|wx.LEFT,5)
            SelectSizer.Add(self.ignoreCase,0,wx.ALIGN_CENTER|wx.LEFT,2)
            SelectSizer.Add(self.useLocale,0,wx.ALIGN_CENTER|wx.LEFT,2)
            SelectSizer.Add(self.divider1,0,wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT,7)
            SelectSizer.Add(self.select,0,wx.RIGHT|wx.ALIGN_CENTER,5)
            SelectSizer.Add(self.folders_on,0,wx.ALIGN_CENTER|wx.RIGHT,7)
            SelectSizer.Add(self.files_on,0,wx.ALIGN_CENTER|wx.RIGHT,5)
            SelectSizer.Add(self.walkIt,0,wx.ALIGN_CENTER|wx.RIGHT,7)
            SelectSizer.Add(self.select_all,0,wx.RIGHT,2)
            SelectSizer.Add(self.select_none,0)

            mainSizer.Add(self.path_help,0,wx.LEFT|wx.TOP|wx.EXPAND, 6)

        # left to right languages
        else:
            PathSizer.Add(self.path,1,wx.ALIGN_CENTER|wx.LEFT, 5)
            PathSizer.Add(self.OK,0,wx.ALL, 5)
            PathSizer.Add(self.BROWSE,0,wx.ALL, 5)

            SelectSizer.Add(self.select_none,0)
            SelectSizer.Add(self.select_all,0,wx.LEFT,2)
            SelectSizer.Add(self.walkIt,0,wx.ALIGN_CENTER|wx.LEFT,7)
            SelectSizer.Add(self.files_on,0,wx.ALIGN_CENTER|wx.LEFT,5)
            SelectSizer.Add(self.folders_on,0,wx.ALIGN_CENTER|wx.LEFT,7)
            SelectSizer.Add(self.select,0,wx.LEFT|wx.ALIGN_CENTER,5)
            SelectSizer.Add(self.divider1,0,wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT,7)
            SelectSizer.Add(self.useLocale,0,wx.ALIGN_CENTER|wx.LEFT,2)
            SelectSizer.Add(self.ignoreCase,0,wx.ALIGN_CENTER|wx.RIGHT,2)
            SelectSizer.Add(self.filterByRE,0,wx.ALIGN_CENTER|wx.RIGHT,5)
            SelectSizer.Add(self.fileType,1,wx.ALIGN_CENTER)
            SelectSizer.Add(self.not_type,0,wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT,5)
            SelectSizer.Add(self.staticText1,0,wx.ALIGN_CENTER)

            mainSizer.Add(self.path_help,0,wx.RIGHT|wx.TOP|wx.ALIGN_RIGHT|wx.EXPAND, 6)

        mainSizer.Add(PathSizer,0,wx.EXPAND|wx.ALIGN_CENTER)
        mainSizer.Add(SelectSizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND,5)
        mainSizer.Add(self.selectionArea,1,wx.EXPAND|wx.TOP, 3)

        self.SetSizerAndFit(mainSizer)

    def _init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PICKERPANEL, name=u'pickerPanel',
              parent=prnt, style=wx.NO_BORDER)


        self.path = wx.TextCtrl(id=wxID_PICKERPANELPATH, name=u'path',
              parent=self, style=wx.TE_PROCESS_ENTER, value='')
        self.path.Bind(wx.EVT_TEXT_ENTER, self.OnOkButton,
              id=wxID_PICKERPANELPATH)

        self.OK = wx.Button(id=wxID_PICKERPANELOK, label=_(u"OK"), name=u'OK',
              parent=self, style=0)
        self.OK.Enable(True)
        self.OK.SetToolTipString(_(u"Load or reload current path."))
        self.OK.Bind(wx.EVT_BUTTON, self.OnOkButton, id=wxID_PICKERPANELOK)

        self.BROWSE = wx.Button(id=wxID_PICKERPANELBROWSE, label=_(u"Browse"),
          name=u'BROWSE', parent=self, style=0)
        self.BROWSE.SetToolTipString(_(u"Browse for path."))
        self.BROWSE.Bind(wx.EVT_BUTTON, self.OnBROWSEButton,
          id=wxID_PICKERPANELBROWSE)

        self.path_help = wx.StaticText(id=wxID_PICKERPANELPATH_HELP,
              label=_(u"Input/Paste path and press OK, or BROWSE for path:"),
              name=u'path_help', parent=self, style=0)

        self.select = wx.StaticText(id=wxID_PICKERPANELSELECT, label=_(u"Select:"),
              name=u'select', parent=self, style=0)

        txt = _(u"all")
        self.select_all = wx.Button(id=wxID_PICKERPANELSELECT_ALL, label=txt,
              name=u'select_all', parent=self, style=0)
        Size = wx.Size(self.select_all.GetTextExtent(txt)[0] + 20,-1)
        self.select_all.SetMinSize(Size)
        self.select_all.Enable(False)
        self.select_all.Bind(wx.EVT_BUTTON, self.OnSelect_all,
              id=wxID_PICKERPANELSELECT_ALL)

        txt = _(u"none")
        self.select_none = wx.Button(id=wxID_PICKERPANELSELECT_NONE,
              label=txt, name=u'select_none', parent=self, style=0)
        Size = wx.Size(self.select_none.GetTextExtent(txt)[0] + 20,-1)
        self.select_none.SetMinSize(Size)
        self.select_none.Enable(False)
        self.select_none.Bind(wx.EVT_BUTTON, self.OnSelect_none,
              id=wxID_PICKERPANELSELECT_NONE)

        self.folders_on = wx.CheckBox(id=wxID_PICKERPANELFOLDERSON, label=_(u"Folders"),
              name=u'folders', parent=self, style=0,)
        self.folders_on.SetValue(True)
        self.folders_on.Bind(wx.EVT_CHECKBOX, self.ShowPicker,
              id=wxID_PICKERPANELFOLDERSON)

        self.files_on = wx.CheckBox(id=wxID_PICKERPANELFILESON, label=_(u"Files"),
              name=u'files', parent=self, style=0)
        self.files_on.SetValue(True)
        self.files_on.Bind(wx.EVT_CHECKBOX, self.ShowPicker,
              id=wxID_PICKERPANELFILESON)

        self.fileType = wx.TextCtrl(id=wxID_PICKERPANELFILETYPE,
              name=u'fileType', parent=self, style=wx.TE_PROCESS_ENTER, value='')
        self.fileType.SetToolTipString(_(u"Names containing:"))
        self.fileType.Bind(wx.EVT_TEXT_ENTER, self.ShowPicker,
              id=wxID_PICKERPANELFILETYPE)

        self.staticText1 = wx.StaticText(id=wxID_PICKERPANELSTATICTEXT1,
              label=_(u"Filter:"), name=u'staticText1', parent=self, style=0)

        self.filterByRE = wx.CheckBox(id=wxID_PICKERPANELFILTERBYRE, label=_(u"Reg-Expr"),
              name=u'filterByRE', parent=self, style=0)
        self.filterByRE.SetValue(False)
        self.filterByRE.SetToolTipString(_(u"Evaluate filter as a regular expression."))
        self.filterByRE.Bind(wx.EVT_CHECKBOX, self.REoptions,
              id=wxID_PICKERPANELFILTERBYRE)

        self.ignoreCase = wx.CheckBox(id=wxID_PICKERPANELIGNORECASE, label=_(u"I"),
              name=u'ignoreCase', parent=self, style=0)
        self.ignoreCase.SetValue(True)
        self.ignoreCase.Enable(False)
        self.ignoreCase.SetToolTipString(_(u"case-Insensitive match"))
        self.ignoreCase.Bind(wx.EVT_CHECKBOX, self.ShowPicker,
              id=wxID_PICKERPANELIGNORECASE)

        self.useLocale = wx.CheckBox(id=wxID_PICKERPANELUSELOCALE, label=_(u"U"),
              name=u'useLocale', parent=self, style=0)
        self.useLocale.SetValue(True)
        self.useLocale.Enable(False)
        self.useLocale.SetToolTipString(_(u"Unicode match (\w matches etc)"))
        self.useLocale.Bind(wx.EVT_CHECKBOX, self.ShowPicker,
              id=wxID_PICKERPANELUSELOCALE)

        self.walkIt = wx.CheckBox(id=wxID_PICKERPANELWALKIT, label=_(u"Walk"),
              name=u'walkIt', parent=self, style=0)
        self.walkIt.SetValue(False)
        self.walkIt.SetToolTipString(_(u"Get all files in directory and sub-directories, but no folders."))
        self.walkIt.Bind(wx.EVT_CHECKBOX, self.OnWalkItCheckbox,
              id=wxID_PICKERPANELWALKIT)

        self.not_type = wx.CheckBox(id=wxID_PICKERPANELNOT_TYPE, label=u"!=",
              name=u'not_type', parent=self, style=0)
        self.not_type.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.not_type.SetValue(False)
        self.not_type.SetToolTipString(_(u"NOT containing"))
        self.not_type.Bind(wx.EVT_CHECKBOX, self.ShowPicker,
              id=wxID_PICKERPANELNOT_TYPE)

        self.divider1 = wx.StaticLine(id=wxID_PICKERPANELDIVIDER1,
              name=u'divider1', parent=self, size=wx.Size(3, 22), style=wx.LI_VERTICAL)

        # create split window:
        self.selectionArea = wx.SplitterWindow(parent=self, id=wxID_SELECTIONAREA,
          name=u'selectionArea', style=wx.SP_LIVE_UPDATE)

        # directory picker:
        if main.prefs[u'useDirTree=']:
            self.createDirTree()

        # file picker:
        self.picker = wx.ListCtrl(id=wxID_SELECTIONAREAFPICKER, name=u'picker',
              parent=self.selectionArea, style=wx.LC_LIST)
        self.picker.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnPickerListItemSelected, id=wxID_SELECTIONAREAFPICKER)
        self.picker.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.picker.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        # images for picker:
        self.imgs = wx.ImageList(16, 16)
        self.imgs.Add(wx.Bitmap(main.realPath(u'icons/folder.ico'), wx.BITMAP_TYPE_ICO))
        self.imgs.Add(wx.Bitmap(main.realPath(u'icons/file.ico'), wx.BITMAP_TYPE_ICO))
        self.picker.SetImageList(self.imgs, wx.IMAGE_LIST_SMALL)

        self.initSplitter()


    def __init__(self, parent, main_window):
        global parnt
        parnt = parent
        global main
        main = main_window
        global root
        root = ''

        self.joinedItems = []
        self._init_ctrls(parent)
        self.sizer()

        self.BackgroundClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        self.HighlightClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.HighlightTxtClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.TxtClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        self.shiftDown = False
        self.totalSelected = 0


    # ---- create the directory tree:
    def createDirTree(self):
        self.dirPicker = DirControl(self.selectionArea, wxID_SELECTIONAREADIRPICKER, u'dirPicker', )
        if main.prefs['showHiddenDirs=']:
            self.dirPicker.ShowHidden(True)

    def initSplitter(self):
        # initialise split window based on preferences:
        if main.prefs['useDirTree=']:
            # right to left languages
            if main.langLTR:
                self.selectionArea.SplitVertically(self.dirPicker, self.picker, 275)
            else:
                self.selectionArea.SplitVertically(self.picker, self.dirPicker, -275)
        else:
            self.selectionArea.Initialize(self.picker)

    # ---- hide/show directory tree:
    def setTree(self):
        if main.prefs[u'useDirTree=']:
            self.createDirTree()
            self.dirPicker.SetPath(self.path.GetValue())
        else:
            self.selectionArea.Unsplit(self.dirPicker)
            self.dirPicker.Destroy()
        self.initSplitter()


    #---- get and set path:
    def OnBROWSEButton(self, event):
        dlg = wx.DirDialog(self,_(u"Choose a directory:"),
            style=wx.DD_DEFAULT_STYLE)
        dlg.SetPath(self.path.GetValue())
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                self.path.SetValue(dir)
                self.OnOkButton(event)
        finally: dlg.Destroy()

    #---- set path:
    def OnOkButton(self, event):
        if main.prefs[u'useDirTree=']:
            # keep a record of the original path
            path = self.path.GetValue()
            # need to temporarily unbind to avoid showing picker twice
            self.dirPicker.Bind(wx.EVT_TREE_SEL_CHANGED, self.dirPicker.devNull)
            try:
                self.dirPicker.SetPath(path)
            except AttributeError:
                pass
            # OK bind again
            self.dirPicker.Bind(wx.EVT_TREE_SEL_CHANGED, self.dirPicker.dirChange)
            # if tree won't display original path, force it
            if self.dirPicker.GetPath() != path:
                self.path.SetValue(path)
                self.ShowPicker(event)
            else:
                self.ShowPicker(event)
        # always refresh if dirpicker not there
        else:
            self.ShowPicker(event)


    # gets item info and parses it for inclusion in renaming list
    def GetItemInfo(self, i):
        item_txt = self.picker.GetItemText(i)
        item_txt = item_txt.lstrip(os.sep)
        fullItem = os.path.join(self.path.GetValue(),item_txt)
        IsFile = os.path.isfile(fullItem)
        fullItem = (fullItem,IsFile)
        return fullItem

    #---- select all button, adds all items to renaming list:
    def OnSelect_all(self, event):
        total_items = self.picker.GetItemCount()
        # clear list:
        self.joinedItems = []
        # only run if there's something there
        if total_items != 0:
            #print range(0,total_items)
            for i in range(total_items):
                #add to list :
                self.joinedItems.append(self.GetItemInfo(i))
                # show selected in picker:
                item = wx.ListItem()
                item.SetId(i)
                item.SetBackgroundColour(self.HighlightClr)
                item.SetTextColour(self.HighlightTxtClr)
                self.picker.SetItem(item)
            # enable buttons:
            self.select_none.Enable(True)
            main.menuPicker.getNoneMenu.Enable(True)
            self.select_all.Enable(False)
            main.menuPicker.getAllMenu.Enable(False)
            main.currentItem = None
            main.showPreview(True)

    #---- select none button, removes all items from renaming list:
    def OnSelect_none(self, event):
        total_items = self.picker.GetItemCount()
        # clear list:
        self.joinedItems = []
        # show deselected in picker:
        for i in range(total_items):
            item = wx.ListItem()
            item.SetId(i)
            item.SetBackgroundColour(self.BackgroundClr)
            item.SetTextColour(self.TxtClr)
            self.picker.SetItem(item)
        # enable buttons:
        self.select_all.Enable(True)
        main.menuPicker.getAllMenu.Enable(True)
        self.select_none.Enable(False)
        main.menuPicker.getNoneMenu.Enable(False)

        main.currentItem = None
        main.showPreview(True)


    # Need to know if shift is pressed to adjust selection
    def OnKeyDown(self, event):
        if event.m_keyCode == wx.WXK_SHIFT:
            self.shiftDown = True
        else:
            self.shiftDown = False

    def OnKeyUp(self, event):
        self.shiftDown = False
        if event.m_keyCode == wx.WXK_SHIFT:
            self.totalSelected = 0
            self.enableButtons()
            main.showPreview(True)

    # dis/enable buttons
    def enableButtons(self):
        total_items = self.picker.GetItemCount()
        if self.joinedItems != []:
            self.select_none.Enable(True)
            main.menuPicker.getNoneMenu.Enable(False)
            if len(self.joinedItems) == total_items:
                self.select_all.Enable(False)
                main.menuPicker.getAllMenu.Enable(False)
            else:
                self.select_all.Enable(True)
                main.menuPicker.getAllMenu.Enable(True)
        else:
            self.select_all.Enable(True)
            main.menuPicker.getAllMenu.Enable(True)
            self.select_none.Enable(False)
            main.menuPicker.getNoneMenu.Enable(False)


    #---- show selected items and add/remove from renaming list:
    def OnPickerListItemSelected(self, event):
        currentItem = event.m_itemIndex
        item = wx.ListItem()
        item.SetId(currentItem)
        fullItem = self.GetItemInfo(currentItem)

        # avoid selecting same item twice when using shift key
        if self.shiftDown:
            self.totalSelected += 1

        if self.totalSelected != 1:
            # add to list / show selected:
            if fullItem not in self.joinedItems:
                item.SetBackgroundColour(self.HighlightClr)
                item.SetTextColour(self.HighlightTxtClr)
                self.joinedItems.append(fullItem)
            # remove from list / show deselected:
            else:
                item.SetBackgroundColour(self.BackgroundClr)
                item.SetTextColour(self.TxtClr)
                self.joinedItems.remove(fullItem)
            # apply highlighting
            self.picker.SetItem(item)

        # Deselect item to avoid user confusion
        main.currentItem = None
        self.picker.Select(currentItem, False)

        if not self.shiftDown:
            self.enableButtons()
            main.showPreview(True)


    def ShowPicker(self, event):
        """
        This is the most important function for the picker.
        It will go and grab items from the specified directory,
        either as a listing or as a walk, and filter out entries
        based on user settings. Files and folders are seperated
        for proper sorting.
        This function is called, depending on user preferences -
        from almost every widget in the picker panel, and from
        main_window.py.
        """
        self.clearALL()
        files = [] #files will go here
        folders = [] #folders will go here
        err = False
        i = 0

        root = unicode(self.path.GetValue())
        # don't do anything for blank path:
        if not root:
            main.setStatusMsg('',u'eyes')
            main.display.DeleteAllItems()
        # don't do anything unless path is readable:
        elif not os.access(root, os.R_OK):
            main.setStatusMsg(_(u"Cannot read path!"),u'warn')
            main.display.DeleteAllItems()
        # OK, load items up:
        else:
            wx.BeginBusyCursor()
            self.select_none.Enable(False)
            main.menuPicker.getNoneMenu.Enable(False)
            main.go.Enable(False)
            main.setStatusMsg(_(u"Getting directory contents please wait ..."),u'wait')
            not_type = self.not_type.GetValue()
            folderOn = self.folders_on.GetValue()
            fileOn = self.files_on.GetValue()
            filter = self.fileType.GetValue()
            filterRE = self.filterByRE.GetValue()
            # are we searching by regular expression?
            if filter and filterRE:
                ignoreCase = self.ignoreCase.GetValue()
                useLocale = self.useLocale.GetValue()
                try:
                    #compile according to options:
                    if ignoreCase and useLocale:
                        filter = re.compile(filter, re.IGNORECASE | re.UNICODE)
                    elif ignoreCase:
                        filter = re.compile(filter, re.IGNORECASE)
                    elif useLocale:
                        filter = re.compile(filter, re.UNICODE)
                    else:
                        filter = re.compile(filter)
                except sre_constants.error:
                    useRE = False
                else:
                    useRE = True
            else:
                filter = filter.lower()
                useRE = False

            # create the search (filtering) operations...
            # normal filtering:
            if filter and not useRE:
                def filterFolders(entry):
                    if filter in entry.lower() and not not_type:
                        folders.append(entry)
                    if filter not in entry.lower() and not_type:
                        folders.append(entry)
                def filterFiles(entry):
                    if filter in entry.lower() and not not_type:
                        files.append(entry)
                    if filter not in entry.lower() and not_type:
                        files.append(entry)
            # regular expression filtering
            elif filter and useRE:
                def filterFolders(entry):
                    if filter.search(entry) and not not_type:
                        folders.append(entry)
                    if not filter.search(entry) and not_type:
                        folders.append(entry)
                def filterFiles(entry):
                    if filter.search(entry) and not not_type:
                        files.append(entry)
                    if not filter.search(entry) and not_type:
                        files.append(entry)
            # no filtering:
            else:
                def filterFolders(entry):
                    folders.append(entry)
                def filterFiles(entry):
                    files.append(entry)

            # Now to get the items according to operations defined above...
            # retrieve items by walking:
            if self.walkIt.GetValue():
                try:
                    for base, dirs, walk_files in os.walk(root):
                        main.Update()
                        base = base.replace(root,'')
                        for entry in walk_files:
                            entry = os.path.join(base,entry)
                            filterFiles(entry)
                        main.setStatusMsg(_(u"Retrieved %s items from directory.")%len(files),u'wait')
                except UnicodeDecodeError, err:
                    main.makeErrMsg(unicode(err), _("Unable to load item"))
                    err = True
                    pass
                except WindowsError:
                    main.setStatusMsg(_(u"Cannot read path!"),u'warn')
                    err = True
                    pass

            # normal retrieval:
            else:
                # Loop through items in directory:
                try:
                    listedDir = os.listdir(root)
                except WindowsError:
                    main.setStatusMsg(_(u"Cannot read path!"),u'warn')
                    err = True
                    pass
                else:
                    for entry in listedDir:
                        main.Update()
                        try:
                            isFolder = os.path.isdir(os.path.join(root, entry))
                        except UnicodeDecodeError, err:
                            entry = entry.decode(sys.getfilesystemencoding(), 'replace')
                            msg = _("%s\n%s\n\nAttempt to load more items from this directory?")%(entry,err)
                            dlg = wx.MessageDialog(self, msg, _("Unable to load item"), wx.YES_NO|wx.ICON_ERROR)
                            if dlg.ShowModal() == wx.ID_YES:
                                pass
                            else:
                                break
                        #load folders if set:
                        if folderOn and isFolder:
                            filterFolders(entry)
                        #load files if set:
                        if fileOn and not isFolder:
                            filterFiles(entry)

            # list folders in picker list first ...
            folders.sort(key=lambda x: x.lower())
            for i in range(len(folders)):
                self.picker.InsertImageStringItem(i, folders[i], 0)

            # ...then files:
            def make_key(f): return (os.path.dirname(f), f.lower())
            files.sort(key=make_key)
            i = len(folders)
            for item in files:
                self.picker.InsertImageStringItem(i, item, 1)
                i += 1

            # after retrieval:
            self.select_all.Enable(True)
            main.menuPicker.getAllMenu.Enable(True)
            main.display.DeleteAllItems()
            if not err:
                main.setStatusMsg(_(u"Retrieved %s items from directory.") %i,u'complete')
            wx.EndBusyCursor()

            if main.prefs[u'autoSelectAll=']:
                self.OnSelect_all(0)


    #---- Sorted retrieval of items.
    def GetItems(self):
        sorting = main.notebook.GetPage(2).sorting.GetSelection()
        dirsFirst = True
        # sort items?
        if sorting != 2 and dirsFirst:
            main.currentItem = None
            self.fc = 0
            def seperate(f):
                if f[1] == 0:
                    self.fc += 1
                return f[1]
            # sort list by file / folder:
            self.joinedItems.sort(key=seperate)
            # seperate files / folders:
            folders = self.joinedItems[:self.fc]
            files = self.joinedItems[self.fc:]
            # sort both:
            def make_key(x): return (os.path.dirname(x[0]), x[0].lower())
            folders.sort(key=lambda x: x[0].lower())
            files.sort(key=make_key)
            # join back together:
            self.joinedItems[:self.fc] = folders
            self.joinedItems[self.fc:] = files
            # reverse sort list?
            if sorting == 1:
                self.joinedItems.reverse()

        return self.joinedItems

    #---- clear stuff out
    def clearALL(self):
        self.joinedItems = []
        self.picker.DeleteAllItems()

    def walkFromMenu(self, event):
        self.walkIt.SetValue(True)
        self.OnWalkItCheckbox(event)

    def OnWalkItCheckbox(self, event):
        if self.walkIt.GetValue():
            self.folders_on.Enable(False)
            self.files_on.Enable(False)
        else:
            self.folders_on.Enable(True)
            self.files_on.Enable(True)
        self.ShowPicker(event)

    def REoptions(self, event):
        if self.filterByRE.GetValue():
            self.ignoreCase.Enable(True)
            self.useLocale.Enable(True)
        else:
            self.ignoreCase.Enable(False)
            self.useLocale.Enable(False)
        self.ShowPicker(event)


###### GET/SET CONFIGURATION SETTINGS: #########################################
    def getSettings(self):
        settings = (u"<[picker]>",
          u"path>:>%s" %self.path.GetValue(),
          u"not_type>:>%s" %int(self.not_type.GetValue()),
          u"fileType>:>%s" %self.fileType.GetValue(),
          u"filterByRE>:>%s" %int(self.filterByRE.GetValue()),
          u"ignoreCase>:>%s" %int(self.ignoreCase.GetValue()),
          u"useLocale>:>%s" %int(self.useLocale.GetValue()),
          u"folders>:>%s" %int(self.folders_on.GetValue()),
          u"files>:>%s" %int(self.files_on.GetValue()),
          u"walkIt>:>%s" %int(self.walkIt.GetValue()),
          )
        return settings

    def setSettings(self,settings):
        if len(settings) == 9: #make sure number of settings is correct
            try:
                if settings[0]:
                    self.path.SetValue(settings[0])
                    self.OnOkButton(0)
                self.not_type.SetValue(int(settings[1]))
                self.fileType.SetValue(settings[2])
                self.filterByRE.SetValue(int(settings[3]))
                self.ignoreCase.SetValue(int(settings[4]))
                self.useLocale.SetValue(int(settings[5]))
                self.folders_on.SetValue(int(settings[6]))
                self.files_on.SetValue(int(settings[7]))
                self.walkIt.SetValue(int(settings[8].replace('\n','')))
            except ValueError:
                return False
            else:
                self.OnWalkItCheckbox(False)
                self.REoptions(False)
                return True
        else:
            return False


