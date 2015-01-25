# -*- coding: utf-8 -*-
#Boa:FramePanel:numberingPanel

# This is the numbering panel that goes into
# the main application's notebook.

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

[wxID_NUMBERINGPANEL, wxID_NUMBERINGPANELALPHA, wxID_NUMBERINGPANELALPHA_PAD,
 wxID_NUMBERINGPANELALPHA_UC, wxID_NUMBERINGPANELASC,
 wxID_NUMBERINGPANELCOUNT, wxID_NUMBERINGPANELCOUNTBYDIR,
 wxID_NUMBERINGPANELDESC, wxID_NUMBERINGPANELDIGIT,
 wxID_NUMBERINGPANELDIGIT_AUTOPAD, wxID_NUMBERINGPANELDIGIT_PAD,
 wxID_NUMBERINGPANELDIGIT_SETPAD, wxID_NUMBERINGPANELDOWNBOTTOM,
 wxID_NUMBERINGPANELDOWNBUTTON, wxID_NUMBERINGPANELDOWNMORE,
 wxID_NUMBERINGPANELORDER, wxID_NUMBERINGPANELPAD_CHAR,
 wxID_NUMBERINGPANELPAD_WIDTH, wxID_NUMBERINGPANELRESET,
 wxID_NUMBERINGPANELRESETDIR, wxID_NUMBERINGPANELROMAN,
 wxID_NUMBERINGPANELROMAN_UC, wxID_NUMBERINGPANELSORTING,
 wxID_NUMBERINGPANELSORT_TEXT, wxID_NUMBERINGPANELSTART,
 wxID_NUMBERINGPANELSTARTBYITEMS, wxID_NUMBERINGPANELSTATICTEXT1,
 wxID_NUMBERINGPANELSTATICTEXT2, wxID_NUMBERINGPANELSTATICTEXT5,
 wxID_NUMBERINGPANELSTATICTEXT6, wxID_NUMBERINGPANELSTATICTEXT7,
 wxID_NUMBERINGPANELSTEP, wxID_NUMBERINGPANELSTYLE,
 wxID_NUMBERINGPANELUPBUTTON, wxID_NUMBERINGPANELUPMORE,
 wxID_NUMBERINGPANELUPTOP, wxID_NUMBERINGPANELSTARTBYITEM
] = [wx.NewId() for _init_ctrls in range(37)]

class numberingPanel(wx.Panel):

    def sizer(self):
        #>> start style box:
        sLine1 = wx.BoxSizer(wx.HORIZONTAL)
        line1elements = [(self.digit,10),
                         (self.digit_pad,0),
                         (self.pad_char,5)]
        if main.langLTR:
            for i in line1elements:
                sLine1.Add(i[0],0,wx.ALIGN_CENTER|wx.RIGHT,i[1])
        else:
            line1elements.reverse()
            for i in line1elements:
                sLine1.Add(i[0],0,wx.ALIGN_CENTER|wx.LEFT,i[1])
            sLine1.Add((5,-1),0)

        sLine3 = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            sLine3.Add(self.digit_setpad,0,wx.ALIGN_CENTER)
            sLine3.Add(self.pad_width,0)
        else:
            sLine3.Add(self.pad_width,0)
            sLine3.Add(self.digit_setpad,0,wx.ALIGN_CENTER)

        sLine4 = wx.BoxSizer(wx.HORIZONTAL)
        line4elements = [(self.alpha,10),
                         (self.alpha_uc,5),
                         (self.alpha_pad,10),]
        if main.langLTR:
            for i in line4elements:
                sLine4.Add(i[0],0,wx.ALIGN_CENTER|wx.RIGHT,i[1])
        else:
            line4elements.reverse()
            for i in line4elements:
                sLine4.Add(i[0],0,wx.ALIGN_CENTER|wx.LEFT,i[1])
            sLine4.Add((5,-1),0)

        sLine5 = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            sLine5.Add(self.roman,0,wx.RIGHT,10)
            sLine5.Add(self.roman_uc,0)
        else:
            sLine5.Add(self.roman_uc,0,wx.RIGHT,10)
            sLine5.Add(self.roman,0,wx.RIGHT,5)

        styleSizer = wx.StaticBoxSizer(self.style, wx.VERTICAL)
        styleSizer.Add(sLine1,0,wx.TOP|wx.BOTTOM|main.alignment,7)
        styleSizer.Add(self.digit_autopad,0,wx.LEFT|wx.RIGHT|main.alignment,20)
        styleSizer.Add((1,7))
        styleSizer.Add(sLine3,0,wx.LEFT|wx.RIGHT|main.alignment,20)
        styleSizer.Add(sLine4,0,wx.BOTTOM|wx.TOP|main.alignment,25)
        styleSizer.Add(sLine5,0,wx.BOTTOM|main.alignment,10)
        #<< end style box

        #>> start order box:
        oLine1 = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            oLine1.Add(self.sort_text,0,wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,5)
            oLine1.Add(self.sorting,0,wx.ALIGN_CENTER)
        else:
            oLine1.Add((-1,-1),1)
            oLine1.Add(self.sorting,0,wx.ALIGN_CENTER)
            oLine1.Add(self.sort_text,0,wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,5)

        oLine2 = wx.BoxSizer(wx.HORIZONTAL)
        oLine2elements = [((5,-1),0),
                         (self.staticText2,5),
                         (self.upButton,2),
                         (self.downButton,0),
                         ((5,-1),0),
                         (self.upMore,2),
                         (self.downMore,0),
                         ((5,-1),0),
                         (self.upTop,2),
                         (self.downBottom,0),
                         ((5,-1),0)]
        if main.langLTR:
            for i in oLine2elements:
                oLine2.Add(i[0],0,wx.ALIGN_CENTER|wx.RIGHT,i[1])
        else:
            oLine2elements.reverse()
            for i in oLine2elements:
                oLine2.Add(i[0],0,wx.ALIGN_CENTER|wx.LEFT,i[1])

        orderSizer = self.orderSizer = wx.StaticBoxSizer(self.order, wx.VERTICAL)
        orderSizer.Add((-1,3),0)
        orderSizer.Add(oLine1,0,wx.BOTTOM|wx.EXPAND,10)
        orderSizer.Add(oLine2,0,wx.BOTTOM,4)
        #<< end order box

        #>> start count box:

        countDir = wx.BoxSizer(wx.HORIZONTAL)
        countDir.Add(self.asc,3)
        countDir.Add((-1,-1),1)
        countDir.Add(self.desc,3)

        countSizer = wx.FlexGridSizer(cols=2, vgap=3, hgap=5)
        countElements = [[self.staticText5,
                          self.start],
                         [(-1,-1),
                          self.startByItems],
                         [(-1,5),(-1,5)],
                         [self.staticText6,
                          countDir],
                         [(-1,5),(-1,5)],
                         [self.staticText7,
                          self.step],
                         [(-1,-1),
                          self.countByDir],
                         [(-1,15),(-1,15)],
                         [self.staticText1,
                          self.reset],
                         [(-1,-1),
                          self.resetDir],
                        ]
        for row in countElements:
            if not main.langLTR:
                row.reverse()
            for i in row:
                countSizer.Add(i,0,wx.EXPAND|main.alignment)

        countBoxSizer = wx.StaticBoxSizer(self.count, wx.VERTICAL)
        countBoxSizer.Add(countSizer,0,wx.ALL,7)
        #<< end count box

        # main sizer and finish:
        mainSizer = self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = self.leftSizer = wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(styleSizer,0,wx.EXPAND)
        leftSizer.Add(orderSizer,0,wx.EXPAND|wx.TOP,10)

        mainElements = [((10,-1),0),
                        (leftSizer,7),
                        ((25,-1),0),
                        (countBoxSizer,30)]
        if main.langLTR:
            for i in mainElements:
                mainSizer.Add(i[0],0,wx.TOP,i[1])
        else:
            mainElements.reverse()
            mainSizer.Add((-1,-1),1)
            for i in mainElements:
                mainSizer.Add(i[0],0,wx.TOP,i[1])
        self.SetSizerAndFit(mainSizer)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_NUMBERINGPANEL, name=u'numberingPanel',
              parent=prnt, pos=wx.Point(346, 305), size=wx.Size(642, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(634, 328))

        self.count = wx.StaticBox(id=wxID_NUMBERINGPANELCOUNT,
              label=_(u"Counter:"), name=u'count', parent=self,
              pos=wx.Point(328, 16), style=main.alignment)

        self.order = wx.StaticBox(id=wxID_NUMBERINGPANELORDER, label=_(u"Item Sorting:"),
              name=u'order', parent=self, pos=wx.Point(16, 208),
              size=wx.Size(280, 88), style=main.alignment)

        self.style = wx.StaticBox(id=wxID_NUMBERINGPANELSTYLE,
              label=_(u"Style:"), name=u'style', parent=self, pos=wx.Point(16,
              16), style=main.alignment)

        self.digit = wx.RadioButton(id=wxID_NUMBERINGPANELDIGIT,
              label=_(u"Numerical:"), name=u'digit', parent=self,
              pos=wx.Point(32, 48), style=wx.RB_GROUP)
        self.digit.SetValue(True)
        self.digit.Bind(wx.EVT_RADIOBUTTON, self.check_styles,
              id=wxID_NUMBERINGPANELDIGIT)

        self.alpha = wx.RadioButton(id=wxID_NUMBERINGPANELALPHA,
              label=_(u"Alphabetical:"), name=u'alpha', parent=self,
              pos=wx.Point(32, 112), style=0)
        self.alpha.SetValue(False)
        self.alpha.Enable(True)
        self.alpha.SetToolTipString(_(u"Must start at positive value: (1=a, 28=ab, etc..)"))
        self.alpha.Bind(wx.EVT_RADIOBUTTON, self.check_styles)

        self.roman = wx.RadioButton(id=wxID_NUMBERINGPANELROMAN,
              label=_(u"Roman Numeral:"), name=u'roman', parent=self,
              pos=wx.Point(32, 144), style=0)
        self.roman.SetValue(False)
        self.roman.SetToolTipString(_(u"Count values must be between 1 and 4999"))
        self.roman.Bind(wx.EVT_RADIOBUTTON, self.check_styles)

        self.digit_pad = wx.CheckBox(id=wxID_NUMBERINGPANELDIGIT_PAD,
              label=_(u"Pad, using:"), name=u'digit_pad', parent=self,
              pos=wx.Point(112, 48), style=0)
        self.digit_pad.SetValue(True)
        self.digit_pad.Bind(wx.EVT_CHECKBOX, self.check_styles)

        self.pad_char = wx.TextCtrl(id=wxID_NUMBERINGPANELPAD_CHAR,
              name=u'pad_char', parent=self, pos=wx.Point(185, 47),
              size=wx.Size(24, -1), style=0, value='0')
        self.pad_char.SetMaxLength(1)
        self.pad_char.Bind(wx.EVT_TEXT, main.showPreview)

        self.alpha_pad = wx.CheckBox(id=wxID_NUMBERINGPANELALPHA_PAD,
              label=_(u"auto pad"), name=u'alpha_pad', parent=self,
              pos=wx.Point(216, 112), style=0)
        self.alpha_pad.SetValue(True)
        self.alpha_pad.Enable(False)
        self.alpha_pad.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.pad_width = wx.SpinCtrl(id=wxID_NUMBERINGPANELPAD_WIDTH, initial=3,
              max=255, min=1, name=u'pad_width', parent=self, pos=wx.Point(161,
              82), size=wx.Size(55, -1), style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.pad_width.SetValue(3)
        self.pad_width.SetRange(1, 255)
        self.pad_width.Bind(wx.EVT_TEXT_ENTER, self.OnPad_widthSpinctrl)
        self.pad_width.Bind(wx.EVT_SPINCTRL, self.OnPad_widthSpinctrl)

        self.roman_uc = wx.CheckBox(id=wxID_NUMBERINGPANELROMAN_UC,
              label=_(u"Uppercase"), name=u'roman_uc', parent=self,
              pos=wx.Point(152, 144), style=0)
        self.roman_uc.SetValue(True)
        self.roman_uc.Enable(False)
        self.roman_uc.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.sort_text = wx.StaticText(id=wxID_NUMBERINGPANELSORT_TEXT,
              label=_(u"Sort all items:"), name=u'sort_text', parent=self,
              pos=wx.Point(24, 232), style=0)

        self.staticText2 = wx.StaticText(id=wxID_NUMBERINGPANELSTATICTEXT2,
              label=_(u"Manually adjust item:"), name=u'staticText2', parent=self,
              pos=wx.Point(24, 264), style=0)

        self.downButton = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/down.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELDOWNBUTTON,
              name=u'downButton', parent=self, pos=wx.Point(152, 256), style=wx.BU_AUTODRAW)
        self.downButton.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELDOWNBUTTON)

        self.upButton = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/up.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELUPBUTTON,
              name=u'upButton', parent=self, pos=wx.Point(128, 256), style=wx.BU_AUTODRAW)
        self.upButton.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELUPBUTTON)

        self.upTop = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/upAll.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELUPTOP, name=u'upTop',
              parent=self, pos=wx.Point(240, 256), style=wx.BU_AUTODRAW)
        self.upTop.SetToolTipString(_(u"move to top"))
        self.upTop.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELUPTOP)

        self.downBottom = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/downAll.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELDOWNBOTTOM,
              name=u'downBottom', parent=self, pos=wx.Point(264, 256), style=wx.BU_AUTODRAW)
        self.downBottom.SetToolTipString(_(u"move to bottom"))
        self.downBottom.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELDOWNBOTTOM)

        self.upMore = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/up5.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELUPMORE, name=u'upMore',
              parent=self, pos=wx.Point(184, 256), style=wx.BU_AUTODRAW)
        self.upMore.SetToolTipString(_(u"move by 5"))
        self.upMore.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELUPMORE)

        self.downMore = wx.BitmapButton(bitmap=wx.Bitmap(main.realPath(u'icons/down5.png'),
              wx.BITMAP_TYPE_PNG), id=wxID_NUMBERINGPANELDOWNMORE,
              name=u'downMore', parent=self, pos=wx.Point(208, 256), style=wx.BU_AUTODRAW)
        self.downMore.SetToolTipString(_(u"move by 5"))
        self.downMore.Bind(wx.EVT_BUTTON, self.changeItemOrder,
              id=wxID_NUMBERINGPANELDOWNMORE)

        self.sorting = wx.Choice(choices=[ _(u"Ascending"), _(u"Descending"),
              _(u"Manually")], id=wxID_NUMBERINGPANELSORTING, name=u'sorting',
              parent=self, pos=wx.Point(160, 224), style=0)
        self.sorting.SetSelection(0)
        self.sorting.Bind(wx.EVT_CHOICE, self.setSortingOptions,
              id=wxID_NUMBERINGPANELSORTING)

        self.staticText5 = wx.StaticText(id=wxID_NUMBERINGPANELSTATICTEXT5,
              label=_(u"Start at:"), name=u'staticText5', parent=self,
              pos=wx.Point(352, 43), style=0)

        self.step = wx.SpinCtrl(id=wxID_NUMBERINGPANELSTEP, initial=1,
              max=10000000, min=1, name=u'step', parent=self, pos=wx.Point(416,
              136), size=wx.Size(168, -1), style=wx.SP_ARROW_KEYS)
        self.step.SetValue(1)
        self.step.SetToolTipString(_(u"A.K.A. step size"))
        self.step.Bind(wx.EVT_TEXT_ENTER, main.showPreview)
        self.step.Bind(wx.EVT_SPINCTRL, main.showPreview)

        self.staticText7 = wx.StaticText(id=wxID_NUMBERINGPANELSTATICTEXT7,
              label=_(u"Count by:"), name=u'staticText7', parent=self,
              pos=wx.Point(344, 142), style=0)

        self.asc = wx.RadioButton(id=wxID_NUMBERINGPANELASC, label=_(u"+"),
              name=u'asc', parent=self, pos=wx.Point(504, 104),
              style=wx.RB_GROUP)
        self.asc.SetFont(wx.Font(17, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.asc.SetValue(True)
        self.asc.SetToolTipString(_(u"Increase counting number."))
        self.asc.Bind(wx.EVT_RADIOBUTTON, main.showPreview)

        self.desc = wx.RadioButton(id=wxID_NUMBERINGPANELDESC, label=_(u"-"),
              name=u'desc', parent=self, pos=wx.Point(552, 104), style=0)
        self.desc.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'Impact'))
        self.desc.SetValue(False)
        self.desc.SetToolTipString(_(u"Decrease counting number."))
        self.desc.Bind(wx.EVT_RADIOBUTTON, main.showPreview)

        self.staticText6 = wx.StaticText(id=wxID_NUMBERINGPANELSTATICTEXT6,
              label=_(u"Count:"), name=u'staticText6', parent=self,
              pos=wx.Point(360, 104), style=0)

        self.alpha_uc = wx.CheckBox(id=wxID_NUMBERINGPANELALPHA_UC,
              label=_(u"Uppercase"), name=u'alpha_uc', parent=self,
              pos=wx.Point(136, 112), style=0)
        self.alpha_uc.SetValue(False)
        self.alpha_uc.Enable(False)
        self.alpha_uc.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.start = wx.SpinCtrl(id=wxID_NUMBERINGPANELSTART, initial=0,
              max=100000000, min=0, name=u'start', parent=self,
              pos=wx.Point(416, 40), size=wx.Size(168, -1),
              style=wx.SP_ARROW_KEYS)
        self.start.SetValue(1)
        self.start.SetToolTipString(_(u"starting number or equivalent alpha/roman character"))
        self.start.Bind(wx.EVT_TEXT_ENTER, main.showPreview, id=wxID_NUMBERINGPANELSTART)
        self.start.Bind(wx.EVT_SPINCTRL, main.showPreview, id=wxID_NUMBERINGPANELSTART)

        self.staticText1 = wx.StaticText(id=wxID_NUMBERINGPANELSTATICTEXT1,
              label=_(u"Reset every:"), name=u'staticText1', parent=self,
              pos=wx.Point(344, 203), style=0)

        self.reset = wx.SpinCtrl(id=wxID_NUMBERINGPANELRESET, initial=0,
              max=100000000, min=0, name=u'reset', parent=self,
              pos=wx.Point(416, 200), size=wx.Size(168, -1),
              style=wx.SP_ARROW_KEYS)
        self.reset.SetValue(0)
        self.reset.SetToolTipString(_(u"0 = don't reset"))
        self.reset.SetRange(0, 100000000)
        self.reset.Bind(wx.EVT_TEXT_ENTER, main.showPreview,
              id=wxID_NUMBERINGPANELRESET)
        self.reset.Bind(wx.EVT_SPINCTRL, main.showPreview,
              id=wxID_NUMBERINGPANELRESET)

        self.digit_autopad = wx.RadioButton(id=wxID_NUMBERINGPANELDIGIT_AUTOPAD,
              label=_(u"Auto pad"), name=u'digit_autopad', parent=self,
              pos=wx.Point(56, 68), style=wx.RB_GROUP)
        self.digit_autopad.SetValue(True)
        self.digit_autopad.Bind(wx.EVT_RADIOBUTTON, self.check_styles)

        self.digit_setpad = wx.RadioButton(id=wxID_NUMBERINGPANELDIGIT_SETPAD,
              label=_(u"Fixed pad width:"), name=u'digit_setpad', parent=self,
              style=0)
        self.digit_setpad.SetValue(False)
        self.digit_setpad.Bind(wx.EVT_RADIOBUTTON, self.check_styles)

        self.resetDir = wx.CheckBox(id=wxID_NUMBERINGPANELRESETDIR,
              label=_(u"Reset every directory"), name=u'resetDir', parent=self,
              pos=wx.Point(456, 232), style=0)
        self.resetDir.SetToolTipString(_(u"Reset count to initial value when directory changes."))
        self.resetDir.SetValue(False)
        self.resetDir.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.countByDir = wx.CheckBox(id=wxID_NUMBERINGPANELCOUNTBYDIR,
              label=_(u"Count by directory"), name=u'countByDir', parent=self,
              pos=wx.Point(472, 168), style=0)
        self.countByDir.SetToolTipString(_(u"Only increase/decrease count when directory changes."))
        self.countByDir.SetValue(False)
        self.countByDir.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.startByItems = wx.CheckBox(id=wxID_NUMBERINGPANELSTARTBYITEM,
              label=_(u"Start at number of items"), name=u'start_by_item',
              parent=self, pos=wx.Point(440, 72), style=0)
        self.startByItems.SetValue(False)
        self.startByItems.SetToolTipString(_(u"Use number of items as starting point for count."))
        self.startByItems.Bind(wx.EVT_CHECKBOX, self.OnStartByItemsCheckbox,
              id=wxID_NUMBERINGPANELSTARTBYITEM)

    def __init__(self, parent, main_window):
        global main
        main = main_window
        self._init_ctrls(parent)
        self.sizer()
        self.setSortingOptions(0)

    # determine style:
    def GetNumberStyle(self):
        #digit:
        style = ''
        if self.digit.GetValue():
            pad = self.digit_pad.GetValue()
            pad_char = self.pad_char.GetValue()
            if self.digit_setpad.GetValue():
                pad_width = self.pad_width.GetValue()
            else:
                pad_width = u"auto"
            style = (u"digit", pad_char, pad_width, pad)

        #alphabetical:
        elif self.alpha.GetValue():
            style = (u"alpha", self.alpha_uc.GetValue(), self.alpha_pad.GetValue())

        #roman numeral:
        elif self.roman.GetValue():
            style = (u"roman", self.roman_uc.GetValue())
        return style

    # determine parameters:
    def GetNumberParams(self):
        #ascending:
        if self.asc.GetValue() == True:
            step_dir = +int(self.step.GetValue())
        #descending:
        else:
            step_dir = -int(self.step.GetValue())
        params = (self.start.GetValue(), step_dir, self.reset.GetValue(),
          self.resetDir.GetValue(), self.countByDir.GetValue(),
          self.startByItems.GetValue(),)
        return params

    # enables/disables item position change buttons:
    def setSortingOptions(self, event):
        sortButtons = (self.staticText2,self.upButton, self.downButton,
          self.upMore,self.downMore,self.upTop,self.downBottom,)
        if self.sorting.GetSelection() == 2:
            for item in sortButtons:
                item.Enable(True)
        else:
            for item in sortButtons:
                item.Enable(False)
        main.showPreview(event)

    #enable/disable options based on what is selected:
    def check_styles(self, event):
        #digit:
        digit_options = (self.digit_pad, self.pad_char, self.digit_setpad,
            self.digit_autopad, self.pad_width)
        pad_options = (self.digit_setpad, self.digit_autopad, self.pad_char,
            self.pad_width)
        if self.digit.GetValue():
            self.digit_pad.Enable(True)
            if self.digit_pad.GetValue():
                for option in pad_options:
                    option.Enable(True)
            else:
                for option in pad_options:
                    option.Enable(False)
            if self.reset.GetValue() == 4999:
                self.reset.SetValue(0)
        else:
            for option in digit_options:
                option.Enable(False)

        #roman numeral:
        if self.roman.GetValue():
            self.roman_uc.Enable(True)
            if self.reset.GetValue() > 4999:
                self.reset.SetValue(4999)
            if self.start.GetValue() == 0:
                self.start.SetValue(1)
        else:
            self.roman_uc.Enable(False)

        #alphabetical:
        if self.alpha.GetValue():
            self.alpha_uc.Enable(True)
            self.alpha_pad.Enable(True)
            if self.start.GetValue() == 0:
                self.start.SetValue(1)
            if self.reset.GetValue() == 4999:
                self.reset.SetValue(0)
        else:
            self.alpha_uc.Enable(False)
            self.alpha_pad.Enable(False)
        main.showPreview(event)

    def OnStartByItemsCheckbox(self, event):
        if self.startByItems.GetValue():
            self.start.Enable(False)
        else:
            self.start.Enable(True)
        main.showPreview(event)

    def OnPad_widthSpinctrl(self, event):
        self.digit_setpad.SetValue(True)
        main.showPreview(event)

    # triggered when a button to change item position is clicked
    def changeItemOrder(self, event):
        buttons = {
          wxID_NUMBERINGPANELUPBUTTON : -1,
          wxID_NUMBERINGPANELDOWNBUTTON : 1,
          wxID_NUMBERINGPANELUPMORE : -5,
          wxID_NUMBERINGPANELDOWNMORE : 5,
          wxID_NUMBERINGPANELUPTOP : u'top',
          wxID_NUMBERINGPANELDOWNBOTTOM : u'bottom',
          }

        change = buttons[event.GetId()]
        main.changeItemOrder(change)


###### GET/SET CONFIGURATION SETTINGS: #########################################
    def getSettings(self):
        settings = (u"<[numbering]>",
          u"digit>:>%s" %int(self.digit.GetValue()),
          u"digit_pad>:>%s" %int(self.digit_pad.GetValue()),
          u"pad_char>:>%s" %self.pad_char.GetValue(),
          u"digit_setpad>:>%s" %int(self.digit_setpad.GetValue()),
          u"digit_autopad>:>%s" %int(self.digit_autopad.GetValue()),
          u"pad_width>:>%s" %self.pad_width.GetValue(),
          u"alpha>:>%s" %int(self.alpha.GetValue()),
          u"alpha_uc>:>%s" %int(self.alpha_uc.GetValue()),
          u"alpha_pad>:>%s" %int(self.alpha_pad.GetValue()),
          u"roman>:>%s" %int(self.roman.GetValue()),
          u"roman_uc>:>%s" %int(self.roman_uc.GetValue()),
          u"start>:>%s" %self.start.GetValue(),
          u"asc>:>%s" %int(self.asc.GetValue()),
          u"desc>:>%s" %int(self.desc.GetValue()),
          u"step>:>%s" %int(self.step.GetValue()),
          u"reset>:>%s" %int(self.reset.GetValue()),
          u"resetDir>:>%s" %int(self.resetDir.GetValue()),
          u"countByDir>:>%s" %int(self.countByDir.GetValue()),
          u"startByItems>:>%s" %int(self.startByItems.GetValue()),
          u"sorting>:>%s" %self.sorting.GetSelection(),
          )
        return settings

    def setSettings(self,settings):
        if len(settings) == 20: #make sure number of settings is correct
            try:
                self.digit.SetValue(int(settings[0]))
                self.digit_pad.SetValue(int(settings[1]))
                self.pad_char.SetValue(settings[2])
                self.digit_setpad.SetValue(int(settings[3]))
                self.digit_autopad.SetValue(int(settings[4]))
                self.pad_width.SetValue(int(settings[5]))
                self.alpha.SetValue(int(settings[6]))
                self.alpha_uc.SetValue(int(settings[7]))
                self.alpha_pad.SetValue(int(settings[8]))
                self.roman.SetValue(int(settings[9]))
                self.roman_uc.SetValue(int(settings[10]))
                self.start.SetValue(int(settings[11]))
                self.asc.SetValue(int(settings[12]))
                self.desc.SetValue(int(settings[13]))
                self.step.SetValue(int(settings[14]))
                self.reset.SetValue(int(settings[15]))
                self.resetDir.SetValue(int(settings[16]))
                self.countByDir.SetValue(int(settings[17]))
                self.startByItems.SetValue(int(settings[18]))
                self.sorting.SetSelection(int(settings[19].replace(u'\n','')))
            except ValueError:
                return False
            else:
                # apply settings:
                self.check_styles(0)
                self.setSortingOptions(0)
                return True
        else:
            return False



