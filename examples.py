# -*- coding: utf-8 -*-
#Boa:Dialog:examples

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

def create(parent):
    return examples(parent)

[wxID_EXAMPLES, wxID_EXAMPLESDISPLAY, 
] = [wx.NewId() for _init_ctrls in range(2)]

class examples(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_EXAMPLES, name=u'examples', parent=prnt,
              size=wx.Size(548, 531),
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX, title=_(u"Examples"))
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/examples.ico'),wx.BITMAP_TYPE_ICO))
        self.SetMinSize(wx.Size(350, 200))

        self.display = wx.html.HtmlWindow(id=wxID_EXAMPLESDISPLAY,
              name=u'display', parent=self, size=wx.Size(540,
              504), style=wx.html.HW_SCROLLBAR_AUTO)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.Center(wx.HORIZONTAL|wx.VERTICAL)
        if u'gtk2' in wx.PlatformInfo:
            self.display.SetStandardFonts()

        langpath = parent.realPath(u'languages/en')
        self.display.LoadPage(os.path.join(langpath,u'examples.html'))
