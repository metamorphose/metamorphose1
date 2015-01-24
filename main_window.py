# -*- coding: utf-8 -*-
#Boa:Frame:main_window
#
# This is the main application controls
# and the renaming functions.
#

"""
Copyright (c) 2005-2010 Ianaré Sévi

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

-

All translations also copyright (c) Ianaré Sévi, under BSD license.
This is only for ease of contributing translations to other OSS projects.
Credit for translations is obviously given to the translator !

----------------------------------------------------------------

Contributions:

2007-01-17
toAlpha function by Gustavo Niemeyer (gustavo@niemeyer.net)

"""

# needed modules:
import wx
import sys
import platform
import os
import codecs
import re
import wx.lib.buttons as buttons
import EnhancedStatusBar as ESB
import sre_constants
import time
import gettext
import locale
import EXIF
import calendar

# notebook windows:
import picker
import main
import numbering
import DateTime
import errors

# dialogs:
import preferences
import helpDiag
import about
import smallHelp
import langSelect


def create(parent):
    return main_window(parent)


[wxID_MAIN_WINDOW, wxID_MAIN_WINDOWDISPLAY, wxID_MAIN_WINDOWGO,
 wxID_MAIN_WINDOWNOTEBOOK, wxID_MAIN_WINDOWPREVIEW,
 wxID_MAIN_WINDOWSTATUSBAR1, wxID_MAIN_WINDOWSTATUSIMAGE,
 wxID_MAIN_WINDOWAUTOPREVIEW,
] = [wx.NewId() for _init_ctrls in range(8)]

[wxID_MAIN_WINDOWMENUHELPABOUT, wxID_MAIN_WINDOWMENUHELPHELP,
 wxID_MAIN_WINDOWMENUHELPEXAMPLES, wxID_MAIN_WINDOWMENUHELPREHELP,
 wxID_MAIN_WINDOWMENUHELPFORMATHELP
] = [wx.NewId() for _init_coll_menuHelp_Items in range(5)]

[wxID_MAIN_WINDOWMENUFILEEXIT, wxID_MAIN_WINDOWMENUFILEPREVIEW,
wxID_MAIN_WINDOWMENUFILEGO, wxID_MAIN_WINDOWMENUFILELOADINI,
wxID_MAIN_WINDOWMENUFILESAVEINI, wxID_MAIN_WINDOWMENUFILEBROWSE,
wxID_MAIN_WINDOWMENUFILEOK,
] = [wx.NewId() for _init_coll_menuFile_Items in range(7)]

[wxID_MAIN_WINDOWMENUPICKERALL, wxID_MAIN_WINDOWMENUPICKERNONE,
wxID_MAIN_WINDOWMENUPICKERWALK,
] = [wx.NewId() for _init_coll_menuPicker_Items in range(3)]

[wxID_MAIN_WINDOWMENUEDITPREFERENCES, wxID_MAIN_WINDOWMENUEDITUNDO,
wxID_MAIN_WINDOWMENUEDITLANG,
] = [wx.NewId() for _init_coll_menuEdit_Items in range(3)]

# the custom listcrtl class:
class listCtrl(wx.ListCtrl):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        self.parent = parent
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        if parent.langLTR:
            align = wx.LIST_FORMAT_LEFT
        else:
            align = wx.LIST_FORMAT_RIGHT

        self.InsertColumn(col=0, format=align, heading=_(u"Location"), width=205)
        self.InsertColumn(col=1, format=align, heading=_(u"Original Name"), width=225)
        self.InsertColumn(col=2, format=align, heading=_(u"New Name"), width=225)


# the main application class:
class main_window(wx.Frame):

    # use this to add spacing for translation
    def makeSpace(self,statusText):
        #if self.langLTR:
        #    return self.spacer+statusText
        #else:
        return self.spacer+statusText

    def _init_coll_menuBar_Menus(self, parent):
        # menu bar
        parent.Append(menu=self.menuFile, title=_(u"File"))
        parent.Append(menu=self.menuPicker, title=_(u"Picker"))
        parent.Append(menu=self.menuEdit, title=_(u"Edit"))
        parent.Append(menu=self.menuHelp, title=_(u"Help"))
        self.menuPicker.getAllMenu.Enable(False)
        self.menuPicker.getNoneMenu.Enable(False)
        self.menuFile.GoMenu.Enable(False)
        #if not self.prefs[u'enableUndo=']:
        #    self.menuEdit.UndoMenu.Enable(False)

    def _init_coll_menuEdit_Items(self, parent):
        # edit menu
        parent.PrefsMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUEDITPREFERENCES, _(u"Preferences"),
         self.makeSpace(_(u"Change your preferences")))
        parent.langMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUEDITLANG, _(u"Language"),
         self.makeSpace(_(u"Change the language")))
        parent.UndoMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUEDITUNDO, _(u"Undo\tctrl+Z"),
         self.makeSpace(_(u"Undo last renaming operation")))

        parent.PrefsMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/preferences.ico'),
            wx.BITMAP_TYPE_ICO))
        parent.AppendItem(parent.PrefsMenu)
        parent.langMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/language.png'),
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(parent.langMenu)
        parent.UndoMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/undo.ico'),
            wx.BITMAP_TYPE_ICO))
        parent.AppendItem(parent.UndoMenu)

        self.Bind(wx.EVT_MENU, self.OnMenuEditPreferencesMenu,
              id=wxID_MAIN_WINDOWMENUEDITPREFERENCES)
        self.Bind(wx.EVT_MENU, self.OnMenuEditUndoMenu,
              id=wxID_MAIN_WINDOWMENUEDITUNDO)
        self.Bind(wx.EVT_MENU, self.languageSelect,
              id=wxID_MAIN_WINDOWMENUEDITLANG)


    def _init_coll_menuHelp_Items(self, parent):
        # help menu
        parent.aboutMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUHELPABOUT, _(u"About"),
         self.makeSpace(_(u"Display general information about Metamorphose")))
        parent.aboutMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/about.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.helpMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUHELPHELP, _(u"&Help\tF1"),
         self.makeSpace(_(u"How to use Metamorphose")))
        parent.helpMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/help.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.examplesMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUHELPEXAMPLES, _(u"&Examples"),
         self.makeSpace(_(u"Some useful examples")))
        parent.examplesMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/examples.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.FormatHelpMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUHELPFORMATHELP, _(u"&Date/Time Formats"),
         self.makeSpace(_(u"Display a reference for Date & Time formats")))
        parent.FormatHelpMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/date_time.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.REhelpMenu = wx.MenuItem(parent,
         wxID_MAIN_WINDOWMENUHELPREHELP, _(u"&Regular Expressions"),
          self.makeSpace(_(u"Display a regular expression reference")))
        parent.REhelpMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/re.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.AppendItem(parent.aboutMenu)
        parent.AppendItem(parent.helpMenu)
        parent.AppendItem(parent.examplesMenu)
        parent.AppendItem(parent.FormatHelpMenu)
        parent.AppendItem(parent.REhelpMenu)

        self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
              id=wxID_MAIN_WINDOWMENUHELPABOUT)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpHelpMenu,
              id=wxID_MAIN_WINDOWMENUHELPHELP)
        self.Bind(wx.EVT_MENU, self.showSmallHelp,
              id=wxID_MAIN_WINDOWMENUHELPEXAMPLES)
        self.Bind(wx.EVT_MENU, self.showSmallHelp,
              id=wxID_MAIN_WINDOWMENUHELPFORMATHELP)
        self.Bind(wx.EVT_MENU, self.showSmallHelp,
              id=wxID_MAIN_WINDOWMENUHELPREHELP)


    def _init_coll_menuPicker_Items(self, parent):
        # picker menu
        parent.getAllMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUPICKERALL,
            _(u"Select &all\tctrl+A"), self.makeSpace(_(u"Select all items in picker")))
        parent.getAllMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/select_all.png'),
            wx.BITMAP_TYPE_PNG))
        parent.getNoneMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUPICKERNONE,
            _(u"Select &none\tctrl+N"), self.makeSpace(_(u"Deselect all items in picker")))
        parent.getNoneMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/select_none.png'),
            wx.BITMAP_TYPE_PNG))
        parent.walkMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUPICKERWALK,
            _(u"&Recursive selection (walk)\tctrl+W"), self.makeSpace(_(u"Get all files in directory and sub-directories, but no folders.")))
        parent.walkMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/walk.png'),
            wx.BITMAP_TYPE_PNG))

        parent.AppendItem(parent.getAllMenu)
        parent.AppendItem(parent.getNoneMenu)
        parent.AppendItem(parent.walkMenu)

        self.Bind(wx.EVT_MENU, self.notebook.GetPage(0).OnSelect_none,
              id=wxID_MAIN_WINDOWMENUPICKERNONE)
        self.Bind(wx.EVT_MENU, self.notebook.GetPage(0).OnSelect_all,
              id=wxID_MAIN_WINDOWMENUPICKERALL)
        self.Bind(wx.EVT_MENU, self.notebook.GetPage(0).walkFromMenu,
              id=wxID_MAIN_WINDOWMENUPICKERWALK)


    def _init_coll_menuFile_Items(self, parent):
        # file menu
        parent.browseMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILEBROWSE,
            _(u"&Browse...\tF4"),
            self.makeSpace(_(u"Browse for path.")))
        parent.browseMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/browse.png'),
            wx.BITMAP_TYPE_PNG))
        parent.okMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILEOK,
            _(u"&OK (load/reload)\tF5"), self.makeSpace(_(u"Load or reload current path")))
        parent.okMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/reload.png'),
            wx.BITMAP_TYPE_PNG))

        parent.LoadIniMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILELOADINI,
            _(u"&Load Config\tctrl+L"), self.makeSpace(_(u"Load configuration from file")))
        parent.LoadIniMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/loadIni.ico'),
            wx.BITMAP_TYPE_ICO))
        parent.SaveIniMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILESAVEINI,
            _(u"&Save Config\tctrl+S"), self.makeSpace(_(u"Save configuration to file")))
        parent.SaveIniMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/saveIni.ico'),
            wx.BITMAP_TYPE_ICO))

        parent.PreviewMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILEPREVIEW,
            _(u"&Preview\tF6"), self.makeSpace(_(u"Preview selection")))
        parent.PreviewMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/preview.png'),
            wx.BITMAP_TYPE_PNG))
        parent.GoMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILEGO,
            _(u"&Go !\tF7"), self.makeSpace(_(u"Rename selection")))
        parent.GoMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/go.png'),
            wx.BITMAP_TYPE_PNG))

        parent.exitMenu = wx.MenuItem(parent, wxID_MAIN_WINDOWMENUFILEEXIT,
            _(u"&Exit\tctrl+Q"), self.makeSpace(_(u"Exit Metamorphose")))
        parent.exitMenu.SetBitmap(wx.Bitmap(self.realPath(u'icons/exit.png'),
            wx.BITMAP_TYPE_PNG))

        parent.AppendItem(parent.browseMenu)
        parent.AppendItem(parent.okMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.LoadIniMenu)
        parent.AppendItem(parent.SaveIniMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.PreviewMenu)
        parent.AppendItem(parent.GoMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.exitMenu)

        self.Bind(wx.EVT_MENU, self.notebook.GetPage(0).OnBROWSEButton,
              id=wxID_MAIN_WINDOWMENUFILEBROWSE)
        self.Bind(wx.EVT_MENU, self.notebook.GetPage(0).OnOkButton,
              id=wxID_MAIN_WINDOWMENUFILEOK)
        self.Bind(wx.EVT_MENU, self.SaveCfg,
              id=wxID_MAIN_WINDOWMENUFILESAVEINI)
        self.Bind(wx.EVT_MENU, self.loadCfg,
              id=wxID_MAIN_WINDOWMENUFILELOADINI)
        self.Bind(wx.EVT_MENU, self.OnPreviewButton,
              id=wxID_MAIN_WINDOWMENUFILEPREVIEW)
        self.Bind(wx.EVT_MENU, self.OnGoButton,
              id=wxID_MAIN_WINDOWMENUFILEGO)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExitMenu,
              id=wxID_MAIN_WINDOWMENUFILEEXIT)

    def note_book(self):
        parent = self.notebook

        # make the notebook pages:
        pickerPanel = picker.pickerPanel(parent, self)
        mainPanel = main.mainPanel(parent, self)
        numberPanel = numbering.numberingPanel(parent, self)
        DateTimePanel = DateTime.Panel(parent, self)
        errorPanel = errors.errorPanel(parent, self)

        # add notebook pages to notebook:
        parent.AddPage(pickerPanel, _(u"Picker"))
        parent.AddPage(mainPanel, _(u"- Main -"))
        parent.AddPage(numberPanel, _(u"Numbering"))
        parent.AddPage(DateTimePanel, _(u"Date and Time"))
        parent.AddPage(errorPanel, _(u"Errors/Warnings: 0"))

        # list containing notebook images:
        il = wx.ImageList(16, 16)
        img0 = il.Add(wx.Bitmap(self.realPath(u'icons/picker.ico'), wx.BITMAP_TYPE_ICO))
        img1 = il.Add(wx.Bitmap(self.realPath(u'icons/main.ico'), wx.BITMAP_TYPE_ICO))
        img2 = il.Add(wx.Bitmap(self.realPath(u'icons/numbering.ico'), wx.BITMAP_TYPE_ICO))
        img3 = il.Add(wx.Bitmap(self.realPath(u'icons/date_time.ico'), wx.BITMAP_TYPE_ICO))
        img4 = il.Add(wx.Bitmap(self.realPath(u'icons/errors.ico'), wx.BITMAP_TYPE_ICO))

        # set images to pages:
        parent.AssignImageList(il)
        parent.SetPageImage(0, img0)
        parent.SetPageImage(1, img1)
        parent.SetPageImage(2, img2)
        parent.SetPageImage(3, img3)
        parent.SetPageImage(4, img4)

        # required to make XP theme colours ok:
        self.notebook.SetBackgroundColour(self.notebook.GetThemeBackgroundColour())

    def sizer(self):
        buttonSizer = self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        buttonElements = [(self.preview,0),
                          ((10,-1),0),
                          (self.go,0),
                          ((-1,-1),1),
                          (self.autoPreview,0),
                          ((-1,10),0)]
        # right to left languages
        if self.langLTR:
            for i in buttonElements:
                buttonSizer.Add(i[0],i[1],wx.ALIGN_CENTER)
        # left to right languages
        else:
            buttonElements.reverse()
            for i in buttonElements:
                buttonSizer.Add(i[0],i[1],wx.ALIGN_CENTER)

        mainSizer.Add(self.notebook,0,wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(buttonSizer,0,wx.EXPAND|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT,8)
        mainSizer.Add(self.display,1,wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(mainSizer)

    def _init_utils(self):
        self.menuFile = wx.Menu()
        self.menuPicker = wx.Menu()
        self.menuEdit = wx.Menu()
        self.menuHelp = wx.Menu()
        self.menuBar = wx.MenuBar()
        self._init_coll_menuFile_Items(self.menuFile)
        self._init_coll_menuPicker_Items(self.menuPicker)
        self._init_coll_menuEdit_Items(self.menuEdit)
        self._init_coll_menuHelp_Items(self.menuHelp)
        self._init_coll_menuBar_Menus(self.menuBar)
        self.SetMenuBar(self.menuBar)

    # get fonts from system or specify own
    def initFonts(self):
        if wx.Platform == '__WXGTK__':
            sysFont = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
            self.fontParams = {
                'size' : sysFont.GetPixelSize()[0],
                'style' : sysFont.GetStyle(),
                'family' : sysFont.GetFamily(),
                'weight' : sysFont.GetWeight(),
            }
        else:
            self.fontParams = {
                'size' : 9,
                'style' : wx.DEFAULT,
                'family' : wx.DEFAULT,
                'weight' : wx.DEFAULT,
            }
        #print self.fontParams
        self.SetFont(wx.Font(
            self.fontParams['size'],
            self.fontParams['family'],
            self.fontParams['style'],
            self.fontParams['weight'])
        )

    def _init_ctrls(self, prnt):
        self.SetTitle(u"Métamorphose")
        self.SetBackgroundColour(wx.NullColour)
        self.SetAutoLayout(False)
        self.SetStatusBarPane(0)
        self.SetIcon(wx.Icon(self.realPath(u'icons/metamorphose.ico'), wx.BITMAP_TYPE_ICO))
        self.SetThemeEnabled(True)
        self.initFonts()

        self.statusBar1 = ESB.EnhancedStatusBar(id=wxID_MAIN_WINDOWSTATUSBAR1,
              name=u'statusBar1', parent=self)
        self.SetStatusBar(self.statusBar1)

        self.statusImage = wx.StaticBitmap(bitmap=wx.Bitmap(self.realPath(u'icons/eyes.png'),
              wx.BITMAP_TYPE_PNG),
              id=wxID_MAIN_WINDOWSTATUSIMAGE, name=u'statusImage',
              parent=self.statusBar1, size=wx.Size(16, 16), style=0)

        if self.langLTR: SBalign = ESB.ESB_ALIGN_LEFT
        else: SBalign = ESB.ESB_ALIGN_RIGHT
        self.statusBar1.AddWidget(self.statusImage, SBalign)

        self.notebook = wx.Notebook(id=wxID_MAIN_WINDOWNOTEBOOK,
              name=u'notebook', parent=self, pos=wx.Point(10, 7),
              style=wx.NB_TOP)
        self.notebook.SetThemeEnabled(True)

        self.preview = buttons.GenBitmapTextButton(self, wxID_MAIN_WINDOWPREVIEW,
        wx.Bitmap(self.realPath(u'icons/preview.png'), wx.BITMAP_TYPE_PNG), _(u"Preview"),
          size=(-1, 26))
        self.Bind(wx.EVT_BUTTON, self.OnPreviewButton,
              id=wxID_MAIN_WINDOWPREVIEW)

        self.go = buttons.GenBitmapTextButton(self, wxID_MAIN_WINDOWGO,
          wx.Bitmap(self.realPath(u'icons/go.png'),wx.BITMAP_TYPE_PNG), _(u"Go!"), size=(-1, 26))
        self.go.Enable(False)
        self.go.Bind(wx.EVT_BUTTON, self.OnGoButton, id=wxID_MAIN_WINDOWGO)

        self.autoPreview = wx.CheckBox(id=wxID_MAIN_WINDOWAUTOPREVIEW,
          label=_(u"Automatic Preview"), name=u'autoPreview', parent=self,
          size=wx.Size(-1, -1), style=0)
        self.autoPreview.Bind(wx.EVT_CHECKBOX, self.autoPreviewCheckbox,
          id=wxID_MAIN_WINDOWAUTOPREVIEW)
        self.autoPreview.SetToolTipString(_(u"(According to settings in preferences)"))
        self.autoPreview.SetValue(True)

        self.display = listCtrl(self, wxID_MAIN_WINDOWDISPLAY,
              size=wx.Size(-1, 155), style=wx.LC_REPORT)
        self.display.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.display)


    def _init_language(self):
        self.language = ""

        try:# see if language file exist
            langIni = codecs.open(self.stdPath(u'language.ini'),'r', 'utf-8')
        except IOError:# have user choose language
            self.makeInitialEnvironment()
            language = self.languageSelect(0)
        else:# get language from file
            language = langIni.read()

        # reference
        locales = {
            u'ar' : (wx.LANGUAGE_ARABIC, u'ar_SA.UTF-8'),
            u'de' : (wx.LANGUAGE_GERMAN, u'de_DE.UTF-8'),
            u'el' : (wx.LANGUAGE_GREEK, u'el_GR.UTF-8'),
            u'en_GB' : (wx.LANGUAGE_ENGLISH_UK, u'en_GB.UTF-8'),
            u'en_US' : (wx.LANGUAGE_ENGLISH_US, u'en_US.UTF-8'),
            u'es' : (wx.LANGUAGE_SPANISH, u'es_ES.UTF-8'),
            u'fr' : (wx.LANGUAGE_FRENCH, u'fr_FR.UTF-8'),
            u'he' : (wx.LANGUAGE_HEBREW, u'he_IL.UTF-8'),
            u'hu' : (wx.LANGUAGE_HUNGARIAN, u'hu_HU.UTF-8'),
            u'it' : (wx.LANGUAGE_ITALIAN, u'it_IT.UTF-8'),
            u'ja' : (wx.LANGUAGE_JAPANESE, u'ja_JP.UTF-8'),
            u'ko' : (wx.LANGUAGE_KOREAN, u'ko_KR.UTF-8'),
            u'nl' : (wx.LANGUAGE_DUTCH, u'nl_NL.UTF-8'),
            u'pl' : (wx.LANGUAGE_POLISH, u'pl_PL.UTF-8'),
            u'pt_BR' : (wx.LANGUAGE_PORTUGUESE_BRAZILIAN, u'pt_BR.UTF-8'),
            u'ru' : (wx.LANGUAGE_RUSSIAN, u'ru_RU.UTF-8'),
            u'sk' : (wx.LANGUAGE_SLOVAK, u'sk_SK.UTF-8'),
            u'sv' : (wx.LANGUAGE_SWEDISH, u'sv_SE.UTF-8'),
            u'tr' : (wx.LANGUAGE_TURKISH, u'tr_TR.UTF-8'),
            u'zh_CN' : (wx.LANGUAGE_CHINESE_SIMPLIFIED, u'zh_CN.UTF-8'),
            }
        # right-to-left languages
        right_left_languages = ('ar','dv','fa','ha','he','ps','ur','yi')
        try:
            locales[language]
        except KeyError:
            print u"Could not initialise language: '%s'.\nContinuing in American English (en_US)\n"%language
            language = 'en_US'

        # needed for calendar and other things, send all logs to stderr
        wx.Log.SetActiveTarget(wx.LogStderr())

        # set locale and language
        wx.Locale(locales[language][0], wx.LOCALE_LOAD_DEFAULT)
        Lang = gettext.translation(u'metamorphose', self.localePath(language),
                                   languages=[locales[language][1]])
        Lang.install(unicode=True)

        # set some globals
        if language not in right_left_languages:
            self.langLTR = True
            self.alignment = wx.ALIGN_LEFT
        else:
            self.langLTR = False
            self.alignment = wx.ALIGN_RIGHT

        self.encoding = unicode(locale.getlocale()[1])
        self.language = language

        if platform.system() != 'Windows':
            try:
                # to get some language settings to display properly
                os.environ['LANG'] = locales[language][1]
            except (ValueError, KeyError):
                pass


    def __init__(self, prnt):
        self.version = self.getVersion()

        wx.Frame.__init__(self, id=wxID_MAIN_WINDOW, name=u'main_window',
              parent=prnt, pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.DEFAULT_FRAME_STYLE)
              
        # set language parameters
        self._init_language()

        # import these modules here since they need language settings activated
        global roman
        import roman
        global id3reader
        import id3reader

        # initialise preferences
        self.prefs = False
        self.prefs = self.getPrefs()

        # build main GUI
        self._init_ctrls(prnt)

        # init some globals
        global errorList
        errorList = []

        self.warn = [] # warnings
        self.bad = [] # errors
        self.errorLog = [] # errors
        self.items = [] # items to rename
        self.spacer = u" "*5 # spacer for status messages
        self.currentItem = None

        # clear undo (if set in preferences)
        if self.prefs[u'clearUndo=']:
            try:
                originalFile = codecs.open(self.stdPath(u'undo/original.bak'),'w', "utf-8")
                originalFile.write('')
                renamedFile = codecs.open(self.stdPath(u'undo/renamed.bak'),'w', "utf-8")
                renamedFile.write('')
            except IOError, error:
                self.makeErrMsg(_(u"%s\n\nCould not clear undo")%error, _(u"Error"))
                pass

        # construct rest of GUI
        self.note_book()
        self._init_utils()
        self.sizer()
        
        # call this after sizer to place properly
        self.Center(wx.HORIZONTAL|wx.VERTICAL)

        # Set root directory from command line arguments
        if len(sys.argv) > 1:
            path = ''
            for chunk in sys.argv[1:]:
                path += chunk + ' '
            path = path.rstrip()
            self.notebook.GetPage(0).path.SetValue(path)
            self.notebook.GetPage(0).OnOkButton(0)


##### MISC STUFF: ##############################################################
    # Little functions to make repetitive stuff easier to implement.

    # get version info from file
    def getVersion(self):
        try:
            f = open(self.realPath("version"))
        except:
            v = 'unknown'
        else:
            v = f.readline()
            f.close()
        return v
    
    # return application path
    def realPath(self, file):
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        else:
            path = ''
            for path in sys.path:
                if 'metamorphose' in path:
                    path = path.decode(sys.getfilesystemencoding())
                    break
            if path == '':
                print "Could not determine application path.\nMake sure the application is correctly installed.\n"
                sys.exit();
        #print path
        return os.path.join(path,file)

    # return locale directory
    def localePath(self, lang):
        if os.path.exists(u'/usr/share/locale/'+lang+u'/LC_MESSAGES/metamorphose.mo'):
            return u'/usr/share/locale'
        else:
            return self.realPath(u'messages')

    # return user path:
    def stdPath(self, file):
        base = wx.StandardPaths.Get().GetUserConfigDir()
        return os.path.join(base,u'.metamorphose',file)

    # Generic error messages
    def makeErrMsg(self, msg, title):
        dlg = wx.MessageDialog(self, msg, title, wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    # create necessary folders
    def makeInitialEnvironment(self):
        try:
            os.makedirs(self.stdPath('undo'))
        except OSError, error:
            if error[0] == 17:
                pass
            else:
                self.makeErrMsg(unicode(error), u"Error")
                pass

    # Call the preview function, if the user has set
    # so in preferences
    def showPreview(self, event):
        if self.prefs[u'autoPreviewPicker='] and event:
            self.OnPreviewButton(0)

    # open selection dialog for language
    def languageSelect(self, event):
        # if triggered from event, language has already been loaded,
        # and we will be changing it. No event = no language file
        if event == 0:
            Title = u"\m/ (>_<) \m/"
        else:
            Title = _(u"Language")
            event = self.language

        # show the language choices
        dlg = langSelect.create(self, Title, event)
        if dlg.ShowModal() == wx.ID_OK:
            language = dlg.GetLanguage()
            dlg.Destroy()
            if self.language != language:
                self.OnChangeLanguage(language, event)
            return language


    # write language.ini file
    def OnChangeLanguage(self, language, event):
        try:
            langFile = codecs.open(self.stdPath(u'language.ini'),'w', 'utf-8')
        except IOError, error:
            self.makeErrMsg(unicode(error), u"Error")
            pass
        else:
            langFile.write(language)
            langFile.close()
        if event:
            dlg = wx.MessageDialog(self, _(u"%s\n\nYou will need to restart Metamorphose")%language
              +_(u" to change the language.\n\nClose out of Metamorphose now?"),
              _(u"Change the Language"), wx.YES_NO | wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                if platform.system() == 'Linux' or platform.system() == 'FreeBSD':
                    try:
                        if wx.Process.Open(self.realPath(sys.argv[0])):
                            self.Close()
                    except (ValueError, KeyError):
                        pass
                else:
                    self.Close()


    # Set status bar text and image
    def setStatusMsg(self, msg, select):
        images = {
            u'failed' : wx.Bitmap(self.realPath(u'icons/failed.png'),wx.BITMAP_TYPE_PNG),
            u'wait' : wx.Bitmap(self.realPath(u'icons/wait.png'),wx.BITMAP_TYPE_PNG),
            u'warn' : wx.Bitmap(self.realPath(u'icons/warn.png'),wx.BITMAP_TYPE_PNG),
            u'complete' : wx.Bitmap(self.realPath(u'icons/complete.png'),wx.BITMAP_TYPE_PNG),
            u'eyes' : wx.Bitmap(self.realPath(u'icons/eyes.png'),wx.BITMAP_TYPE_PNG),
            }
        self.statusImage.SetBitmap(images[select])
        if self.langLTR:
            self.SetStatusText(self.makeSpace(msg))
        else:
            self.SetStatusText(self.makeSpace(self.spacer))

##### MENU ACTIONS: ############################################################
    # close out of application
    def OnMenuFileExitMenu(self, event):
        self.Close()

    #------- saves configuration file -------#
    def SaveCfg(self, event):
        cfgFile = ""
        # get each notebook tab's settings
        picker = self.notebook.GetPage(0).getSettings()
        main = self.notebook.GetPage(1).getSettings()
        numbering = self.notebook.GetPage(2).getSettings()
        dateTime = self.notebook.GetPage(3).getSettings()
        tabs = (picker, main, numbering, dateTime)

        # add settings to file
        for tab in tabs:
            for setting in tab:
                cfgFile = cfgFile + setting + u'\n'
            #line to seperate tabs in file:
            cfgFile = cfgFile + u'\n'

        # open up a save dialog
        dlg = wx.FileDialog(
            self, message=_(u"Save configuration as ..."), defaultDir=self.realPath(u'configs'),
            defaultFile=u'', wildcard=_(u"Configuration file (*.cfg)")+u'|*.cfg',
            style=wx.SAVE|wx.OVERWRITE_PROMPT
            )

        # attempt to write file
        if dlg.ShowModal() == wx.ID_OK:
            try:
                fp = codecs.open(dlg.GetPath(), 'w', 'utf_8')
            except (IOError, OSError), error:
                self.makeErrMsg(unicode(error), _(u"Error"))
                pass
            else:
                fp.write(unicode(cfgFile))
                fp.close()
        dlg.Destroy()


    #------ loads configuration file ------#
    def loadCfg(self, event):
        dlg = wx.FileDialog(
          self, message=_(u"Load a configuration file"), defaultDir=self.realPath(u'configs'),
          defaultFile=u'', wildcard=_(u"Configuration file (*.cfg)")+u'|*.cfg',
          style=wx.OPEN
          )
        if dlg.ShowModal() == wx.ID_OK:
            error = False
            div1 = re.compile(u'<\[.+\]>') #to split into tabs
            div2 = re.compile(u'\\n.+\>:>') #to split into settings

            fo = codecs.open(dlg.GetPath(), 'r', 'utf_8')
            settings = fo.read()
            settings = div1.split(settings) #split file data into tabs
            del settings[0]

            # run through each tab and...
            i = 0
            for set in settings:
                #... split into individual settings:
                settings[i] = div2.split(settings[i])
                #remove first (blank) setting:
                del settings[i][0]
                i += 1

            # ... check all tabs accounted for
            if len(settings) != 4:
                error = True
            """
            Now apply settings to each tab. Needs to go backwards
            so settings in config tabs are set before retrieving
            files and -possibly (depending on user preferences)-
            previewing selection.
            """
            # start by clearing stuff out:
            self.notebook.GetPage(0).clearALL()
            # this lets preview not to run while loading settings:
            self.items = u'config_load'
            i = 3
            while i >= 0 and not error:
                if not self.notebook.GetPage(i).setSettings(settings[i]):
                    #err_page = self.notebook.GetPage(i)
                    error = True #want to make sure settings loaded OK
                i -= 1

            if error:
                self.makeErrMsg(_(u"Configuration file may be corrupt.\n\nNote this doesn't mean ALL settings did not load."),
                  _(u"Error Loading Settings"))
            self.items = [] # loading done, preview enabled again.
            if self.prefs[u'autoPreviewPicker=']:
                self.OnPreviewButton(0)
            #clean up:
            fo.close()
        dlg.Destroy()

    # opens help dialog
    def OnMenuHelpHelpMenu(self, event):
        helpDiag.create(self).Show()

    # opens generic html help dialog
    def showSmallHelp(self, event):
        if event.GetId() == wxID_MAIN_WINDOWMENUHELPREHELP:
            helpFile=u'REhelp.html'
            Title=_(u"Regular Expression Help")
            Icon=u're'
        elif event.GetId() == wxID_MAIN_WINDOWMENUHELPFORMATHELP:
            helpFile=u'format.html'
            Title=_(u"Date and Time Formatting Help")
            Icon=u'date_time'
        elif event.GetId() == wxID_MAIN_WINDOWMENUHELPEXAMPLES:
            helpFile=u'examples.html'
            Title=_(u"Examples")
            Icon=u'examples'
        smallHelp.create(self,helpFile,Title,Icon).Show()

    # opens about dialog
    def OnMenuHelpAboutMenu(self, event):
        aboutDlg = about.create(self)
        aboutDlg.CentreOnParent()
        aboutDlg.ShowModal()



##### UNDO: ####################################################################
    # Grabs names from .bak files and reverts them to their originals.
    def OnMenuEditUndoMenu(self, event):
        original = []
        renamed = []
        wx.BeginBusyCursor()
        try:
            originalFile = codecs.open(self.stdPath(u'undo/original.bak'),'r', 'utf-8')
            renamedFile = codecs.open(self.stdPath(u'undo/renamed.bak'),'r', 'utf-8')
            for line in originalFile:
                original.append(line.replace(u'\n',''))
            for line in renamedFile:
                renamed.append((line.replace(u'\n',''),0))
        except IOError, error:
            self.makeErrMsg(_(u"%s\n\nUndo Failed !!")%error, _(u"Error"))
            pass
        else:
            if not len(original) == 0:
                global to_rename
                to_rename = zip(renamed,original) #reverse order from original rename!
                self.displayResults()
                self.OnGoButton(u'doNotReload')
                del to_rename
            else:
                self.setStatusMsg(_(u"Nothing to undo."), u'eyes')
        wx.EndBusyCursor()


#### PREFERENCES: ##############################################################

    #---- opens preferences dialog
    def OnMenuEditPreferencesMenu(self, event):
        oldDirTree = self.prefs[u'useDirTree=']
        oldSHowHiddenDirs = self.prefs[u'showHiddenDirs=']
        prefsDiag = preferences.create(self)
        # user presses ok, rewrite/reload preferences.ini
        if prefsDiag.ShowModal() == wx.ID_OK:
            prefsDiag.setPrefs()
            self.prefs = self.getPrefs()
            # apply changes:
            if self.prefs[u'autoPreviewPicker=']:
                self.OnPreviewButton(0)
            if self.prefs[u'useDirTree='] != oldDirTree:
                self.notebook.GetPage(0).setTree()
            if self.prefs[u'showHiddenDirs='] != oldSHowHiddenDirs:
                self.notebook.GetPage(0).dirPicker.ShowHidden(self.prefs[u'showHiddenDirs='])
        prefsDiag.Destroy()

    #---- main preferences
    def getPrefs(self):
        # Default preferences
        if platform.system() == 'Windows':
            winOn = 1
        else:
            winOn = 0

        preferences = {
          u'useWinChars=' : winOn,
          u'markBadChars=' : 0,
          u'useWinNames=' : winOn,
          u'reloadAfterRename=' : 0,
          u'autoSelectAll=' : 1,
          u'autoPreviewPicker=' : 1,
          u'autoPreviewMain=' : 1,
          u'autoPreviewNumbering=' : 1,
          u'autoPreviewDateTime=' : 1,
          u'autoShowError=' : 0,
          u'clearUndo=' : 0,
          u'useDirTree=' : 1,
          u'showHiddenDirs=' : winOn,
          u'encodingGroup=' : 0,
          u'encodingSelect=' : 0,
          u'encoding=' : self.encoding,
          }

        def createNewPreferences(prefFile):
            prefFile.truncate(0)
            header = u"Métamorphose version %s\n" % self.version
            header += u"Manually editing this text file is futile, use the preferences menu.\n\n"
            # make the file
            prefFile.write(header)
            for key, value in preferences.items():
                prefFile.write("%s%s\n"%(key, value))
            prefFile.write(u"\n~ End Of File ~\n\n")

        # make sure the file exist and is readable
        try:
            prefFile = codecs.open(self.stdPath(u'preferences.ini'),'r', 'utf_8')
        except (IOError, OSError):
            # otherwise create it:
            prefFile = codecs.open(self.stdPath(u'preferences.ini'),'w', 'utf-8')
            createNewPreferences(prefFile)

        # process preferences file and assign results to preferences dictionary
        else:
            prefFile.seek(0)
            # preferences are from prior version, create new file
            version = prefFile.readline().strip().replace(u"Métamorphose version ",'')
            if version[:2] != self.version[:2]:
                newPrefFile = codecs.open(self.stdPath(u'preferences.ini'),'w+', 'utf_8')
                createNewPreferences(newPrefFile)
                newPrefFile.seek(0)
                prefFile = newPrefFile

            for line in prefFile:
                line = line.replace(u'\n','')
                for pref in preferences:
                    if pref in line:
                        try:
                            preferences[pref] = int(line.replace(pref,''))
                        except KeyError:
                            pass
                        except ValueError:
                            preferences[pref] = unicode(line.replace(pref,''))
                            pass
            prefFile.close()

        # use windows-compatible file names?
        if preferences[u'useWinChars=']:
            preferences[u'bad_chars'] = (u'\\',u'/',u':',u'*',u'?',u'"',u'>',u'<',u'|')
        else:
            preferences[u'bad_chars'] = (unicode(os.sep)) #can't use path separator character!

        if preferences[u'useWinNames=']:
            preferences[u'bad_win_words'] = (u'con', u'prn', u'aux', u'clock$',
              u'nul', u'com1', u'com2', u'com3', u'com4', u'com5', u'com6', u'com7',
              u'com8', u'com9', u'lpt1', u'lpt2', u'lpt3', u'lpt4', u'lpt5',u'lpt6',
              u'lpt7', u'lpt8', u'lpt9')
        # encoding can't be integer
        preferences[u'encoding='] = unicode(preferences[u'encoding='])

        return preferences


    #---- checkbox modifier
    def autoPreviewCheckbox(self, event):
        if self.autoPreview.GetValue():
            self.prefs = self.getPrefs()
        else:
            self.prefs[u'autoPreviewPicker='] = 0
            self.prefs[u'autoPreviewMain='] = 0
            self.prefs[u'autoPreviewNumbering='] = 0
            self.prefs[u'autoPreviewDateTime='] = 0


#### NUMBERING: ###############################################################

    def toAlpha(self,i):
        s = ""
        while i:
            i -= 1
            q, m = divmod(i, 26)
            s = chr(97+m)+s
            i = q
        return s

    def enumber(self,file):
        global c
        count = number_params[1]
        dirReset = number_params[3]
        countByDir = number_params[4]

        # to reset count by directory
        if lastDir != curDir and dirReset and lastDir != u'begin':
            c = 0
        if lastDir != curDir and countByDir and lastDir != u'begin':
            c += 1

        # calculate current number based on user settings
        i = start + (c*int(count))
        reset = number_params[2]

        # numerical counting
        if numberStyle[0] == u'digit':
            pad_char = unicode(numberStyle[1])
            # padding enabled and non-empty pad charcter
            if numberStyle[3] and pad_char:
                if numberStyle[2] == u'auto':
                    pad_width = len(unicode(abs((len(self.items) + (start-1))*count)))
                    y = unicode(i).rjust(pad_width, pad_char)
                else:
                    y = unicode(i).rjust(int(numberStyle[2]), pad_char)
            # no padding
            else:
                y = i

        # alphabetical numbering
        elif numberStyle[0] == u'alpha':
            i = abs(i)
            if i == 0:
                i = 1
            y = self.toAlpha(i)
            # uppercase
            if numberStyle[1]:
                y = y.upper()

        # roman numerals baby!
        elif numberStyle[0] == u'roman':
            try:
                y = roman.toRoman(i)
                if not numberStyle[1]:
                    y = y.lower()
            except:
                if self.bad.count(self.ec) < 1:
                    self.bad.append(self.ec)
                    self.errorLog.insert(0,(self.ec,file,_(u"Roman numeral error: %s")%sys.exc_info()[1],u'bad'))
                y = ""

        # see if count is at reset level
        if c == reset and c != 0:
            c = 0
        elif not countByDir:
            c += 1

        return unicode(y)


#### DATE AND TIME: ############################################################
    def dateTime(self,op,path):
        dateTimePage = self.notebook.GetPage(3)
        dateTime = dateTimePage.dateTime
        dateTime[1] = dateTimePage.dateTestDisplay.GetValue()
        dateTime[2] = dateTimePage.timeTestDisplay.GetValue()

        # user specified date/time
        if not dateTime[0]:
            if op == 0:#date
                return dateTime[1]
            elif op == 1:#time
                return dateTime[2]
        # get date/time from item
        else:
            itemTimeType = dateTimePage.itemTimeType.GetSelection()
            if itemTimeType == 0:
                try: itemDateTime = time.localtime(os.path.getctime(path))
                except WindowsError: return ''
            elif itemTimeType == 1:
                try: itemDateTime = time.localtime(os.path.getmtime(path))
                except WindowsError: return ''
            elif itemTimeType == 2:
                try: itemDateTime = time.localtime(os.path.getatime(path))
                except WindowsError: return ''
            elif itemTimeType == 3:
                ec = self.ec
                warn = self.warn
                ext = os.path.splitext(path)[1][1:].lower()
                if re.match('tif|tiff|jpg|jpeg|jtif|thm', ext):
                    try:
                        file = open(path,'rb')
                    except IOError:
                        if warn.count(ec) < 1:
                            warn.append(ec)
                            self.errorLog.insert(0,(ec,path,_(u"Could not read EXIF tag"),u'warn'))
                        return ''
                    else:
                        tag = 'EXIF DateTimeOriginal'
                        tags = EXIF.process_file(file,details=False)
                        # only process if tag exists
                        if tags.has_key(tag):
                            itemDT = str(tags[tag])
                            itemDateTime = re.compile(r'\D').split(itemDT)
                            for i in range(len(itemDateTime)):
                                itemDateTime[i] = int(itemDateTime[i])

                            # some dates are returned in US format
                            if '/' in itemDT:
                                year = itemDateTime[2]
                                day = itemDateTime[1]
                                month = itemDateTime[0]
                            # ISO standard date
                            else:
                                year = itemDateTime[0]
                                month = itemDateTime[1]
                                day = itemDateTime[2]
                            itemDateTime[0] = year
                            itemDateTime[1] = month
                            itemDateTime[2] = day

                            # attempt to convert tag text to date
                            try:
                                dayWeek = calendar.weekday(itemDateTime[0],itemDateTime[1],itemDateTime[2])
                            # invalid date
                            except ValueError, err:
                                if warn.count(ec) < 1:
                                    warn.append(ec)
                                    self.errorLog.insert(0,(ec,path,_(u"EXIF error: %s")%err,u'warn'))
                                return ''
                            else:
                                itemDateTime.extend([dayWeek, 1, 0])
                        # date tag doesn't exist
                        else:
                            if warn.count(ec) < 1:
                                warn.append(ec)
                                self.errorLog.insert(0,(ec,path,_(u"Could not read EXIF tag"),u'warn'))
                            return ''
                else:
                    return ''

            # all encode/decode crap is a workaround for strftime not accepting unicode
            def uDate(format):
                udate = time.strftime(format.encode(self.encoding),itemDateTime)
                return udate.decode(self.encoding)
            if op == 0:#date
                return uDate(dateTime[1])
            elif op == 1:#time
                return uDate(dateTime[2])


#### PARSE INPUT AND FORMAT: ###################################################
    """
    This function is called by each field in the '- Main -' tab when the
    preview button is clicked. Basically just calls other functions depending
    on what the user input into the field.
    """
    def ParseInput(self,text,file):
        ec = self.ec
        warn = self.warn
        bad  = self.bad
        # possible commands
        commands = (_(u"numb"),_(u"date"),_(u"time"),_(u"album"), _(u"performer"), _(u"title"),
              _(u"track"), _(u"year"), _(u"genre"))
        parsedText = u''

        # any text in between this character is considered an operation
        text = text.split(u':')

        # execute functions based on user input
        for segment in text:
            if segment == commands[0]:
                parsedText = parsedText + self.enumber(file)
            elif segment == commands[1]:
                parsedText = parsedText + self.dateTime(0,file)
            elif segment == commands[2]:
                parsedText = parsedText + self.dateTime(1,file)
            elif segment in commands[3:]:
                ext = os.path.splitext(file)[1].lower()
                for command in commands[3:]:
                    if segment == command and ext == u'.mp3':
                        try:
                            id3r = id3reader.Reader(file)
                            value = id3r.getValue(command, self.prefs[u'encoding='])
                        except AttributeError:
                            if warn.count(ec) < 1:
                                warn.append(ec)
                                self.errorLog.insert(0,(ec,file,_(u"Could not read id3 tag: %s")%command,u'warn'))
                            pass
                        except UnicodeDecodeError:
                            if warn.count(ec) < 1:
                                warn.append(ec)
                                self.errorLog.insert(0,(ec,file,_(u"id3 encoding error"),u'warn'))
                            pass
                        except IOError:
                            if bad.count(ec) < 1:
                                self.errorLog.insert(0,(ec,file,_(u"Could not open file!"),u'bad'))
                        except:
                            if warn.count(ec) < 1:
                                warn.append(ec)
                                self.errorLog.insert(0,(ec,file,_(u"id3 error: %s")%sys.exc_info()[1],u'warn'))
                            pass
                        else:
                            parsedText = parsedText + value
            # if operation doesn't match a command, do nothing
            else:
                parsedText = parsedText + segment
        return parsedText


#### ERROR CHECKING: ###########################################################
    def errorCheck(self,renamedItem,itemToRename,path,items_ren):
        """
        Here we do final error checking and optional character stripping.
        Run for each name to be renamed.
        """
        bad = self.bad
        warn = self.warn
        errorLog = self.errorLog
        ec = self.ec
        #------------ ERRORS: ---------------#
        # strip off or flag invalid characters (depends on user settings)
        x = 0
        for char in self.prefs[u'bad_chars']:
            if not self.prefs[u'markBadChars=']:
                renamedItem = renamedItem.replace(char,'')
            else:
                if char in renamedItem and x < 1:
                    bad.append(ec)
                    errorLog.insert(0,(ec,itemToRename,_(u"Invalid character: %s")%char,u'bad'))
                    x += 1
                # flag bad words
        if self.prefs[u'useWinNames=']:
            for word in self.prefs[u'bad_win_words']:
                if renamedItem.lower() == word:
                    bad.append(ec)
                    errorLog.insert(0,(ec,itemToRename,_(u"Invalid name: %s")%word,u'bad'))
        # completly blank
        if renamedItem == "":
            bad.append(ec)
            errorLog.insert(0,(ec,itemToRename,_(u"Completely blank"),u'bad'))
        # nothing over 255 characters allowed
        elif len(renamedItem) > 255:
            #if bad.count(ec) < 1:
            bad.append(ec)
            errorLog.insert(0,(ec,itemToRename,_(u"Name length over 255 characters"),u'bad'))

        # no dupes (must be last ERROR check)
        if os.path.join(path,renamedItem) in items_ren:
            if ec not in bad:
                bad.append(ec)
                errorLog.insert(0,(ec,itemToRename,_(u"Duplicate name"),u'bad'))

        #------------ WARNINGS: ---------------#
        # blank file name, but extension is there
        # check original name too, to avoid flagging hidden files in *nix.
        leaf = os.path.split(itemToRename)[1]
        newBlank = re.search("^\..+",renamedItem)
        oldBlank = re.search("^\..+",leaf)
        if  (newBlank != None and oldBlank == None) and ec not in warn\
         and ec not in bad and os.path.isfile(itemToRename):
            warn.append(ec)
            errorLog.insert(0,(ec,itemToRename,_(u"Blank file name"),u'warn'))

        return renamedItem


##### RENAMING PREVIEW: ########################################################
    """
    this is the main function, it parses user settings, goes through
    each item to be renamed and applies renaming operations. Results are
    stored in the dictionary 'to_rename' and arranged like so
    'original name : renamed name'. The dictionary is used by the rename
    function (OnGoButton()) to do the actual renaming.
    """
    def generatePreview(self, main_page, main_pos, apply_to_name, apply_to_ext):
        global to_rename # dictionary
        global lastDir # last directory acessed
        lastDir = u'begin'
        global curDir # current directory

        prefixText = main_page.prefix_txt.GetValue()
        suffixText = main_page.suffix_txt.GetValue()

        bad = self.bad = []
        warn = self.warn = []
        errorLog = self.errorLog = []
        items_ren = []
        self.ec = 0
        ec = self.ec # bad/warn items counter
        REmsg = False # is there a regular expression warn message?
        dirMatch = [] # for storing directory matches

        """
        First go through each activated rename operation and get as many
        variables defined, functions set up, et cetera. This way these can
        be used in the loop without having to recalculate them for every
        item.
        """
        #---- sub-directories:
        if main_pos[0]:
            SubDir_txt = main_page.SubDir_txt.GetValue()
            dirMatch = SubDir_txt.split(u':/')

        #---- Replacement/modification
        if main_pos[3]:
            #- get values from widgets
            # true/false values
            text_find = main_page.repl_textButton.GetValue()
            regexp_find = main_page.reg_expr.GetValue()
            position_find = main_page.repl_posButton.GetValue()
            text_sensitive = main_page.repl_case.GetValue()
            # string value
            REtxt = main_page.reg_exp_text.GetValue()
            moveTxt = ''
            moveTo = ''

            #---- input -----#
            #- normal search:
            if text_find:
                find = main_page.repl_find.GetValue()
            #- regular expression search
            elif regexp_find:
                a_z = main_page.a_z.GetValue()
                digit = main_page.digit.GetValue()
                #format for character sets
                if a_z or digit:
                    invert = main_page.inverse.GetValue() # inverses the set
                    REfind = u'['
                    if a_z and not invert:
                        REfind = REfind + u'^\W\d'
                    elif a_z and invert:
                        REfind = REfind + u'\W\d'
                    if digit and not invert:
                        REfind = REfind + u'\d'
                    elif digit and invert:
                        REfind = REfind + u'\D'
                    REfind = REfind + u']'

                    # add regular expression
                    if REtxt != '':
                        REfind = REfind + u'|('+ REtxt + u')'
                # normal regular expression
                else:
                    REfind = REtxt

                # now ready to compile expression
                ignoreCase = main_page.reg_exp_i.GetValue()
                useLocale = main_page.reg_exp_u.GetValue()
                try:
                    # compile according to options
                    if ignoreCase and useLocale:
                        mod = re.compile(REfind, re.IGNORECASE | re.UNICODE)
                    elif ignoreCase:
                        mod = re.compile(REfind, re.IGNORECASE)
                    elif useLocale:
                        mod = re.compile(REfind, re.UNICODE)
                    else:
                        mod = re.compile(REfind)
                except sre_constants.error, err:
                    # make blank regular expression
                    mod = re.compile(r'')
                    # give user a descriptive error message
                    msg = _(u"Regular-Expression: %s")%err
                    self.setStatusMsg(msg,u'warn')
                    # so we know not to change status text after re error msg
                    REmsg = True
                    pass

            #---- output -----#
            #- replacement
            if main_page.repl_replace.GetValue():
                text = main_page.repl_txt.GetValue()
            #- modification
            elif main_page.repl_operation.GetValue():
                # Definitions for modifications
                def Uppercase(match):
                    if regexp_find and REfind:
                        return match.group().upper()
                    else:
                        return match.upper()
                def Lowercase(match):
                    if regexp_find and REfind:
                        return match.group().lower()
                    else:
                        return match.lower()
                def Capitalize(match):
                    if regexp_find and REfind:
                        return match.group().capitalize()
                    else:
                        return match.capitalize()
                def Title(match):
                    if regexp_find and REfind:
                        return match.group().title()
                    else:
                        return match.title()
                def Swapcase(match):
                    if regexp_find and REfind:
                        return match.group().swapcase()
                    else:
                        return match.swapcase()
                def Dorkify(match):
                    if regexp_find and REfind:
                        match = match.group()
                    i = 0
                    new_string = ''
                    for char in match:
                        i += 1
                        if i == 2:
                            new_string = new_string + char.lower()
                            i = 0
                        else:
                            new_string = new_string + char.upper()
                    return new_string

                # possible modifications
                commands = (Uppercase,Lowercase,Swapcase,Capitalize,Title,Dorkify)
                # selected operation
                op = main_page.repl_operation_value.GetSelection()
            #- move
            else:
                moveTo = u':Do_Not_Move:'
                moveMod = main_page.repl_move_txt_mod.GetStringSelection()
                # by position
                if main_page.repl_move_pos.GetValue():
                    moveByPosition = True
                    moveTo = main_page.repl_move_pos_value.GetValue()
                # by searching for text
                else:
                    moveByPosition = False
                    moveTxt = main_page.repl_move_txt_value.GetValue()
                    moveRE = False
                    # regular expression
                    if main_page.repl_move_txt_re.GetValue():
                        try:
                            moveRE = re.compile(moveTxt)
                        except sre_constants.error, err:
                            msg = _(u"Regular-Expression: %s")%err
                            self.setStatusMsg(msg,u'warn')
                            # so we know not to change status text after RE error msg
                            REmsg = True
                            pass

        #---- insert at position
        if main_pos[4]:
            insertText = main_page.insert_txt.GetValue()

        #---- Modify length
        if main_pos[5]:
            type = main_page.mod_length_type.GetSelection()# 0 = cut, 1 = pad, 2 = both
            width = int(main_page.mod_length.GetValue())
            direction = main_page.mod_length_direction.GetSelection()# 0 = right, 1 = left
            position = main_page.mod_length_position.GetValue()
            padChar = unicode(main_page.mod_length_pad.GetValue())
            def truncate(renamed_name):
                if direction == 1:# right
                    cut = len(renamed_name) - width
                    if cut < 0: cut = 0
                    renamed_name = renamed_name[cut:]
                else:
                    renamed_name = renamed_name[:width]
                return renamed_name
            def pad(renamed_name):
                if direction == 0 and position == 0 and padChar:
                    renamed_name = renamed_name.ljust(width, padChar)
                elif direction == 1 and position == 0 and padChar:
                    renamed_name = renamed_name.rjust(width, padChar)

                # padding by inserting at position
                else:
                    padSize = width - len(renamed_name)
                    renamed_name = renamed_name[:position] + unicode(padChar*padSize) + renamed_name[position:]
                return renamed_name
            if type == 0:#cut
                def modifyOp(renamed_name):
                    return truncate(renamed_name)
            elif type == 1:#pad
                def modifyOp(renamed_name):
                    return pad(renamed_name)
            elif type == 2:#both
                def modifyOp(renamed_name):
                    if len(renamed_name) < width:
                        return pad(renamed_name)
                    elif len(renamed_name) > width:
                        return truncate(renamed_name)
                    else:
                        return renamed_name

        def searchReplaceModifyMove(renamed_name, moveTxt, moveTo):
            #-- case insensitive regular search
            if text_find and not text_sensitive:
                found = None
                CI_find = find.lower()
                CI_renamed = renamed_name.lower()
                # no need to run whole operation if not found at all
                if CI_find in CI_renamed:
                    find_len = len(CI_find)
                    if find_len == 0:
                        find_len = 1
                    renamed_len = len(CI_renamed)
                    found = []
                    #get matching sections
                    index = 0
                    x = 0
                    while x < renamed_len:
                        try:
                            x = CI_renamed.index(CI_find,index,renamed_len)
                        except ValueError:
                            break
                        else:
                            index = x + find_len
                            found.append(renamed_name[x:index])

            #-- Positioning (starting from begining)
            elif position_find and not main_page.repl_end.GetValue():
                frm = main_page.repl_from.GetValue()
                to = frm + main_page.repl_to.GetValue()

            #-- Positioning (starting from end)
            elif position_find and main_page.repl_end.GetValue():
                frm = len(renamed_name) - 1 - main_page.repl_from.GetValue()
                if frm < 0: frm = 0
                to = frm + main_page.repl_to.GetValue()

            #-- replacement
            if main_page.repl_replace.GetValue():
                #- search and replace when field not blank
                if text_find and find:
                    parsedText = self.ParseInput(text,itemToRename)
                    #case insensitive
                    if not text_sensitive and found:
                        for match in found:
                            renamed_name = renamed_name.replace(match,parsedText)
                    #case sensitive
                    else:
                        renamed_name = renamed_name.replace(find, parsedText)
                #- replace everything if text field left blank
                elif text_find:
                    renamed_name = self.ParseInput(text,itemToRename)
                #- replace using regular expression
                elif regexp_find and REfind:
                    # need to first substiute, then parse for backreference support
                    try:
                        replaced = mod.sub(text, renamed_name)
                    except sre_constants.error, err:
                        self.setStatusMsg(_(u"Regular-Expression: %s")%err,u'warn')
                        # so we know not to change status text after RE error msg
                        REmsg = True
                        pass
                    else:
                        renamed_name = self.ParseInput(replaced,itemToRename)
                #- replace by position:
                elif position_find:
                    parsedText = self.ParseInput(text,itemToRename)
                    renamed_name = renamed_name[:frm] + parsedText + renamed_name[to:]

            #-- modification:
            elif main_page.repl_operation.GetValue():
                # do the modifications based on selected operations
                # regular expression
                if regexp_find and REfind:
                    renamed_name = mod.sub(commands[op], renamed_name)
                # normal
                elif text_find and find:
                    # case insensitive
                    if not text_sensitive and found:
                        for match in found:
                            renamed_name = renamed_name.replace(match, commands[op](find))
                    # case sensitive
                    else:
                        renamed_name = renamed_name.replace(find, commands[op](find))
                # positioning
                elif position_find:
                    renamed_name = renamed_name[:frm] + commands[op](renamed_name[frm:to]) + renamed_name[to:]
                # nothing set, default
                else:
                    renamed_name = commands[op](renamed_name)
            #-- move:
            else:
                # default to not finding anything
                moveMatch = ""
                # first find the original
                # regular expression
                if regexp_find and REfind:
                    try:
                        moveMatch = mod.findall(renamed_name)[0]
                    except (AttributeError, IndexError):
                        pass
                # normal:
                elif text_find and find:
                    # case insensitive
                    if not text_sensitive and found:
                        moveMatch = found[0]
                    # case sensitive:
                    elif find in renamed_name:
                        moveMatch = find
                # position
                elif position_find:
                    moveMatch = renamed_name[frm:to]

                # remove the original, saving a backup in case no match found
                old_name = renamed_name
                renamed_name = renamed_name.replace(moveMatch,"",1)

                # now find where to move to if not by position
                if not moveByPosition:
                    if moveTxt: # text has to contain something
                        # regular expression
                        if moveRE != False:
                            moveTxt = moveRE.findall(renamed_name)
                            # if match is found, get first item in list
                            if len(moveTxt) > 0:
                                moveTxt = moveTxt[0]
                            else:
                                moveTxt = ''

                        # get the index of match
                        try:
                            moveTo = renamed_name.index(moveTxt)
                        except (ValueError):
                            moveTo = u':Do_Not_Move:'
                            pass
                        else:
                            if moveMod == _(u"after"):
                                moveTo = moveTo + len(moveTxt)
                            elif moveMod != _(u"before"):
                                moveTo = moveMod
                    else:
                        moveTo = u':Do_Not_Move:'

                # finally recreate string
                if moveTo != u':Do_Not_Move:':
                    # position specified
                    if moveTo != moveMod and moveByPosition:
                        if moveTo == -1:
                            renamed_name = renamed_name + moveMatch
                        elif moveTo < -1:
                            renamed_name = renamed_name[:moveTo+1] + moveMatch + renamed_name[moveTo+1:]
                        else:
                            renamed_name = renamed_name[:moveTo] + moveMatch + renamed_name[moveTo:]
                    # text specified
                    else:
                        if moveTo == _(u"replace") and moveMatch:
                            renamed_name = renamed_name.replace(moveTxt,moveMatch,1)
                        elif moveMatch:
                            renamed_name = renamed_name[:moveTo] + moveMatch + renamed_name[moveTo:]
                    del old_name
                # no match found
                else:
                    renamed_name = old_name
            return renamed_name


        def insertion(renamed_name):
            parsedText = self.ParseInput(insertText,itemToRename)
            # insert at specified position
            if main_page.insert_position.GetValue():
                pos = main_page.insert_position_value.GetValue()
                if pos == -1:
                    renamed_name = renamed_name + parsedText
                elif pos < -1:
                    renamed_name = renamed_name[:pos+1] + parsedText + renamed_name[pos+1:]
                else:
                    renamed_name = renamed_name[:pos] + parsedText + renamed_name[pos:]
            # insert in between characters
            else:
                rep = main_page.insert_repetion_value.GetValue()
                temp_name = renamed_name
                renamed_name = ''
                i = 1
                for char in temp_name:
                    if rep == i:
                        renamed_name = renamed_name + char + parsedText
                        i = 1
                    else:
                        renamed_name = renamed_name + char
                        i += 1
            return renamed_name

        def modifyLength(renamed_name):
            return modifyOp(renamed_name)

        def prefix(renamed_name):
            parsedText = self.ParseInput(prefixText,itemToRename)
            renamed_name = parsedText + renamed_name
            return renamed_name

        def suffix(renamed_name):
            parsedText = self.ParseInput(suffixText,itemToRename)
            renamed_name = renamed_name + parsedText
            return renamed_name


        if not REmsg:
            self.setStatusMsg(_(u"Generating preview, please wait..."),u'wait')

        #-------------------------------------------#
        #    run trough each item to be renamed:    #
        #-------------------------------------------#
        for itemToRename, IsFile in self.items:
            self.Update()
            # lets start by clearing stuff out
            split_path = os.path.split(itemToRename)
            path = split_path[0]
            curDir = path
            name = split_path[1]
            splitName = os.path.splitext(name)
            # what to do with files
            if IsFile == True:
                # name only
                if not apply_to_name and apply_to_ext:
                    original_name = splitName[1]
                    renamed_name = splitName[0]
                # extension only
                elif apply_to_name and not apply_to_ext:
                    original_name = splitName[0]
                    renamed_name = splitName[1].replace('.','')
                # both
                elif apply_to_name and apply_to_ext:
                    renamed_name = name
            # what to do with directories
            else:
                renamed_name = name

            # doing what the user set
            #---- Modify length
            if main_pos[5]:
                renamed_name = modifyLength(renamed_name)

            #---- replacement/modification/move
            if main_pos[3]:
                renamed_name = searchReplaceModifyMove(renamed_name, moveTxt, moveTo)

            #---- prefix
            if main_pos[1]:
                renamed_name = prefix(renamed_name)

            #---- suffix
            if main_pos[2]:
                renamed_name = suffix(renamed_name)

            #---- insertion
            if main_pos[4]:
                renamed_name = insertion(renamed_name)


            # once everything is done reaseemble file and extension:
            if IsFile == True:
                # name only
                if not apply_to_name and apply_to_ext:
                    renamedItem = renamed_name + original_name
                # extension only
                elif apply_to_name and not apply_to_ext:
                    renamedItem = original_name + u'.' + renamed_name
                # both
                elif apply_to_name and apply_to_ext:
                    renamedItem = renamed_name

            # directories are simpler
            else:
                renamedItem = renamed_name

            #---- assemble directories
            for dir in dirMatch:
                parsedDir = self.ParseInput(dir,itemToRename)
                parsedDir = parsedDir.rstrip(u" ")
                if len(parsedDir) != 0:
                    # error check directories
                    parsedDir = self.errorCheck(parsedDir,path,path,items_ren)
                    # assemble new path
                    path = os.path.join(path,parsedDir)

            #--------- ERROR CHECKING: ---------#
            renamedItem = self.errorCheck(renamedItem,itemToRename,path,items_ren)

            # add to list of renamed items
            items_ren.append(unicode(os.path.join(path,renamedItem)))

            # increment item position counters
            self.ec += 1 #for error/warn assignment
            lastDir = curDir #for reseting numbering by directory

        #-------------------------------------------#
        #           ^ End of 'for' loop ^           #
        #-------------------------------------------#


        # make new dictionary with original and renamed files
        to_rename = zip(self.items,items_ren)
        del items_ren

        #---- display results
        self.displayResults()

        #---- show some messages and display problems in error tab
        #- good, no errors no warnings
        if len(bad) == 0 and len(warn) == 0:
            if not REmsg:
                self.setStatusMsg(_(u"Previewed %s items with no filename errors.") %len(to_rename),u'complete')
        #- problems
        else:
            self.notebook.GetPage(4).display_errors(errorLog,warn,bad,len(to_rename))
            #switch to error panel if set so in preferences:
            if self.prefs[u'autoShowError=']:
                self.notebook.SetSelection(4)

        #only enable 'GO' button if items have been changed, and w/o errors
        if len(bad) == 0:
            self.go.Enable(True)
            self.menuFile.GoMenu.Enable(True)
        else:
            self.go.Enable(False)
            self.menuFile.GoMenu.Enable(False)



#### DISPLAY RESULTS ###########################################################
    """
    Resets the main display then loads it up with items in to_rename,
    also setting colors as need be depending on item's status. Called from
    preview and undo.
    """
    def displayResults(self):
        self.display.DeleteAllItems()
        self.display.SetBackgroundColour(u'white')
        self.notebook.GetPage(4).clear_errors()
        self.notebook.SetPageText(4,_(u"Errors/Warnings: 0"))
        i = 0
        for original,renamed in to_rename:
                # self.Update() #causes linux problems
                split = os.path.split(original[0])
                base = split[0]
                renamed = renamed.replace(base, "")
                renamed = renamed.lstrip(os.path.sep)
                # renamed = os.path.split(renamed)[1]

                original = split[1]
                index = self.display.InsertStringItem(i, base)
                self.display.SetStringItem(index, 1, original ,0)
                self.display.SetStringItem(index, 2, renamed ,0)

                # make items that will be renamed stand out
                if original != renamed:
                    self.display.SetItemBackgroundColour(i,u'#E5FFE5')#light green

                # make bad names stand out:
                if i in self.bad:
                    self.display.SetItemBackgroundColour(i,u'#FF1616')#red
                elif i in self.warn:
                    self.display.SetItemBackgroundColour(i,u'#FDEB22')#yellow

                i += 1
        # show the last warning/error
        if self.warn != []:
            self.display.EnsureVisible(self.warn[-1])
        elif self.bad != []:
            self.display.EnsureVisible(self.bad[-1])
        # show currently selected item
        try:
            self.display.Select(self.currentItem, True)
        except (AttributeError,TypeError):
            pass
        else:
            self.display.EnsureVisible(self.currentItem)

        # auto resize column
        self.display.SetColumnWidth(2,-1)
        if self.display.GetColumnWidth(2) < 125:
            self.display.SetColumnWidth(2,125)


#### CHANGE ITEM POSITION IN LIST ##############################################
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def changeItemOrder(self, change):
        if self.currentItem != None:
            try:
                moveTo = self.currentItem + change
            except TypeError:
                if change == u'top':
                    moveTo = 0
                else:
                    moveTo = len(self.items)-1
                pass

            if moveTo > len(self.items):
                moveTo = len(self.items)-1
            if moveTo < 0:
                moveTo = 0

            old = self.items[self.currentItem]
            new = self.items[moveTo]

            del self.items[self.currentItem]
            self.items.insert(moveTo,old)

            self.currentItem = moveTo
            self.OnPreviewButton(0)



#### PRE-GENERATE PREVIEW ######################################################
    """
    This is a helping function to generatePreview(). Mainly checks
    various conditions to see if running the preview is appropriate.
    Also some setting of global variables.
    """
    def OnPreviewButton(self, event):
        wx.BeginBusyCursor()
        #--- general globals ---#
        global error # to see if an error has occured

        #--- numbering globals ---#
        global c #numbering counter
        global start #numbering start
        global numberStyle
        numberStyle = self.notebook.GetPage(2).GetNumberStyle()
        global number_params
        number_params = self.notebook.GetPage(2).GetNumberParams()

        #--- initial variables ---#
        blanks = [False, False, False, False]
        run = True #load items and run preview ?

        """
        First get some widget values to determine which operations will
        definitly yield an error due to blank info.
        """
        # List containing which operations to do
        main_page = self.notebook.GetPage(1)
        main_pos = main_page.GetReNamePosition()

        apply_to_ext = main_page.apply_to_ext.GetValue()
        apply_to_name = main_page.apply_to_name.GetValue()
        if not apply_to_ext and not apply_to_name:
            blanks[0] = True

        if main_pos[3]:
            text_find = main_page.repl_textButton.GetValue()
            replace = main_page.repl_replace.GetValue()
            text = main_page.repl_txt.GetValue()
            find = main_page.repl_find.GetValue()
            if (text_find and replace) and not find and not text:
                blanks[3] = True

        if self.items == u'config_load':
            run = False
        elif (blanks[3] and (True not in main_pos[:3] and True not in main_pos[4:])) or (blanks[0]):
            run = False
        """
        If blank checking is OK, then attempt to load items and
        run the actual previewing operation, passing some variables along.
        Split up this way because the items list can be rather large, no
        need to make it (see picker.py) if the preview will ultimatly
        not happen.
        """
        if run:
            # The items to rename
            self.items = self.notebook.GetPage(0).GetItems()
            # check to make sure we have items
            if self.items == []:
                # try to load items first, if doing so will get all
                # items in location
                if self.prefs[u'autoSelectAll='] and self.notebook.GetPage(0).select_none.IsEnabled():
                    self.notebook.GetPage(0).ShowPicker(0)
                    self.items = self.notebook.GetPage(0).GetItems()
                    #still no good?
                    if self.items == []:
                        self.go.Enable(False)
                        self.menuFile.GoMenu.Enable(False)
                        self.display.DeleteAllItems()
                else:
                    self.go.Enable(False)
                    self.menuFile.GoMenu.Enable(False)
                    self.display.DeleteAllItems()

            # checks completed, generate preview
            else:
                # set some initial variables for counting
                # set count by value or set by number of items
                if number_params[5]:
                    start = len(self.items)
                else:
                    start = number_params[0]

                # alpha auto pad start value correction
                if numberStyle[0] == u'alpha' and numberStyle[2]:
                    a = (len(self.items)+number_params[0])*number_params[1]
                    width = len(self.toAlpha(abs(a)))

                    if width == 1:
                        start = start
                    elif width == 2 and start < 27:
                        start = 26 + start
                    elif width == 3 and start < 703:
                        start = 702 + start
                    elif width == 4 and start < 18279:
                        start = 18278 + start

                c = 0 # item numbering counter
                self.generatePreview(main_page, main_pos, apply_to_ext, apply_to_name)
        else:
            self.go.Enable(False)
            self.menuFile.GoMenu.Enable(False)
            self.display.DeleteAllItems()

        # stuff to do after preview completes
        wx.EndBusyCursor()



##### RENAMING: ################################################################
    """
    Writes undo files first (safety first !), then attemps to perform
    the actual renaming operation. Will stop on errors.
    """
    def OnGoButton(self, event):
        error = False
        self.currentItem = None
        wx.BeginBusyCursor()
        self.notebook.GetPage(0).path.SetEditable(False)
        self.setStatusMsg(_(u"Renaming in progress, please wait ..."),u'wait')

        # save output to undo files
        try:
            originalFile = codecs.open(self.stdPath(u'undo/original.bak'),'w', "utf-8")
            renamedFile = codecs.open(self.stdPath(u'undo/renamed.bak'),'w', "utf-8")
        except IOError, (errno, strerror):
            dlg = wx.MessageDialog(self,
                strerror + _(u"\nMake sure 'undo' directory exists and is read/write\n\nYou will not be able to undo!!\nDo you want to continue??"),
                _(u"Problem with undo!"), wx.ICON_ERROR|wx.YES_NO)
            if dlg.ShowModal() == wx.ID_NO:
                error = 'bad_undo_files'
            dlg.Destroy()

        if not error:
            i = 0
            warn = ''
            # renaming operation
            for original, renamed in to_rename:
                self.Update()
                # dupe handling
                # windows makes no difference between case
                if platform.system() == 'Windows':
                    renamedCompare = renamed.lower()
                    originalCompare = original[0].lower()
                else:
                    renamedCompare = renamed
                    originalCompare = original[0]
                if warn != u'duplicate_name' and renamedCompare != originalCompare and os.path.exists(renamed):
                    self.display.SetItemBackgroundColour(i,u'#FF1616')
                    self.setStatusMsg(_(u"Duplicate name"),u'warn')
                    msg = _(u"This name already exists:\n%s")%renamed\
                        +_(u"\n\nI can make a sub-folder called 't_e_m_p' and attempt\nto do the renaming operation there. You can then move everything back.\nThis will take longer, and may not always work.\n\nGo ahead and try this??")
                    dlg = wx.MessageDialog(self, msg,_(u"Duplicate name"),
                        wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
                    if dlg.ShowModal() == wx.ID_YES:
                        warn = u'duplicate_name'
                    else:
                        error = True
                        break
                    dlg.Destroy()

                # set correct path if in dupe error mode
                if warn == u'duplicate_name':
                    path = self.notebook.GetPage(0).path.GetValue()
                    if not path.endswith(os.path.sep):
                        path = path+os.path.sep
                    renamed = renamed.replace(path,u'')
                    renamed = os.path.join(path, u't_e_m_p', renamed)

                # write name to undo
                originalFile.write(original[0] + u'\n')
                renamedFile.write(renamed + u'\n')

                try:
                    os.renames(original[0], renamed)
                except OSError, (errno, strerror):
                    strerror = strerror.decode(sys.getfilesystemencoding())
                    self.display.SetItemBackgroundColour(i,u'#FF1616')
                    self.setStatusMsg(strerror, u'failed')
                    self.makeErrMsg(_(u"There was an error renaming:\n\n%s")%original[0] +\
                        _(u"\n\nto:\n\n%s\n\nReason: %s")%(renamed,strerror), _(u"Bad !!"))
                    error = True
                    break
                self.display.SetItemBackgroundColour(i,u'#97F27F')#green
                self.display.EnsureVisible(i)
                i += 1

        # end of operations
        if not error:
            self.setStatusMsg(_(u"Renaming for %s items completed.")%len(to_rename),u"complete")
            if self.prefs['reloadAfterRename='] and event != u'doNotReload':
                self.notebook.GetPage(0).ShowPicker(event)
            else:
                self.notebook.GetPage(0).clearALL()

        elif error == u'bad_undo_files':
            self.setStatusMsg(_(u"Renaming cancelled."),u'failed')

        wx.EndBusyCursor()

        # refresh dir tree
        if self.prefs[u'useDirTree=']:
            dirPicker = self.notebook.GetPage(0).dirPicker
            itemId = dirPicker.GetTreeCtrl().GetSelection()
            dirPicker.GetTreeCtrl().CollapseAndReset(itemId)
            dirPicker.GetTreeCtrl().Expand(itemId)

        self.go.Enable(False)
        self.menuFile.GoMenu.Enable(False)
        self.notebook.GetPage(0).path.SetEditable(True)
