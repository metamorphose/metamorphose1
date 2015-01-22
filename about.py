# -*- coding: utf-8 -*-
#Boa:Dialog:About

# This is the about dialog.

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
import wx.lib.hyperlink as hl

def create(parent):
    return About(parent)

[wxID_ABOUT, wxID_ABOUTABOUT_TEXT, wxID_ABOUTCLOSE, wxID_ABOUTCOPYRIGHT,
 wxID_ABOUTGREET, wxID_ABOUTVERSION, wxID_ABOUTLINK, wxID_ABOUTDONATE,
 wxID_ABOUTCONTRIBUTORS, wxID_ABOUTDONATEBUTTON, wxID_ABOUTCONTRIBTXT
] = [wx.NewId() for _init_ctrls in range(11)]

class About(wx.Dialog):
    def sizer(self):
        self.bottomRow = wx.BoxSizer(wx.HORIZONTAL)
        self.bottomRow.Add(self.bugReport,0,wx.ALIGN_CENTER|wx.RIGHT,15)
        self.bottomRow.Add(self.featureRequest,0,wx.ALIGN_CENTER)

        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.CLOSE,0,wx.ALIGN_CENTER|wx.BOTTOM|wx.TOP,5)
        mainSizer.Add(self.greet,0,wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,7)
        mainSizer.Add(self.version,0,wx.ALIGN_CENTER|wx.BOTTOM,4)
        mainSizer.Add(self.copyright,0,wx.ALIGN_CENTER|wx.BOTTOM,2)
        mainSizer.Add(self.about_text,0,wx.ALIGN_CENTER|wx.BOTTOM,8)
        mainSizer.Add(self.donateButton,0,wx.ALIGN_CENTER|wx.BOTTOM,15)
        mainSizer.Add(self.contribtxt,0,wx.ALIGN_CENTER|wx.BOTTOM,1)
        mainSizer.Add(self.contributors,1,wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,5)
        mainSizer.Add((-1,15),0)
        mainSizer.Add(self.link,0,wx.ALIGN_CENTER|wx.BOTTOM,10)
        mainSizer.Add(self.bottomRow,0,wx.ALIGN_CENTER|wx.BOTTOM,10)
        self.SetSizerAndFit(mainSizer)

    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=wxID_ABOUT, name=u'About', parent=prnt,
              pos=wx.Point(400, 209), size=wx.Size(306, 400),
              style=wx.DEFAULT_DIALOG_STYLE, title=_(u"About Metamorphose"))
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/about.ico'),wx.BITMAP_TYPE_ICO))

        fontParams = prnt.fontParams
        fontSize = fontParams['size']
        fontFamily = fontParams['family']
        fontStyle = fontParams['style']

        self.SetFont(wx.Font(fontSize+1, fontFamily, fontStyle, wx.NORMAL, False, u'Times New Roman'))
        self.Center(wx.HORIZONTAL | wx.VERTICAL)
        self.SetThemeEnabled(True)

        self.greet = wx.StaticText(id=wxID_ABOUTGREET,
              label=u"Métamorphose file -n- folder renamer", name=u'greet',
              parent=self, pos=wx.Point(17, 144), style=0)
        self.greet.SetFont(wx.Font(fontSize+3, fontFamily, fontStyle, wx.BOLD, False,
              u'Times New Roman'))

        self.CLOSE = wx.BitmapButton(id=wxID_ABOUTCLOSE,
              bitmap=wx.Bitmap(prnt.realPath(u'icons/metamorphose128.png'), wx.BITMAP_TYPE_PNG),
              name=u'CLOSE', parent=self, style=wx.BU_AUTODRAW|wx.NO_BORDER)
        self.CLOSE.SetToolTipString(_(u"Click the trippy graphic to exit."))
        self.CLOSE.Bind(wx.EVT_BUTTON, self.OnCLOSEButton, id=wxID_ABOUTCLOSE)

        self.copyright = wx.StaticText(id=wxID_ABOUTCOPYRIGHT,
              label=u"Copyright © 2005-2008 Ianaré Sévi", name=u'copyright',
              parent=self, style=0)
        self.copyright.SetFont(wx.Font(fontSize+1, fontFamily, fontStyle, wx.BOLD, False,
              u'Times New Roman'))

        self.version = wx.StaticText(id=wxID_ABOUTVERSION,
              label=_(u"Version: %s")%prnt.version, name=u'version', parent=self,
              style=0)
        self.version.SetFont(wx.Font(fontSize+2, fontFamily, fontStyle, wx.BOLD, False,
              u'Times New Roman'))

        self.about_text = wx.StaticText(id=wxID_ABOUTABOUT_TEXT,
              label=_(u"GNU General Public License."), name=u'about_text', parent=self,
              style=0)
        self.about_text.SetAutoLayout(True)

        self.link = hl.HyperLinkCtrl(self, wxID_ABOUTLINK, _(u"Metamorphose Home Page"),
              URL=u'http://file-folder-ren.sourceforge.net/', style=0)

        self.donateButton = wx.Button(id=wxID_ABOUTDONATEBUTTON,
              label=_(u"Donate"), name=u'donateButton', parent=self, style=0)
        self.donateButton.SetFont(wx.Font(fontSize+5, fontFamily, fontStyle, wx.BOLD, False,
              u'Times New Roman'))
        self.donateButton.Bind(wx.EVT_BUTTON, self.OnDonateButton,
              id=wxID_ABOUTDONATEBUTTON)
        self.donateButton.SetToolTip(wx.ToolTip(_(u"Support Metamorphose !")))

        self.contribtxt = wx.StaticText(id=wxID_ABOUTCONTRIBTXT,
              label=_(u"Contributors:"), name=u'contribtxt', parent=self,
              style=0)
        self.contribtxt.SetFont(wx.Font(fontSize+1, fontFamily, fontStyle, wx.BOLD, False,
              u'Times New Roman'))

        self.contributors =  wx.TextCtrl(self, wxID_ABOUTCONTRIBUTORS,
                        u"Anthony DeCarvalho, Javier Prats, "
                        u"María Isabel Silva, Lucas Ontivero, "
                        u"Justin Nawrocki, Kevin Mullin, "
                        u"Attila Szervác, Zen, Jan Burkhart, "
                        u"Piotr Czajkowski, Atilla Merdan Nouryev, "
                        u"Gabriel Tillmann, Piotr Kwiliński, "
                        u"Gustavo Niemeyer, Stefano Madrucciani, "
                        u"Vittorio Patriarca, Zhang Ruichao, "
                        u"Kirill Shishkov, Anas Husseini, "
                        u"Shahar Fermon, Pierre-Yves Chibon, "
                        u"Erik Piehl, JEONG Hoe-Hwan, Tomas Klacko",
                        name=u'contributors', size=wx.Size(335,145),
                        style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.bugReport = hl.HyperLinkCtrl(self, wxID_ABOUTLINK, _(u"Bug Report"),
              URL=u'http://sourceforge.net/tracker/?func=add&group_id=146403&atid=765156', style=0)
        self.bugReport.SetToolTip(wx.ToolTip(_(u"Submit a bug report.")))


        self.featureRequest = hl.HyperLinkCtrl(self, wxID_ABOUTLINK, _(u"Feature Request"),
              URL=u'http://sourceforge.net/tracker/?func=add&group_id=146403&atid=765159', style=0)
        self.featureRequest.SetToolTip(wx.ToolTip(_(u"Submit a feature request.")))


        self.donate = hl.HyperLinkCtrl(self, wxID_ABOUTDONATE, '',
          URL=u'http://sourceforge.net/donate/index.php?group_id=146403', style=0)
        self.donate.Show(False)




    def __init__(self, parent):
        self._init_ctrls(parent)
        self.sizer()

    def OnCLOSEButton(self, event):
        self.Close()

    def OnDonateButton(self, event):
        self.donate.GotoURL("http://sourceforge.net/donate/index.php?group_id=146403")
