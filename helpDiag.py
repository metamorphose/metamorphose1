# -*- coding: utf-8 -*-
#Boa:Dialog:help

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
import os
import wx.html

def create(parent):
    return help(parent)

[wxID_HELP, wxID_HELPHTMLWINDOW1, wxID_HELPHTMLWINDOW2, wxID_HELPHTMLWINDOW3,
 wxID_HELPHTMLWINDOW4, wxID_HELPHTMLWINDOW5, wxID_HELPNOTEBOOK1,
] = [wx.NewId() for _init_ctrls in range(7)]

class help(wx.Dialog):
    def _init_coll_notebook1_Pages(self, parent):
        parent.AddPage(imageId=-1, page=self.htmlWindow1, select=True,
              text=_(u"General"))
        parent.AddPage(imageId=-1, page=self.htmlWindow2, select=False,
              text=_(u"Picker"))
        parent.AddPage(imageId=-1, page=self.htmlWindow3, select=False,
              text=_(u"- Main -"))
        parent.AddPage(imageId=-1, page=self.htmlWindow4, select=False,
              text=_(u"Numbering"))
        parent.AddPage(imageId=-1, page=self.htmlWindow5, select=False,
              text=_(u"Date and Time"))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_HELP, name=u'help', parent=prnt,
              pos=wx.Point(323, 54), size=wx.Size(591, 600),
              style= wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER,
              title=_(u"Help"))
        self.SetMinSize(wx.Size(350, 220))
        self.SetClientSize(wx.Size(600, 570))
        self.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/help.ico'),wx.BITMAP_TYPE_ICO))

        self.notebook1 = wx.Notebook(id=wxID_HELPNOTEBOOK1, name=u'notebook1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(600, 571),
              style=wx.SUNKEN_BORDER)

        self.htmlWindow1 = wx.html.HtmlWindow(id=wxID_HELPHTMLWINDOW1,
              name=u'htmlWindow1', parent=self.notebook1, style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow2 = wx.html.HtmlWindow(id=wxID_HELPHTMLWINDOW2,
              name=u'htmlWindow2', parent=self.notebook1, style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow3 = wx.html.HtmlWindow(id=wxID_HELPHTMLWINDOW3,
              name=u'htmlWindow3', parent=self.notebook1, style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow4 = wx.html.HtmlWindow(id=wxID_HELPHTMLWINDOW4,
              name=u'htmlWindow4', parent=self.notebook1, style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow5 = wx.html.HtmlWindow(id=wxID_HELPHTMLWINDOW5,
              name=u'htmlWindow5', parent=self.notebook1, style=wx.html.HW_SCROLLBAR_AUTO)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.Center(wx.HORIZONTAL|wx.VERTICAL)

        # the base path
        docspath = parent.realPath(u'docs')

        # the notebook tabs
        notebookTabs = (self.htmlWindow1, self.htmlWindow2, self.htmlWindow3,
                        self.htmlWindow4, self.htmlWindow5)
        # the helpfiles
        helpFiles = [u'general_help.html', u'picker_help.html', u'main_help.html',
                     u'numbering_help.html', u'date_time_help.html']

        # fix for fonts too big in gtk:
        if u'gtk2' in wx.PlatformInfo:
            for tab in notebookTabs:
                tab.SetStandardFonts()

        # try to load the right file for the language, on fail default to US english
        i = 0
        for helpfile in helpFiles:
            if os.path.isfile(os.path.join(docspath,parent.language,helpfile)):
                helpFiles[i] = os.path.join(docspath,parent.language,helpfile)
            else:
                helpFiles[i] = os.path.join(docspath,u'en_US',helpfile)
            i += 1

        # display the file
        i = 0
        for tab in notebookTabs:
            tab.LoadPage(helpFiles[i])
            i += 1


