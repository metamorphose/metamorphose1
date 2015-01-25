# -*- coding: utf-8 -*-
#
#Boa:Dialog:Preferences
#
# This is the preferences dialog box and functions to save the preferences.
#

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
import sys
import codecs

def create(parent):
    return Preferences(parent)

[wxID_PREFERENCES, wxID_PREFERENCESAUTOPREVIEWDATETIME,
 wxID_PREFERENCESAUTOPREVIEWMAIN, wxID_PREFERENCESAUTOPREVIEWNUMBERING,
 wxID_PREFERENCESAUTOPREVIEWPICKER, wxID_PREFERENCESAUTOSELECTALL,
 wxID_PREFERENCESAUTOSHOWERROR, wxID_PREFERENCESCANCEL,
 wxID_PREFERENCESCLEARUNDO, wxID_PREFERENCESENABLEUNDO,
 wxID_PREFERENCESENCODINGGROUP, wxID_PREFERENCESENCODINGSELECT,
 wxID_PREFERENCESMARKBADCHARS, wxID_PREFERENCESNOTEBOOK1,
 wxID_PREFERENCESRELOADAFTERRENAME, wxID_PREFERENCESSTATICBOX1,
 wxID_PREFERENCESSTATICTEXT1, wxID_PREFERENCESSTATICTEXT2,
 wxID_PREFERENCESSTATICTEXT3, wxID_PREFERENCESSTATICTEXT4,
 wxID_PREFERENCESUSEDIRTREE, wxID_PREFERENCESWINCHARS,
 wxID_PREFERENCESWINDOW1, wxID_PREFERENCESWINDOW2, wxID_PREFERENCESWINDOW3,
 wxID_PREFERENCESWINNAMES, wxID_PREFERENCESSTATICLINE1,
 wxID_PREFERENCESSTATICLINE2, wxID_PREFERENCESSTATICLINE3
] = [wx.NewId() for _init_ctrls in range(29)]

class Preferences(wx.Dialog):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.window1, select=True,
              text=_(u"General"))
        parent.AddPage(imageId=-1, page=self.window3, select=False,
              text=_(u"Automation"))
        parent.AddPage(imageId=-1, page=self.window2, select=False,
              text=_(u"Error Checking"))

    def sizer(self):
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        buttonSizer.Add(self.ok,0,wx.LEFT, 5)
        buttonSizer.Add((20,-1),0)
        buttonSizer.Add(self.cancel,0,wx.BOTTOM, 10)

        mainSizer.Add(self.notebook1,1,wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(buttonSizer,0,wx.EXPAND|wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM,5)

        self.SetSizerAndFit(mainSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_PREFERENCES, name=u'Preferences',
              parent=prnt, pos=wx.Point(493, 259),
              style=wx.DEFAULT_DIALOG_STYLE, title=_(u"Preferences"))
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/preferences.ico'),wx.BITMAP_TYPE_ICO))
        self.Center(wx.HORIZONTAL | wx.VERTICAL)

        self.ok = wx.Button(id=wx.ID_OK, name=u'ok',
              parent=self, style=0)

        self.cancel = wx.Button(id=wx.ID_CANCEL, name=u'cancel',
              parent=self, style=0)

        self.notebook1 = wx.Notebook(id=wxID_PREFERENCESNOTEBOOK1,
              name=u'notebook1', parent=self, pos=wx.Point(8, 8),
              style=0)

        self.window1 = wx.Window(id=wxID_PREFERENCESWINDOW1, name=u'window1',
              parent=self.notebook1, pos=wx.Point(0, 0), style=0)

        self.window2 = wx.Window(id=wxID_PREFERENCESWINDOW2, name=u'window2',
              parent=self.notebook1, pos=wx.Point(0, 0), style=0)

        self.window3 = wx.Window(id=wxID_PREFERENCESWINDOW3, name=u'window3',
              parent=self.notebook1, pos=wx.Point(0, 0), style=0)


        # -------------- window 1 ---------------- #

        self.clearUndo = wx.CheckBox(id=wxID_PREFERENCESCLEARUNDO,
              label=_(u"Clear out undo on start up"), name=u'clearUndo',
              parent=self.window1, pos=wx.Point(16, 16), style=0)
        self.clearUndo.SetValue(False)

        self.useDirTree = wx.CheckBox(id=wxID_PREFERENCESUSEDIRTREE,
              label=_(u"Use directory tree view"),
              name=u'useDirTree', parent=self.window1, pos=wx.Point(16, 60),
              style=0)
        self.useDirTree.SetValue(True)

        self.showHiddenDirs = wx.CheckBox(id=wxID_PREFERENCESUSEDIRTREE,
              label=_(u"Show Hidden directories in tree view"),
              name=u'showHiddenDirs', parent=self.window1, pos=wx.Point(32, 85),
              style=0)
        self.showHiddenDirs.SetValue(True)

        self.staticBox1 = wx.StaticBox(id=wxID_PREFERENCESSTATICBOX1,
              label=_(u"Encoding used in .mp3 id3 tags:"), name=u'staticBox1',
              parent=self.window1, pos=wx.Point(8, 125), size=wx.Size(325, 155),
              style=0)

        self.encodingGroup = wx.ComboBox(choices=[
                _(u"Use System Default"),
                _(u'All Languages'),
                _(u'Western Europe'),
                _(u'Central & Eastern Europe'),
                _(u'Esperanto, Maltese'),
                _(u'Nordic Languages'),
                _(u'Celtic Languages'),
                _(u'Baltic Languages'),
                _(u'Cyrillic Languages'),
                _(u'Greek'),
                _(u'Turkish'),
                _(u'Hebrew'),
                _(u'Arabic'),
                _(u'Urdu'),
                _(u'Thai'),
                _(u'Vietnamese'),
                _(u'Traditional Chinese'),
                _(u'Simplified Chinese'),
                _(u'Unified Chinese'),
                _(u'Korean'),
                _(u'Japanese'),
                ],
              id=wxID_PREFERENCESENCODINGGROUP, name=u'encodingGroup',
              parent=self.window1, pos=wx.Point(24, 167), size=wx.Size(295, -1), style=wx.CB_READONLY)
        self.encodingGroup.Bind(wx.EVT_COMBOBOX, self.SetEncodingOptions,
              id=wxID_PREFERENCESENCODINGGROUP)

        self.staticText2 = wx.StaticText(id=wxID_PREFERENCESSTATICTEXT2,
              label=_(u"Select encoding:"), name=u'staticText2',
              parent=self.window1, pos=wx.Point(24, 207), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PREFERENCESSTATICTEXT4,
              label=_(u"Select language group:"), name=u'staticText4', parent=self.window1,
              pos=wx.Point(24, 146), style=0)

        self.staticLine1 = wx.StaticLine(id=wxID_PREFERENCESSTATICLINE1,
              name='staticLine1', parent=self.window1, pos=wx.Point(300, 295),
              size=wx.Size(1, 1), style=0)

        self.staticLine2 = wx.StaticLine(id=wxID_PREFERENCESSTATICLINE2,
              name='staticLine1', parent=self.window1,
              pos=wx.Point(self.staticBox1.GetSize()[0]+20, 295),
              size=wx.Size(1, 1), style=0)



        # -------------- window 2 ---------------- #

        self.winNames = wx.CheckBox(id=wxID_PREFERENCESWINNAMES,
              label=_(u"Use Windows compatible names"), name=u'winNames',
              parent=self.window2, pos=wx.Point(16, 96), style=0)

        self.markBadChars = wx.CheckBox(id=wxID_PREFERENCESMARKBADCHARS,
              label=_(u"Mark name as bad, do not remove characters"),
              name=u'markBadChars', parent=self.window2, pos=wx.Point(32, 48),
              style=0)

        self.winChars = wx.CheckBox(id=wxID_PREFERENCESWINCHARS,
              label=_(u"Use Windows compatible characters"), name=u'winChars',
              parent=self.window2, pos=wx.Point(16, 16), style=0)
        self.winChars.Bind(wx.EVT_CHECKBOX, self.winOptions, id=wxID_PREFERENCESWINCHARS)
        self.winChars.SetToolTipString(_(u"Leave checked for maximum compatibility."))
        self.winChars.SetValue(True)

        self.autoShowError = wx.CheckBox(id=wxID_PREFERENCESAUTOSHOWERROR,
              label=_(u"Automatically show errors after preview"),
              name=u'autoShowError', parent=self.window2, pos=wx.Point(16, 144),
              style=0)


        # -------------- window 3 ---------------- #

        self.autoSelectAll = wx.CheckBox(id=wxID_PREFERENCESAUTOSELECTALL,
              label=_(u"Select all items when loading directory"),
              name=u'autoSelectAll', parent=self.window3, pos=wx.Point(16, 72),
              style=0)
        self.autoSelectAll.SetValue(False)

        self.reloadAfterRename = wx.CheckBox(id=wxID_PREFERENCESRELOADAFTERRENAME,
              label=_(u"Re-load directory contents after renaming"),
              name=u'reloadAfterRename', parent=self.window3, pos=wx.Point(16,
              16), style=0)
        self.reloadAfterRename.SetValue(False)

        self.staticText1 = wx.StaticText(id=wxID_PREFERENCESSTATICTEXT1,
              label=_(u"(When working with many items, this feature can be annoying.)"),
              name=u'staticText1', parent=self.window3, pos=wx.Point(40, 40),
              style=0)

        self.staticLine3 = wx.StaticLine(id=wxID_PREFERENCESSTATICLINE3,
              name='staticLine1', parent=self.window3,
              pos=wx.Point(self.staticText1.GetSize()[0]+50, 40),
              size=wx.Size(1, 1), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PREFERENCESSTATICTEXT3,
              label=_(u"Automatically preview selection when the following are modified:"),
              name=u'staticText3', parent=self.window3, pos=wx.Point(16, 120),
              style=0)

        self.autoPreviewPicker = wx.CheckBox(id=wxID_PREFERENCESAUTOPREVIEWPICKER,
              label=_(u"Picker panel"), name=u'autoPreviewPicker',
              parent=self.window3, pos=wx.Point(32, 136), style=0)

        self.autoPreviewMain = wx.CheckBox(id=wxID_PREFERENCESAUTOPREVIEWMAIN,
              label=_(u"-Main- panel"), name=u'autoPreviewMain',
              parent=self.window3, pos=wx.Point(32, 160), style=0)

        self.autoPreviewDateTime = wx.CheckBox(id=wxID_PREFERENCESAUTOPREVIEWDATETIME,
              label=_(u"Date and Time panel"), name=u'autoPreviewDateTime',
              parent=self.window3, pos=wx.Point(32, 208), style=0)

        self.autoPreviewNumbering = wx.CheckBox(id=wxID_PREFERENCESAUTOPREVIEWNUMBERING,
              label=_(u"Numbering Panel"), name=u'autoPreviewNumbering',
              parent=self.window3, pos=wx.Point(32, 184), style=0)
        self.autoPreviewNumbering.SetValue(False)

        self._init_coll_notebook1_Pages(self.notebook1)

    def makeEncodingSelect(self, choicesList):
        self.encodingSelect = wx.ComboBox(choices=choicesList,
              id=wxID_PREFERENCESENCODINGSELECT, name=u'encodingSelect',
              parent=self.window1, pos=wx.Point(24, 225), size=wx.Size(295, -1),
              style=wx.CB_READONLY)

    def __init__(self, prnt):
        global main
        main = prnt
        self._init_ctrls(main)
        self.prefs = main.getPrefs()
        self.encoding = ''
        self.encodingSelect = False #is this choice box there?

        self.sizer()

        self.staticLine1.Show(False)
        self.staticLine2.Show(False)
        self.staticLine3.Show(False)

        # call this after sizer to place properly:
        self.Center(wx.HORIZONTAL|wx.VERTICAL)

        #don't want the user to change these if on windows:
        if sys.platform == u'win32':
            win32stuff = (self.winChars, self.winNames)
            for winThing in win32stuff:
                winThing.Enable(False)
                winThing.SetValue(True)
        else:
            self.winChars.SetValue(self.prefs[u'useWinChars='])
            self.winNames.SetValue(self.prefs[u'useWinNames='])
        self.winOptions(1)

        #'normal' preferences:
        self.reloadAfterRename.SetValue(self.prefs[u'reloadAfterRename='])
        self.markBadChars.SetValue(self.prefs[u'markBadChars='])
        self.autoSelectAll.SetValue(self.prefs[u'autoSelectAll='])
        self.autoPreviewPicker.SetValue(self.prefs[u'autoPreviewPicker='])
        self.autoPreviewMain.SetValue(self.prefs[u'autoPreviewMain='])
        self.autoPreviewNumbering.SetValue(self.prefs[u'autoPreviewNumbering='])
        self.autoPreviewDateTime.SetValue(self.prefs[u'autoPreviewDateTime='])
        self.autoShowError.SetValue(self.prefs[u'autoShowError='])
        self.clearUndo.SetValue(self.prefs[u'clearUndo='])
        self.useDirTree.SetValue(self.prefs[u'useDirTree='])
        self.showHiddenDirs.SetValue(self.prefs[u'showHiddenDirs='])
        self.encodingGroup.SetSelection(self.prefs[u'encodingGroup='])

        #Create the encoding selector depending on encoding group:
        self.encodingOptions(self.encodingGroup.GetValue())

        # and assign it its value:
        self.encodingSelect.SetSelection(self.prefs[u'encodingSelect='])

    # enable windows name checkbox
    def winOptions(self, event):
        if self.winChars.GetValue():
            self.markBadChars.Enable(True)
        else:
            self.markBadChars.Enable(False)


    def setPrefs(self):
        try:
            prefFile = codecs.open(main.stdPath(u'preferences.ini'),'w', 'utf-8')
        except IOError, error:
            self.makeErrMsg(_(u"%s\n\nCould not load preferences, reverting to default settings.")%error, _(u"Error"))
            pass
        else:
            header = u"Métamorphose version %s\nManualy editing text files sucks, use the preferences menu.\n\n"%main.version
            preferences = [
              u'useWinChars=%s\n' %int(self.winChars.GetValue()),
              u'markBadChars=%s\n' %int(self.markBadChars.GetValue()),
              u'useWinNames=%s\n' %int(self.winNames.GetValue()),
              u'reloadAfterRename=%s\n' %int(self.reloadAfterRename.GetValue()),
              u'autoSelectAll=%s\n' %int(self.autoSelectAll.GetValue()),
              u'autoPreviewPicker=%s\n' %int(self.autoPreviewPicker.GetValue()),
              u'autoPreviewMain=%s\n' %int(self.autoPreviewMain.GetValue()),
              u'autoPreviewNumbering=%s\n' %int(self.autoPreviewNumbering.GetValue()),
              u'autoPreviewDateTime=%s\n' %int(self.autoPreviewDateTime.GetValue()),
              u'autoShowError=%s\n' %int(self.autoShowError.GetValue()),
              u'clearUndo=%s\n' %int(self.clearUndo.GetValue()),
              u'useDirTree=%s\n' %int(self.useDirTree.GetValue()),
              u'showHiddenDirs=%s\n' %int(self.showHiddenDirs.GetValue()),
              u'encodingGroup=%s\n' %self.encodingGroup.GetSelection(),
              u'encodingSelect=%s\n' %self.encodingSelect.GetSelection(),
              u'encoding=%s\n' %self.encodingSelect.GetValue(),
              ]
            # make the file:
            prefFile.write(header)
            for value in preferences:
                prefFile.write(value)
            prefFile.write(u"\n~ End Of File ~")
            prefFile.close()

    #called from choice box:
    def SetEncodingOptions(self, event):
        self.encodingOptions(event.GetString())

    def encodingOptions(self, Value):
        choicesLookup = {
                _(u"Use System Default") : [main.encoding],
                _(u'All Languages') : [u'utf_8',u'utf_16'],
                _(u'Western Europe') : [u'latin_1',u'windows-1252',u'iso-8859-15',u'mac_roman',u'cp500',u'cp850',u'cp1140'],
                _(u'Central & Eastern Europe') : [u'windows-1250',u'iso-8859-2',u'mac_latin2',u'cp852'],
                _(u'Esperanto, Maltese') : [u'iso-8859-3'],
                _(u'Nordic Languages') : [u'iso-8859-10',u'mac_iceland',u'cp861',u'cp865',],
                _(u'Celtic Languages') : [u'iso8859_14'],
                _(u'Baltic Languages') : [u'windows-1257',u'iso-8859-13',u'cp775'],
                _(u'Cyrillic Languages') : [u'windows-1251',u'iso-8859-5',u'koi8_r','koi8_u',u'mac_cyrillic',u'cp154',u'cp866',u'cp855',],
                _(u'Greek') : [u'windows-1253',u'iso-8859-7',u'mac_greek',u'cp737',u'cp869',u'cp875'],
                _(u'Turkish') : [u'windows-1254',u'iso-8859-9',u'mac_turkish',u'cp857',u'cp1026',],
                _(u'Hebrew') : [u'windows-1255',u'iso-8859-8',u'cp424',u'cp856',u'cp862',],
                _(u'Arabic') : [u'windows-1256',u'iso-8859-6',u'cp864',],
                _(u'Urdu') : [u'cp1006',],
                _(u'Thai') : [u'cp874',],
                _(u'Vietnamese') : [u'windows-1258',],
                _(u'Traditional Chinese') : [u'ms950',u'big5hkscs',u'big5',],
                _(u'Simplified Chinese') : [u'gb2312',u'hz',],
                _(u'Unified Chinese') : [u'ms936',u'gb18030',],
                _(u'Korean') : [u'ms949',u'iso-2022-kr',u'ms1361',u'euc_kr',],
                _(u'Japanese') : [u'ms-kanji',u'iso-2022-jp',u'shift_jis',u'euc_jp',u'iso-2022-jp-1',u'iso-2022-jp-2004',u'iso-2022-jp-3',u'iso-2022-jp-ext',u'shift_jis_2004',u'shift_jisx0213',u'euc_jis_2004',u'euc_jisx0213'],
                }
        enable = True
        if self.encodingSelect:
            self.encodingSelect.Destroy()
        if Value == _(u"Use System Default"):
            enable = False
        choicesList = choicesLookup[Value]
        self.staticText2.Enable(True)
        self.makeEncodingSelect(choicesList)
        self.encodingSelect.SetSelection(0)
        if not enable:
            self.staticText2.Enable(False)
            self.encodingSelect.Enable(False)

