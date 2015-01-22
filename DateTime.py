# -*- coding: utf-8 -*-

# This is the date and time panel in the main
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
import wx.lib.masked.timectrl
import wx.calendar
import time
import codecs
import sys

[wxID_PANEL, wxID_PANELCAL, wxID_PANELDATESEPERATOR,
 wxID_PANELDATETESTDISPLAY, wxID_PANELDATEFORMAT,
 wxID_PANELFORMATHELP, wxID_PANELGETFROMITEM,
 wxID_PANELITEMTIMETYPE, wxID_PANELSETTIMENOW,
 wxID_PANELSPIN1, wxID_PANELSTATICBOX1,
 wxID_PANELSTATICBOX2, wxID_PANELSTATICLINE1,
 wxID_PANELSTATICTEXT1, wxID_PANELSTATICTEXT2,
 wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT4,
 wxID_PANELSTATICTEXT5, wxID_PANELSTATICTEXT6,
 wxID_PANELSTATICTEXT7, wxID_PANELTIME,
 wxID_PANELTIMESEPERATOR, wxID_PANELTIMETESTDISPLAY,
 wxID_PANELTIME_FORMAT,
] = [wx.NewId() for _init_ctrls in range(24)]

class Panel(wx.Panel):
    def sizer(self):
        topRow = wx.BoxSizer(wx.HORIZONTAL)
        topRowElements = [((40,-1),0),
                          (self.getFromItem,5),
                          (self.itemTimeType,5),
                          (self.staticText7,30)]
        if main.langLTR:
            for i in topRowElements:
                topRow.Add(i[0],0,wx.RIGHT|wx.ALIGN_CENTER,i[1])
        else:
            topRowElements.reverse()
            topRow.Add((-1,-1),1)
            for i in topRowElements:
                topRow.Add(i[0],0,wx.LEFT|wx.ALIGN_CENTER,i[1])

        dateStuff = wx.GridBagSizer(0, 0)
        dateStuff.Add(self.cal, (0,0), (3,1), border=10, flag=wx.RIGHT)
        dateStuff.Add(self.staticText2, (0,1), border=3,
            flag=wx.ALIGN_BOTTOM|wx.BOTTOM|main.alignment)
        dateStuff.Add(self.dateFormat, (1,1), (1,3), wx.ALIGN_TOP)
        dateStuff.Add(self.staticText4, (2,1), flag=wx.ALIGN_CENTER_VERTICAL)
        dateStuff.Add(self.dateSeperator, (2,2), border=5,
            flag=main.alignment|wx.ALIGN_CENTER_VERTICAL|wx.LEFT)

        dateBox = wx.StaticBoxSizer(self.staticBox1,
         wx.HORIZONTAL)
        dateBox.Add(dateStuff,0,wx.LEFT|wx.BOTTOM|wx.TOP,3)

        timeStuff = self.timeStuff = wx.GridBagSizer(0, 0)
        timeStuff.Add(self.time, (0,0), border=10, flag=wx.LEFT|wx.ALIGN_CENTER)
        timeStuff.Add(self.spin1, (0,1), flag=wx.ALIGN_CENTER_VERTICAL)
        timeStuff.Add(self.setTimeNow, (0,2), (1,2), border=5,
            flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL)
        timeStuff.Add(self.staticText1, (2,0), border=10,
            flag=wx.LEFT|wx.ALIGN_BOTTOM|main.alignment)
        timeStuff.Add(self.timeFormat, (3,0), (1,4), border=10, flag=wx.LEFT)
        timeStuff.Add(self.staticText3, (5,0), border=10,
            flag=wx.LEFT|wx.ALIGN_CENTER)
        timeStuff.Add(self.timeSeperator, (5,1), (1,4))

        timeBox = wx.StaticBoxSizer(self.staticBox2,
         wx.HORIZONTAL)
        timeBox.Add(timeStuff,0,wx.BOTTOM|wx.TOP,3)

        midSection = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            midSection.Add(dateBox,0)
            midSection.Add(timeBox,0,wx.LEFT,10)
        else:
            midSection.Add((-1,-1),1)
            midSection.Add(timeBox,0,wx.RIGHT,10)
            midSection.Add(dateBox,0,wx.RIGHT,10)

        bottomRow = wx.BoxSizer(wx.HORIZONTAL)
        bottomRowElements = [((20,-1),0,0),
                             (self.staticText5,0,5),
                             (self.dateTestDisplay,1,20),
                             (self.staticLine1,0,20),
                             (self.staticText6,0,5),
                             (self.timeTestDisplay,1,20)]
        if main.langLTR:
            for i in bottomRowElements:
                bottomRow.Add(i[0],i[1],wx.RIGHT|wx.ALIGN_CENTER,i[2])
        else:
            bottomRowElements.reverse()
            for i in bottomRowElements:
                bottomRow.Add(i[0],i[1],wx.LEFT|wx.ALIGN_CENTER,i[2])

        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topRow,0,wx.TOP|wx.BOTTOM|wx.EXPAND,15)
        mainSizer.Add(midSection,0,wx.LEFT|wx.TOP|wx.EXPAND,7)
        mainSizer.Add(bottomRow,0,wx.EXPAND|wx.TOP,25)

        self.SetSizerAndFit(mainSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'DateTimePanel',
              parent=prnt, style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
              label=_(u"Date Settings:"), name=u'staticBox1', parent=self,
              style=main.alignment)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELSTATICBOX2,
              label=_(u"Time Settings:"), name=u'staticBox2', parent=self,
              style=main.alignment)

        self.cal = wx.calendar.CalendarCtrl(date=wx.DateTime.Now(),
              id=wxID_PANELCAL, name=u'cal', parent=self,
              style=wx.calendar.CAL_SHOW_SURROUNDING_WEEKS  | wx.calendar.CAL_MONDAY_FIRST | wx.calendar.CAL_SHOW_HOLIDAYS)
        self.cal.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.TestDate,
              id=wxID_PANELCAL)

        self.dateFormat = wx.ComboBox(choices=[_(u"MM-DD-YYYY"),
              _(u"MM-DD-YY"), _(u"DD-MM-YYYY"), _(u"DD-MM-YY"),
              _(u"YYYY-MM-DD"), _(u"Month DD, YYYY"), _(u"Day, Month DD, YYYY"),
              _(u"YY"), _(u"YYYY")], id=wxID_PANELDATEFORMAT,
              name=u'dateFormat', parent=self, pos=wx.Point(220, 88),
              style=0, value='')
        self.dateFormat.SetMinSize(wx.Size(165,-1))
        self.dateFormat.SetSelection(0)
        self.dateFormat.SetToolTipString(_(u"Use menu or enter text"))
        self.dateFormat.Bind(wx.EVT_TEXT, self.TestDate,
              id=wxID_PANELDATEFORMAT)

        self.timeFormat = wx.ComboBox(choices=[_(u"HH.MM"), _(u"24HH.MM"),
              _(u"HH.MM.SS"), _(u"24HH.MM.SS")],
              id=wxID_PANELTIME_FORMAT, name=u'timeFormat',
              parent=self, pos=wx.Point(432, 128), style=0)
        self.timeFormat.SetMinSize(wx.Size(140,-1))
        self.timeFormat.SetSelection(2)
        self.timeFormat.SetToolTipString(_(u"Use menu or enter text"))
        self.timeFormat.Bind(wx.EVT_TEXT, self.TestTime,
              id=wxID_PANELTIME_FORMAT)

        self.dateTestDisplay = wx.StaticText(id=wxID_PANELDATETESTDISPLAY,
              name=u'dateTestDisplay', parent=self, pos=wx.Point(112, 224),
              size=wx.Size(176, -1), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
              label=_(u"Formatting:"), name=u'staticText1', parent=self,
              pos=wx.Point(424, 112), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
              label=_(u"Formatting:"), name=u'staticText2', parent=self,
              pos=wx.Point(216, 72), style=0)

        self.timeTestDisplay = wx.StaticText(id=wxID_PANELTIMETESTDISPLAY,
              name=u'timeTestDisplay', parent=self)

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
              label=_(u"Separator:"), name=u'staticText3', parent=self,
              pos=wx.Point(448, 184), style=0)

        self.dateSeperator = wx.TextCtrl(id=wxID_PANELDATESEPERATOR,
              name=u'dateSeperator', parent=self, pos=wx.Point(280, 128),
              size=wx.Size(24, -1), style=0, value='-')
        self.dateSeperator.SetMaxLength(1)
        self.dateSeperator.Bind(wx.EVT_TEXT, self.TestDate,
              id=wxID_PANELDATESEPERATOR)

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
              label=_(u"Separator:"), name=u'staticText4', parent=self,
              pos=wx.Point(224, 128), style=0)

        self.timeSeperator = wx.TextCtrl(id=wxID_PANELTIMESEPERATOR,
              name=u'timeSeperator', parent=self, pos=wx.Point(512, 184),
              size=wx.Size(24, -1), style=0, value="'")
        self.timeSeperator.SetMaxLength(1)
        self.timeSeperator.Bind(wx.EVT_TEXT, self.TestTime,
              id=wxID_PANELTIMESEPERATOR)

        self.spin1 = wx.SpinButton(id=wxID_PANELSPIN1, name=u'spin1',
              parent=self, pos=wx.Point(512, 72), style=wx.SP_VERTICAL)
        self.spin1.SetToolTipString(_(u"Adjust Time"))
        self.spin1.Bind(wx.EVT_SPIN, self.TestTime, id=wxID_PANELSPIN1)

        self.time = wx.lib.masked.timectrl.TimeCtrl(display_seconds=True,
              fmt24hr=False, id=wxID_PANELTIME, name=u'time',
              oob_color=wx.NamedColour(u'Yellow'), parent=self, pos=wx.Point(424,
              72), spinButton=self.spin1, style=wx.TE_PROCESS_TAB,
              useFixedWidthFont=True, value=wx.DateTime.Now())

        self.setTimeNow = wx.Button(id=wxID_PANELSETTIMENOW,
              label=_(u"Set to now"), name=u'setTimeNow', parent=self,
              pos=wx.Point(552, 72), style=0)
        self.setTimeNow.Bind(wx.EVT_BUTTON, self.OnSetTimeNowButton,
              id=wxID_PANELSETTIMENOW)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
              label=_(u"Date Preview:"), name=u'staticText5', parent=self,
              pos=wx.Point(16, 232), style=0)
        self.staticText5.SetFont(wx.Font(main.fontParams['size'], wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.staticText6 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
              label=_(u"Time Preview:"), name=u'staticText6', parent=self,
              pos=wx.Point(352, 224), style=0)
        self.staticText6.SetFont(wx.Font(main.fontParams['size'], wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.staticLine1 = wx.StaticLine(id=wxID_PANELSTATICLINE1,
              name=u'staticLine1', parent=self, pos=wx.Point(336, 227),
              size=wx.Size(2, 18), style=0)

        self.getFromItem = wx.CheckBox(id=wxID_PANELGETFROMITEM,
              label=_(u"Use the item's"), name=u'getFromItem', parent=self,
              pos=wx.Point(288, 16), style=0)
        self.getFromItem.SetValue(False)
        self.getFromItem.Bind(wx.EVT_CHECKBOX, self.GetFromItemCheckbox,
              id=wxID_PANELGETFROMITEM)

        self.itemTimeType = wx.Choice(choices=[self.ctime,
              _(u"last modification"), _(u"last access"), _(u"image EXIF tag")],
              id=wxID_PANELITEMTIMETYPE, name=u'itemTimeType',
              parent=self, pos=wx.Point(392, 16), style=0)
        self.itemTimeType.SetSelection(0)
        self.itemTimeType.Enable(False)
        self.itemTimeType.Bind(wx.EVT_CHOICE, main.showPreview,
              id=wxID_PANELITEMTIMETYPE)

        self.staticText7 = wx.StaticText(id=wxID_PANELSTATICTEXT7,
              label=_(u"time."), name='staticText7', parent=self, pos=wx.Point(536,
              24), style=0)
        self.staticText7.Enable(False)

    def __init__(self, parent, main_window):
        global main
        main = main_window

        if sys.platform == u'win32':
            self.ctime = _(u"creation")
        else:
            self.ctime = _(u"metadata change")

        self._init_ctrls(parent)
        self.sizer()
        self.TestDate(0)
        self.TestTime(0)


    # enables/disables based on wether to get from item or not
    def GetFromItemCheckbox(self, event):
        enabled = (self.itemTimeType, self.staticText7)
        disabled = (self.cal, self.spin1, self.time, self.setTimeNow)
        if self.getFromItem.GetValue():
            for widget in enabled:
                widget.Enable(True)
            for widget in disabled:
                widget.Enable(False)
        else:
            for widget in enabled:
                widget.Enable(False)
            for widget in disabled:
                widget.Enable(True)
        self.TestTime(event)
        self.TestDate(event)

    def GetDateTime(self, event):
        """
        get date/time, format according to user input,
        and return values. Called from 'main' module as well
        as from within this class.
        """
        self.dateTime = [False,False,False] # 0=get from?, 1=date, 2=time

        # get date/time from item or set by user
        if self.getFromItem.GetValue():
            self.dateTime[0] = True

        #-------- DATE --------#
        #translate from human to python readable:
        sep = self.dateSeperator.GetValue()
        date_lookup = {
            _(u"MM-DD-YYYY") : u'%m'+sep+u'%d'+sep+u'%Y',
            _(u"MM-DD-YY") : u'%m'+sep+u'%d'+sep+u'%y',
            _(u"DD-MM-YYYY") : u'%d'+sep+u'%m'+sep+u'%Y',
            _(u"DD-MM-YY") : u'%d'+sep+u'%m'+sep+u'%y',
            _(u"YYYY-MM-DD") : u'%Y'+sep+u'%m'+sep+u'%d',
            _(u"Month DD, YYYY") : u'%B %d, %Y',
            _(u"Day, Month DD, YYYY") : u'%A, %B %d, %Y',
            _(u"YY") : u'%y',
            _(u"YYYY") : u'%Y',
            }
        if event and event.GetId() == wxID_PANELDATEFORMAT:
            dateFormat = event.GetString()
        else:
            dateFormat = self.dateFormat.GetValue()

        # get the format
        try:
            date_form = date_lookup[dateFormat]
        except KeyError:
            date_form = dateFormat

        # get date from item or set by user
        if self.dateTime[0]:
            self.dateTime[1] = date_form
        elif date_form:
            date = self.cal.GetDate().Format(date_form)
            self.dateTime[1] = date


        #-------- TIME --------#
        #translate from human to python readable:
        sep = self.timeSeperator.GetValue()
        time_lookup = {
            _(u"HH.MM") : u'%I'+sep+u'%M %p',
            _(u"24HH.MM") : u'%H'+sep+u'%M',
            _(u"HH.MM.SS") : u'%I'+sep+u'%M'+sep+u'%S %p',
            _(u"24HH.MM.SS") : u'%H'+sep+u'%M'+sep+u'%S'
            }

        if event and event.GetId() == wxID_PANELTIME_FORMAT:
            timeFormat = event.GetString()
        else:
            timeFormat = self.timeFormat.GetValue()

        # get the format
        try:
            time_form = time_lookup[timeFormat]
        except KeyError:
            time_form = timeFormat

        # get time from item or set by user
        if self.dateTime[0]:
            self.dateTime[2] = time_form
        else:
            time = self.time.GetWxDateTime()
            try:
                time = time.Format(time_form)
            except:
                time = ''
                pass
            self.dateTime[2] = time
    #------------------------------------------------#


    def TestDate(self, event):
        #displays date according to current settings:
        self.GetDateTime(event)
        if self.dateTime[1]:
            self.dateTestDisplay.SetLabel(self.dateTime[1])
            main.showPreview(event)

    def TestTime(self, event):
        #displays time according to current settings:
        self.GetDateTime(event)
        if self.dateTime[2]:
            self.timeTestDisplay.SetLabel(self.dateTime[2])
            main.showPreview(event)

    def OnSetTimeNowButton(self, event):
        self.time.SetValue(wx.DateTime.Now())
        self.TestTime(event)


###### GET/SET CONFIGURATION SETTINGS: #########################################
    def getSettings(self):
        settings = (u"<[dateTime]>",
          u"dateFormat>:>%s" %self.dateFormat.GetValue(),
          u"dateSeperator>:>%s" %self.dateSeperator.GetValue(),
          u"timeFormat>:>%s" %self.timeFormat.GetValue(),
          u"timeSeperator>:>%s" %self.timeSeperator.GetValue(),
          u"getFromItem>:>%s" %int(self.getFromItem.GetValue()),
          u"itemTimeType>:>%s" %self.itemTimeType.GetSelection(),
          )
        return settings


    def setSettings(self,settings):
        if len(settings) == 6: #make sure number of settings is correct
            try:
                self.dateFormat.SetValue(settings[0])
                self.dateSeperator.SetValue(settings[1])
                self.timeFormat.SetValue(settings[2])
                self.timeSeperator.SetValue(settings[3])
                self.getFromItem.SetValue(int(settings[4])),
                self.itemTimeType.SetSelection(int(settings[5].replace('\n','')))
            except ValueError:
                return False
            else:
                # apply the settings:
                self.GetFromItemCheckbox(0)
                return True
        else:
            return False


