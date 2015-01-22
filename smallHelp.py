# -*- coding: utf-8 -*-

# Panel that loads language-specific help file when available,
# otherwise load US English.

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
import wx.html
import os

def create(parent, helpFile, Title, Icon):
    return help(parent, helpFile, Title, Icon)

[wxID_HELP, wxID_HELP_DISPLAY, 
] = [wx.NewId() for _init_ctrls in range(2)]

class help(wx.Dialog):
    def _init_ctrls(self, prnt, Title, Icon):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_HELP, name=u'examples', parent=prnt,
              size=wx.Size(610, 531),
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX, title=Title)
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/%s.ico')%Icon,wx.BITMAP_TYPE_ICO))

        self.display = wx.html.HtmlWindow(id=wxID_HELP_DISPLAY,
              name=u'display', parent=self, size=wx.Size(602,
              520), style=wx.html.HW_SCROLLBAR_AUTO)

    def __init__(self, parent, helpFile, Title, Icon):
        self._init_ctrls(parent,Title,Icon)
        self.Center(wx.HORIZONTAL|wx.VERTICAL)
        if u'gtk2' in wx.PlatformInfo:
            self.display.SetStandardFonts()

        docspath = parent.realPath(u'docs')
        if os.path.isfile(os.path.join(docspath,parent.language,helpFile)):
            helpFile = os.path.join(docspath,parent.language,helpFile)            
        else:
            helpFile = os.path.join(docspath,u'en_US',helpFile)
            
        self.display.LoadPage(helpFile)

