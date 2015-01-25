# -*- coding: utf-8 -*-
#Boa:FramePanel:errorPanel

# This is the error panel in the main
# application's notebook.

"""
Copyright (C) 2005-2010 Ianaré Sévi

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
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

[wxID_ERRORPANEL, wxID_ERRORPANELERRORSLIST
] = [wx.NewId() for _init_ctrls in range(2)]

class listCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        #CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class errorPanel(wx.Panel):
    def _init_coll_errorsList_Columns(self, parent):
        # generated method, don't edit
        if main.langLTR:
            align = wx.LIST_FORMAT_LEFT
        else:
            align = wx.LIST_FORMAT_RIGHT
        parent.InsertColumn(col=0, format=align, heading=_(u"Error"),width=200)
        parent.InsertColumn(col=1, format=align, heading=_(u"File"),width=-1)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_ERRORPANEL, name=u'errorPanel',
              parent=prnt, pos=wx.Point(295, 251), size=wx.Size(650, 302),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(642, 273))

        self.errorsList = listCtrl(self, wxID_ERRORPANELERRORSLIST,
              size=wx.Size(-1, -1), style=wx.LC_REPORT)
        self._init_coll_errorsList_Columns(self.errorsList)
        self.errorsList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnActivateError,
              id=wxID_ERRORPANELERRORSLIST)

    def __init__(self, parent, main_window):
        global main
        main = main_window

        self._init_ctrls(parent)
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.errorsList,1,wx.EXPAND|wx.TOP,3)
        self.SetSizerAndFit(mainSizer)


        # icons for error list:
        self.imgs = wx.ImageList(16, 16)
        self.warn = self.imgs.Add(wx.Bitmap(main.realPath(u'icons/warn.png'), wx.BITMAP_TYPE_PNG))
        self.bad = self.imgs.Add(wx.Bitmap(main.realPath(u'icons/failed.png'), wx.BITMAP_TYPE_PNG))
        self.errorsList.AssignImageList(self.imgs, wx.IMAGE_LIST_SMALL)


    def display_errors(self,errorLog, warn, bad, renameLength):
        errImgs = {u'warn':self.warn, u'bad':self.bad}
        total_problems = 0
        for error in errorLog:
            if not (error[0] in warn and error[0] in bad) or error[3] == u'bad':
                index = self.errorsList.InsertImageStringItem(0, u" "+error[2], errImgs[error[3]])
                self.errorsList.SetStringItem(index, 1, error[1])
                self.errorsList.SetItemData(index, error[0])
                total_problems += 1

        self.errorsList.SetColumnWidth(0, -1)
        self.errorsList.SetColumnWidth(1, -1)
        main.notebook.SetPageText(4,_(u"Errors/Warnings: %s") %total_problems)

        if len(warn) != 0 and len(bad) == 0:
            main.setStatusMsg(_(u"Ready to rename %s items, but with warnings.") %renameLength,u'warn')
        else:
            main.setStatusMsg(_(u"There are %s problems.") %total_problems,u'failed')



    def clear_errors(self):
        self.errorsList.DeleteAllItems()

    def OnActivateError(self, event):
        currentItem = event.m_itemIndex
        item_numb = self.errorsList.GetItemData(currentItem)
        main.display.EnsureVisible(item_numb)



