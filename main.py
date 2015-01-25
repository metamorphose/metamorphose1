# -*- coding: utf-8 -*-

# This is the main configuration panel in the main
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
import wx.lib.dialogs
import codecs

[wxID_MAINPANEL, wxID_MAINPANELAPPLY_TO_EXT, wxID_MAINPANELAPPLY_TO_NAME,
 wxID_MAINPANELA_Z, wxID_MAINPANELCHAR_SETS, wxID_MAINPANELDIGIT,
 wxID_MAINPANELID3, wxID_MAINPANELID3_SELECT, wxID_MAINPANELINSERT,
 wxID_MAINPANELINSERT_CHAR_TXT, wxID_MAINPANELINSERT_POSITION,
 wxID_MAINPANELINSERT_POSITION_VALUE, wxID_MAINPANELINSERT_REPETION_VALUE,
 wxID_MAINPANELINSERT_REPETITION, wxID_MAINPANELINSERT_TXT,
 wxID_MAINPANELINS_DATE, wxID_MAINPANELINS_DIR, wxID_MAINPANELINS_NUM,
 wxID_MAINPANELINS_TIME, wxID_MAINPANELINVERSE, wxID_MAINPANELMOD_LENGTH,
 wxID_MAINPANELMOD_LENGTH_CHBOX, wxID_MAINPANELMOD_LENGTH_DIRECTION,
 wxID_MAINPANELMOD_LENGTH_PAD, wxID_MAINPANELMOD_LENGTH_POSITION,
 wxID_MAINPANELMOD_LENGTH_TYPE, wxID_MAINPANELPREFIX,
 wxID_MAINPANELPREFIX_TXT, wxID_MAINPANELREG_EXPR, wxID_MAINPANELREG_EXP_DIV,
 wxID_MAINPANELREG_EXP_I, wxID_MAINPANELREG_EXP_U, wxID_MAINPANELREG_EXP_TEXT,
 wxID_MAINPANELREPLACE, wxID_MAINPANELREPL_CASE, wxID_MAINPANELREPL_END,
 wxID_MAINPANELREPL_FIND, wxID_MAINPANELREPL_FROM, wxID_MAINPANELREPL_FRONT,
 wxID_MAINPANELREPL_MOVE, wxID_MAINPANELREPL_MOVE_POS,
 wxID_MAINPANELREPL_MOVE_POS_VALUE, wxID_MAINPANELREPL_MOVE_TXT,
 wxID_MAINPANELREPL_MOVE_TXT_MOD, wxID_MAINPANELREPL_MOVE_TXT_RE,
 wxID_MAINPANELREPL_MOVE_TXT_VALUE, wxID_MAINPANELREPL_OPERATION,
 wxID_MAINPANELREPL_OPERATION_VALUE, wxID_MAINPANELREPL_POSBUTTON,
 wxID_MAINPANELREPL_REPLACE,
 wxID_MAINPANELREPL_TEXTBUTTON, wxID_MAINPANELREPL_TO, wxID_MAINPANELREPL_TXT,
 wxID_MAINPANELREPL_TXT_FROM, wxID_MAINPANELREPL_TXT_TO,
 wxID_MAINPANELSTATICLINE1, wxID_MAINPANELSTATICLINE2,
 wxID_MAINPANELSTATICTEXT1, wxID_MAINPANELSTATICTEXT2,
 wxID_MAINPANELSTATICTEXT3, wxID_MAINPANELSTATICTEXT4,
 wxID_MAINPANELSTATICTEXT5, wxID_MAINPANELSTATICTEXT6,
 wxID_MAINPANELSTATICTEXT7, wxID_MAINPANELSTATICTEXT8, wxID_MAINPANELSUBDIR,
 wxID_MAINPANELSUBDIR_TXT, wxID_MAINPANELSUFFIX, wxID_MAINPANELSUFFIX_TXT,
] = [wx.NewId() for _init_ctrls in range(69)]

class mainPanel(wx.Panel):
    global main_pos
    main_pos = [False, False, False, False, False, False]

    def sizer(self):
        #buttons on top:
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons = [(self.staticText1,4),
                   (self.ins_dir,4),
                   (self.ins_num,4),
                   (self.ins_date,4),
                   (self.ins_time,4),
                   (self.id3,2),
                   (self.id3_select,0),]
        if main.langLTR:
            for i in buttons:
                buttonSizer.Add(i[0],0,wx.RIGHT|wx.ALIGN_CENTER,i[1])
        else:
            buttons.reverse()
            for i in buttons:
                buttonSizer.Add(i[0],0,wx.LEFT|wx.ALIGN_CENTER,i[1])


        #first row of options:
        rowA = wx.BoxSizer(wx.HORIZONTAL)
        applyTo = wx.BoxSizer(wx.VERTICAL)
        applyTo.Add(self.apply_to_name,0,wx.BOTTOM|main.alignment,1)
        applyTo.Add(self.apply_to_ext,0,main.alignment)
        rowAelements = [(self.staticText7,0,5),
                        (applyTo,0,5),
                        (self.staticLine2,0,5),
                        (self.SubDir,0,3),
                        (self.SubDir_txt,1,5),
                        (self.prefix,0,3),
                        (self.prefix_txt,1,5),
                        (self.suffix,0,3),
                        (self.suffix_txt,1,5)]
        if main.langLTR:
            for i in rowAelements:
                rowA.Add(i[0],i[1],wx.ALIGN_CENTER|wx.RIGHT,i[2])
        else:
            rowAelements.reverse()
            for i in rowAelements:
                rowA.Add(i[0],i[1],wx.ALIGN_CENTER|wx.LEFT,i[2])

        #start of replace
        #text
        rowB = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            rowB.Add(self.repl_textButton,0,wx.ALIGN_CENTER|wx.RIGHT,3)
            rowB.Add(self.repl_find,1,wx.RIGHT,10)
            rowB.Add(self.repl_case,0,wx.ALIGN_CENTER|wx.RIGHT,5)
        else:
            rowB.Add(self.repl_case,0,wx.ALIGN_CENTER|wx.LEFT,3)
            rowB.Add(self.repl_find,1,wx.LEFT,10)
            rowB.Add(self.repl_textButton,0,wx.ALIGN_CENTER|wx.LEFT,5)


        #regular expression:
        regExpRow = wx.BoxSizer(wx.HORIZONTAL)
        regExpRowElements = [(self.reg_expr,0,3),
                          (self.reg_exp_text,1,2),
                          (self.reg_exp_i,0,2),
                          (self.reg_exp_u,0,6),
                          (self.reg_exp_div,0,6),
                          (self.char_sets,0,2),
                          (self.inverse,0,2),
                          (self.a_z,0,2),
                          (self.digit,0,0)]
        if main.langLTR:
            for i in regExpRowElements:
                regExpRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.RIGHT,i[2])
        else:
            regExpRowElements.reverse()
            for i in regExpRowElements:
                regExpRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.LEFT,i[2])

        #position:
        positionRow = wx.BoxSizer(wx.HORIZONTAL)
        positionRowElements = [(self.repl_posButton,4),
                            (self.repl_from,15),
                            (self.repl_txt_to,4),
                            (self.repl_to,20),
                            (self.repl_txt_from,4),
                            (self.repl_front,10),
                            (self.repl_end,10)]
        if main.langLTR:
            for i in positionRowElements:
                positionRow.Add(i[0],0,wx.ALIGN_CENTER|wx.RIGHT,i[1])
        else:
            positionRowElements.reverse()
            for i in positionRowElements:
                positionRow.Add(i[0],0,wx.ALIGN_CENTER|wx.LEFT,i[1])

        #replace with or modify
        replaceRow = wx.BoxSizer(wx.HORIZONTAL)
        replaceRowElements = [(self.repl_replace,0,5),
                           (self.repl_txt,1,15),
                           (self.repl_operation,0,0),
                           (self.repl_operation_value,0,5)]
        if main.langLTR:
            for i in replaceRowElements:
                replaceRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.RIGHT,i[2])
        else:
            replaceRowElements.reverse()
            for i in replaceRowElements:
                replaceRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.LEFT,i[2])

        #move
        moveRow = wx.BoxSizer(wx.HORIZONTAL)
        moveRowElements = [(self.repl_move,0,10),
                           (self.repl_move_pos,0,3),
                           (self.repl_move_pos_value,0,20),
                           (self.repl_move_txt,0,3),
                           (self.repl_move_txt_mod,0,3),
                           (self.staticText6,0,3),
                           (self.repl_move_txt_value,1,3),
                           (self.repl_move_txt_re,0,5),]
        if main.langLTR:
            for i in moveRowElements:
                moveRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.RIGHT,i[2])
        else:
            moveRowElements.reverse()
            for i in moveRowElements:
                moveRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.LEFT,i[2])

        paramSizer = wx.BoxSizer(wx.VERTICAL)
        paramSizer.Add(rowB,0,wx.EXPAND|main.alignment)
        paramSizer.Add(regExpRow,0,wx.EXPAND|wx.TOP|main.alignment,7)
        paramSizer.Add(positionRow,0,wx.TOP|main.alignment,7)

        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        if main.langLTR:
            searchSizer.Add(self.replace,0,wx.LEFT,5)
            searchSizer.Add(paramSizer,1,wx.EXPAND|main.alignment)
        else:
            searchSizer.Add(paramSizer,1,wx.EXPAND|main.alignment)
            searchSizer.Add(self.replace,0,wx.RIGHT,5)
        #end of replace

        #insert:
        insertRow = wx.BoxSizer(wx.HORIZONTAL)
        insertRowElements = [(self.insert,0,5),
                            (self.insert_position,0,4),
                            (self.insert_position_value,0,10),
                            (self.insert_repetition,0,0),
                            (self.insert_repetion_value,0,4),
                            (self.insert_char_txt,0,15),
                            (self.insert_txt,1,5),]
        if main.langLTR:
            for i in insertRowElements:
                insertRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.RIGHT,i[2])
        else:
            insertRowElements.reverse()
            for i in insertRowElements:
                insertRow.Add(i[0],i[1],wx.ALIGN_CENTER|wx.LEFT,i[2])

        #Modify Length:
        modLengthRow = wx.BoxSizer(wx.HORIZONTAL)
        modLengthRowElements = [(self.mod_length_chbox,5),
                            (self.mod_length_type,10),
                            (self.staticText2,4),
                            (self.mod_length,3),
                            (self.staticText8,8),
                            (self.staticText4,4),
                            (self.mod_length_direction,8),
                            (self.staticText3,4),
                            (self.mod_length_pad,8),
                            (self.staticText5,4),
                            (self.mod_length_position,4),]
        if main.langLTR:
            for i in modLengthRowElements:
                modLengthRow.Add(i[0],0,wx.ALIGN_CENTER|wx.RIGHT,i[1])
        else:
            modLengthRowElements.reverse()
            modLengthRow.Add((-1,-1),1)
            for i in modLengthRowElements:
                modLengthRow.Add(i[0],0,wx.ALIGN_CENTER|wx.LEFT,i[1])

        #main panel sizer:
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(buttonSizer,0,wx.ALL|main.alignment,5)
        mainSizer.Add(self.staticLine1,0,wx.EXPAND|wx.LEFT|wx.RIGHT,12)
        mainSizer.Add((-1,10),0)
        mainSizer.Add(rowA,0,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
        mainSizer.Add(searchSizer,0,wx.EXPAND|wx.TOP,10)
        mainSizer.Add(replaceRow,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
        mainSizer.Add(moveRow,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
        mainSizer.Add((15,15),0)
        mainSizer.Add(insertRow,0,wx.EXPAND|wx.LEFT|wx.RIGHT|main.alignment,5)
        mainSizer.Add((15,15),0)
        mainSizer.Add(modLengthRow,0,wx.EXPAND|wx.LEFT|wx.RIGHT|main.alignment,5)
        mainSizer.Add((-1,5))

        self.SetSizerAndFit(mainSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_MAINPANEL, name=u'mainPanel',
              parent=prnt, pos=wx.Point(303, 344), size=wx.Size(679, 344),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(671, 315))
        self.SetThemeEnabled(True)

        txt = _(u"sub-dir")
        self.ins_dir = wx.Button(id=wxID_MAINPANELINS_DIR, label=txt,
              name=u'ins_dir', parent=self, pos=wx.Point(248, 8), style=0)
        Size = wx.Size(self.ins_dir.GetTextExtent(txt)[0] + 20,-1)
        self.ins_dir.SetMinSize(Size)
        self.ins_dir.SetToolTipString(_(u"Insert sub-directory. Only works in 'dir' field"))
        self.ins_dir.Bind(wx.EVT_BUTTON, self.OnIns_dirButton,
              id=wxID_MAINPANELINS_DIR)

        self.ins_date = wx.Button(id=wxID_MAINPANELINS_DATE, label=_(u"date"),
              name=u'ins_date', parent=self, pos=wx.Point(400, 8),
              size=wx.Size(57, -1), style=0)
        self.ins_date.SetToolTipString(_(u"Insert date. Use the 'Date and Time' panel to\nchange settings"))
        self.ins_date.Enable(True)
        self.ins_date.Bind(wx.EVT_BUTTON, self.OnIns_dateButton,
              id=wxID_MAINPANELINS_DATE)

        self.ins_time = wx.Button(id=wxID_MAINPANELINS_TIME, label=_(u"time"),
              name=u'ins_time', parent=self, pos=wx.Point(456, 8),
              size=wx.Size(57, -1), style=0)
        self.ins_time.SetToolTipString(_(u"Insert time. Use the 'Date and Time' panel to\nchange settings"))
        self.ins_time.Enable(True)
        self.ins_time.Bind(wx.EVT_BUTTON, self.OnIns_timeButton,
              id=wxID_MAINPANELINS_TIME)

        txt = _(u"numbering")
        self.ins_num = wx.Button(id=wxID_MAINPANELINS_NUM,
              label=txt, name=u'ins_num', parent=self, style=0)
        Size = wx.Size(self.ins_num.GetTextExtent(txt)[0] + 20,-1)
        self.ins_num.SetMinSize(Size)
        self.ins_num.SetToolTipString(_(u"Insert enumerating sequence. Use the 'Numbering'\npanel to change settings"))
        self.ins_num.Bind(wx.EVT_BUTTON, self.OnIns_numButton,
              id=wxID_MAINPANELINS_NUM)

        self.id3 = wx.Button(id=wxID_MAINPANELID3, label=_(u"id3:"), name=u'id3',
              parent=self, pos=wx.Point(520, 8), size=wx.Size(47, -1), style=0)
        self.id3.SetToolTipString(_(u"Insert id3 tag information from file"))
        self.id3.Bind(wx.EVT_BUTTON, self.OnId3Button, id=wxID_MAINPANELID3)

        self.id3_select = wx.Choice(choices=[_(u"album"), _(u"performer"),
              _(u"title"), _(u"track"), _(u"year"), _(u"genre")],
              id=wxID_MAINPANELID3_SELECT, name=u'id3_select', parent=self,
              pos=wx.Point(568, 9), style=0)
        self.id3_select.SetSelection(2)
        self.id3_select.SetToolTipString(_(u"Select which Id3 tag to read."))

        self.SubDir = wx.CheckBox(id=wxID_MAINPANELSUBDIR, label=_(u"Dir:"),
              name=u'SubDir', parent=self, pos=wx.Point(200, 56), style=0)
        self.SubDir.SetValue(False)
        self.SubDir.Enable(True)
        self.SubDir.SetToolTipString(_(u"Add directory"))
        self.SubDir.Bind(wx.EVT_CHECKBOX, self.OnSubDirCheckbox,
              id=wxID_MAINPANELSUBDIR)

        self.SubDir_txt = wx.TextCtrl(id=wxID_MAINPANELSUBDIR_TXT,
              name=u'SubDir_txt', parent=self, pos=wx.Point(240, 56), style=0,
              value='')
        self.SubDir_txt.Enable(False)
        self.SubDir_txt.SetToolTipString(_(u"Use 'sub-dir' button to add sub-directories"))
        self.SubDir_txt.Bind(wx.EVT_LEFT_DOWN, self.OnSubDir_txtLeftDown)
        self.SubDir_txt.Bind(wx.EVT_TEXT, main.showPreview)

        self.prefix = wx.CheckBox(id=wxID_MAINPANELPREFIX, label=_(u"Prefix:"),
              name=u'prefix', parent=self, pos=wx.Point(344, 56), style=0)
        self.prefix.SetValue(False)
        self.prefix.Enable(True)
        self.prefix.Bind(wx.EVT_CHECKBOX, self.OnPrefixCheckbox,
              id=wxID_MAINPANELPREFIX)

        self.prefix_txt = wx.TextCtrl(id=wxID_MAINPANELPREFIX_TXT,
              name=u'prefix_txt', parent=self, pos=wx.Point(400, 56), style=0,
              value='')
        self.prefix_txt.Enable(False)
        self.prefix_txt.SetMaxLength(255)
        self.prefix_txt.Bind(wx.EVT_LEFT_DOWN, self.OnPrefix_txtLeftDown)
        self.prefix_txt.Bind(wx.EVT_TEXT, main.showPreview)

        self.suffix = wx.CheckBox(id=wxID_MAINPANELSUFFIX, label=_(u"Suffix:"),
              name=u'suffix', parent=self, pos=wx.Point(504, 56), style=0)
        self.suffix.SetValue(False)
        self.suffix.Bind(wx.EVT_CHECKBOX, self.OnSuffixCheckbox,
              id=wxID_MAINPANELSUFFIX)

        self.suffix_txt = wx.TextCtrl(id=wxID_MAINPANELSUFFIX_TXT,
              name=u'suffix_txt', parent=self, pos=wx.Point(560, 56), style=0,
              value='')
        self.suffix_txt.Enable(False)
        self.suffix_txt.SetMaxLength(255)
        self.suffix_txt.Bind(wx.EVT_LEFT_DOWN, self.OnSuffix_txtLeftDown)
        self.suffix_txt.Bind(wx.EVT_TEXT, main.showPreview)

        self.replace = wx.CheckBox(id=wxID_MAINPANELREPLACE,
              label=_(u"Search:"), name=u'replace', parent=self, pos=wx.Point(8,
              96), style=0)
        self.replace.SetValue(False)
        self.replace.SetToolTipString(_(u"Search and: replace, modify, or move"))
        self.replace.Bind(wx.EVT_CHECKBOX, self.OnReplaceCheckbox,
              id=wxID_MAINPANELREPLACE)

        self.insert = wx.CheckBox(id=wxID_MAINPANELINSERT, label=_(u"Insert:"),
              name=u'insert', parent=self, pos=wx.Point(8, 248), style=0)
        self.insert.SetValue(False)
        self.insert.SetToolTipString(_(u"Insert into name."))
        self.insert.Bind(wx.EVT_CHECKBOX, self.OnInsertCheckbox,
              id=wxID_MAINPANELINSERT)

        self.insert_txt = wx.TextCtrl(id=wxID_MAINPANELINSERT_TXT,
              name=u'insert_txt', parent=self, pos=wx.Point(392, 237),
              style=0, value='')
        self.insert_txt.Enable(False)
        self.insert_txt.SetMaxLength(255)
        self.insert_txt.Bind(wx.EVT_LEFT_DOWN, self.OnInsert_txtLeftDown)
        self.insert_txt.Bind(wx.EVT_TEXT, main.showPreview)

        self.insert_position_value = wx.SpinCtrl(id=wxID_MAINPANELINSERT_POSITION_VALUE,
              initial=0, max=255, min=-255, name=u'insert_position_value',
              parent=self, pos=wx.Point(144, 238), size=wx.Size(50, -1),
              style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.insert_position_value.SetRange(-255, 255)
        self.insert_position_value.SetValue(0)
        self.insert_position_value.Enable(False)
        self.insert_position_value.SetToolTipString(_(u"Use negative values to start from end of name."))
        self.insert_position_value.Bind(wx.EVT_TEXT_ENTER, main.showPreview)
        self.insert_position_value.Bind(wx.EVT_SPINCTRL, main.showPreview)

        self.repl_find = wx.TextCtrl(id=wxID_MAINPANELREPL_FIND,
              name=u'repl_find', parent=self, pos=wx.Point(208, 96),
              style=0, value='')
        self.repl_find.Enable(False)
        self.repl_find.SetToolTipString(_(u"Keep blank to replace entire name."))
        self.repl_find.Bind(wx.EVT_LEFT_DOWN, self.OnRepl_findLeftDown)
        self.repl_find.Bind(wx.EVT_TEXT, main.showPreview)

        self.repl_case = wx.CheckBox(id=wxID_MAINPANELREPL_CASE,
              label=_(u"case sensitive"), name=u'repl_case', parent=self,
              pos=wx.Point(576, 96), style=0)
        self.repl_case.SetValue(False)
        self.repl_case.Enable(False)
        self.repl_case.SetToolTipString(_(u"Differentiate between upper and lower case."))
        self.repl_case.Bind(wx.EVT_CHECKBOX, self.OnPrefixCheckbox)

        self.repl_txt_to = wx.StaticText(id=wxID_MAINPANELREPL_TXT_TO,
              label=_(u"Length:"), name=u'repl_txt_to', parent=self,
              pos=wx.Point(224, 152), style=0)
        self.repl_txt_to.Enable(False)

        self.repl_to = wx.SpinCtrl(id=wxID_MAINPANELREPL_TO, initial=1, max=255,
              min=1, name=u'repl_to', parent=self, pos=wx.Point(264, 152),
              size=wx.Size(64, -1), style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.repl_to.SetValue(1)
        self.repl_to.Enable(False)
        self.repl_to.Bind(wx.EVT_TEXT_ENTER, self.setCorrectSearchPosition,
              id=wxID_MAINPANELREPL_TO)
        self.repl_to.Bind(wx.EVT_SPINCTRL, self.setCorrectSearchPosition,
              id=wxID_MAINPANELREPL_TO)

        self.repl_from = wx.SpinCtrl(id=wxID_MAINPANELREPL_FROM, initial=0,
              max=255, min=0, name=u'repl_from', parent=self, pos=wx.Point(128,
              152), size=wx.Size(70, -1), style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.repl_from.SetValue(0)
        self.repl_from.Enable(False)
        self.repl_from.Bind(wx.EVT_TEXT_ENTER, main.showPreview)
        self.repl_from.Bind(wx.EVT_SPINCTRL, main.showPreview)

        self.staticLine1 = wx.StaticLine(id=wxID_MAINPANELSTATICLINE1,
              name=u'staticLine1', parent=self, pos=wx.Point(16, 42),
              size=wx.Size(-1, 2), style=wx.LI_HORIZONTAL)

        self.repl_textButton = wx.RadioButton(id=wxID_MAINPANELREPL_TEXTBUTTON,
              label=_(u"Text (blank for all):"), name=u'repl_textButton',
              parent=self, pos=wx.Point(80, 96), style=wx.RB_GROUP)
        self.repl_textButton.SetValue(True)
        self.repl_textButton.Enable(False)
        self.repl_textButton.Bind(wx.EVT_RADIOBUTTON,
              self.ActivateReplaceOptions, id=wxID_MAINPANELREPL_TEXTBUTTON)

        self.reg_exp_text = wx.TextCtrl(id=wxID_MAINPANELREG_EXP_TEXT,
              name=u'reg_exp_text', parent=self, pos=wx.Point(128, 120),
              style=0, value='')
        self.reg_exp_text.Enable(False)
        self.reg_exp_text.Bind(wx.EVT_LEFT_DOWN, self.OnReg_exp_textLeftDown)
        self.reg_exp_text.Bind(wx.EVT_TEXT, main.showPreview)

        self.repl_posButton = wx.RadioButton(id=wxID_MAINPANELREPL_POSBUTTON,
              label=_(u"Position:"), name=u'repl_posButton', parent=self,
              pos=wx.Point(56, 144), style=0)
        self.repl_posButton.SetValue(False)
        self.repl_posButton.Enable(False)
        self.repl_posButton.Bind(wx.EVT_RADIOBUTTON,
              self.ActivateReplaceOptions, id=wxID_MAINPANELREPL_POSBUTTON)

        self.reg_expr = wx.RadioButton(id=wxID_MAINPANELREG_EXPR,
              label=_(u"Reg-Expr:"), name=u'reg_expr', parent=self,
              pos=wx.Point(56, 120), style=0)
        self.reg_expr.SetValue(False)
        self.reg_expr.SetToolTipString(_(u"Regular Expression"))
        self.reg_expr.Enable(False)
        self.reg_expr.Bind(wx.EVT_RADIOBUTTON, self.ActivateReplaceOptions,
              id=wxID_MAINPANELREG_EXPR)

        self.repl_txt_from = wx.StaticText(id=wxID_MAINPANELREPL_TXT_FROM,
              label=_(u"Start at the:"), name=u'repl_txt_from', parent=self,
              pos=wx.Point(368, 152), style=0)
        self.repl_txt_from.Enable(False)

        self.repl_txt = wx.TextCtrl(id=wxID_MAINPANELREPL_TXT, name=u'repl_txt',
              parent=self, pos=wx.Point(208, 180), style=0, value='')
        self.repl_txt.Enable(False)
        self.repl_txt.SetToolTipString(_(u"Keep blank to delete."))
        self.repl_txt.SetMaxLength(255)
        self.repl_txt.Bind(wx.EVT_LEFT_DOWN, self.OnReplace_txtLeftDown)
        self.repl_txt.Bind(wx.EVT_TEXT, main.showPreview)

        self.a_z = wx.CheckBox(id=wxID_MAINPANELA_Z, label=_(u"[a-z]"),
              name=u'a_z', parent=self, pos=wx.Point(528, 128), style=0)
        self.a_z.SetToolTipString(_(u"All alphabetical characters"))
        self.a_z.SetValue(False)
        self.a_z.Enable(False)
        self.a_z.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.digit = wx.CheckBox(id=wxID_MAINPANELDIGIT, label=_(u"[0-9]"),
              name=u'digit', parent=self, pos=wx.Point(584, 128), style=0)
        self.digit.SetToolTipString(_(u"All number characters"))
        self.digit.SetValue(False)
        self.digit.Enable(False)
        self.digit.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.reg_exp_i = wx.CheckBox(id=wxID_MAINPANELREG_EXP_I, label=_(u"I"),
              name=u'reg_exp_i', parent=self, pos=wx.Point(256, 128), style=0)
        self.reg_exp_i.SetValue(True)
        self.reg_exp_i.SetToolTipString(_(u"case-Insensitive match"))
        self.reg_exp_i.Enable(False)
        self.reg_exp_i.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.reg_exp_u = wx.CheckBox(id=wxID_MAINPANELREG_EXP_U, label=_(u"U"),
              name=u'reg_exp_u', parent=self, pos=wx.Point(288, 128), style=0)
        self.reg_exp_u.SetValue(True)
        self.reg_exp_u.SetToolTipString(_(u"Unicode match (\w matches etc)"))
        self.reg_exp_u.Enable(False)
        self.reg_exp_u.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.repl_end = wx.RadioButton(id=wxID_MAINPANELREPL_END,
              label=_(u"end"), name=u'repl_end', parent=self, pos=wx.Point(456,
              152), style=wx.RB_GROUP)
        self.repl_end.SetValue(False)
        self.repl_end.Enable(False)
        self.repl_end.Bind(wx.EVT_RADIOBUTTON, self.setCorrectSearchPosition,
              id=wxID_MAINPANELREPL_END)

        self.repl_front = wx.RadioButton(id=wxID_MAINPANELREPL_FRONT,
              label=_(u"begining"), name=u'repl_front', parent=self,
              pos=wx.Point(512, 152), style=0)
        self.repl_front.SetValue(True)
        self.repl_front.Enable(False)
        self.repl_front.Bind(wx.EVT_RADIOBUTTON, self.setCorrectSearchPosition,
              id=wxID_MAINPANELREPL_FRONT)

        self.staticText1 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT1,
              label=_(u"Activate a field, then type text or use one of \n the buttons at left to enter in an operation."),
              name=u'staticText1', parent=self, pos=wx.Point(16, 8), style=0)

        self.insert_position = wx.RadioButton(id=wxID_MAINPANELINSERT_POSITION,
              label=_(u"at position:"), name=u'insert_position', parent=self,
              pos=wx.Point(64, 248), style=wx.RB_GROUP)
        self.insert_position.SetValue(True)
        self.insert_position.Enable(False)
        self.insert_position.Bind(wx.EVT_RADIOBUTTON,
              self.ActivateInsertOptions, id=wxID_MAINPANELINSERT_POSITION)

        self.insert_repetition = wx.RadioButton(id=wxID_MAINPANELINSERT_REPETITION,
              label=_(u"every"), name=u'insert_repetition', parent=self,
              pos=wx.Point(216, 240), style=0)
        self.insert_repetition.SetValue(False)
        self.insert_repetition.Enable(False)
        self.insert_repetition.Bind(wx.EVT_RADIOBUTTON,
              self.ActivateInsertOptions, id=wxID_MAINPANELINSERT_REPETITION)

        self.insert_char_txt = wx.StaticText(id=wxID_MAINPANELINSERT_CHAR_TXT,
              label=_(u"characters"), name=u'insert_char_txt', parent=self,
              pos=wx.Point(320, 240), style=0)
        self.insert_char_txt.Enable(False)

        self.insert_repetion_value = wx.SpinCtrl(id=wxID_MAINPANELINSERT_REPETION_VALUE,
              initial=1, max=128, min=1, name=u'insert_repetion_value',
              parent=self, pos=wx.Point(264, 237), size=wx.Size(48, -1),
              style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.insert_repetion_value.SetRange(1, 128)
        self.insert_repetion_value.SetValue(1)
        self.insert_repetion_value.Enable(False)
        self.insert_repetion_value.Bind(wx.EVT_TEXT_ENTER, main.showPreview,
              id=wxID_MAINPANELINSERT_REPETION_VALUE)
        self.insert_repetion_value.Bind(wx.EVT_SPINCTRL, main.showPreview,
              id=wxID_MAINPANELINSERT_REPETION_VALUE)

        self.repl_replace = wx.RadioButton(id=wxID_MAINPANELREPL_REPLACE,
              label=_(u"Replace with (blank to delete):"), name=u'repl_replace',
              parent=self, pos=wx.Point(32, 180), style=wx.RB_GROUP)
        self.repl_replace.SetValue(True)
        self.repl_replace.Enable(False)
        self.repl_replace.Bind(wx.EVT_RADIOBUTTON, self.ActivateReplaceOptions,
              id=wxID_MAINPANELREPL_REPLACE)

        self.repl_operation_value = wx.Choice(choices=[_(u"UPPERCASE"),
              _(u"lowercase"), _(u"SWAP case"), _(u"Capitalize first"),
              _(u"Title Style"), _(u"DoRkIfY")],
              id=wxID_MAINPANELREPL_OPERATION_VALUE,
              name=u'repl_operation_value', parent=self, pos=wx.Point(504, 180),
              style=0)
        self.repl_operation_value.SetMinSize(wx.Size(140,-1))
        self.repl_operation_value.SetSelection(0)
        self.repl_operation_value.Enable(False)
        self.repl_operation_value.SetToolTipString(_(u"Choose the type of case modification."))
        self.repl_operation_value.Bind(wx.EVT_CHOICE, main.showPreview,
              id=wxID_MAINPANELREPL_OPERATION_VALUE)

        self.repl_operation = wx.RadioButton(id=wxID_MAINPANELREPL_OPERATION,
              label=_(u"modify:"), name=u'repl_operation', parent=self,
              pos=wx.Point(448, 184), style=0)
        self.repl_operation.SetToolTipString(_(u"Modifies all matches."))
        self.repl_operation.SetValue(False)
        self.repl_operation.Enable(False)
        self.repl_operation.Bind(wx.EVT_RADIOBUTTON,
              self.ActivateReplaceOptions, id=wxID_MAINPANELREPL_OPERATION)

        self.inverse = wx.CheckBox(id=wxID_MAINPANELINVERSE, label=_(u"^"),
              name=u'inverse', parent=self, pos=wx.Point(488, 128), style=0)
        self.inverse.SetToolTipString(_(u"Anything but ..."))
        self.inverse.SetValue(False)
        self.inverse.Enable(False)
        self.inverse.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.mod_length_chbox = wx.CheckBox(id=wxID_MAINPANELMOD_LENGTH_CHBOX,
              label=_(u"Modify length:"), name=u'mod_length_chbox', parent=self,
              pos=wx.Point(8, 272), style=0)
        self.mod_length_chbox.SetValue(False)
        self.mod_length_chbox.SetToolTipString(_(u"Change the length of the name."))
        self.mod_length_chbox.Bind(wx.EVT_CHECKBOX, self.Mod_length_options,
              id=wxID_MAINPANELMOD_LENGTH_CHBOX)

        self.mod_length = wx.SpinCtrl(id=wxID_MAINPANELMOD_LENGTH, initial=1,
              max=255, min=1, name=u'mod_length', parent=self, pos=wx.Point(224,
              264), size=wx.Size(50, -1), style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.mod_length.SetValue(8)
        self.mod_length.Enable(False)
        self.mod_length.SetToolTipString(_(u"Length after modification"))
        self.mod_length.Bind(wx.EVT_TEXT_ENTER, main.showPreview,
              id=wxID_MAINPANELMOD_LENGTH)
        self.mod_length.Bind(wx.EVT_SPINCTRL, main.showPreview,
              id=wxID_MAINPANELMOD_LENGTH)

        self.staticText2 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT2,
              label=_(u"to:"), name=u'staticText2', parent=self,
              pos=wx.Point(200, 272), style=0)
        self.staticText2.Enable(False)

        self.mod_length_pad = wx.TextCtrl(id=wxID_MAINPANELMOD_LENGTH_PAD,
              name=u'mod_length_pad', parent=self, pos=wx.Point(512, 264),
              size=wx.Size(24, -1), style=0, value='0')
        self.mod_length_pad.SetMaxLength(1)
        self.mod_length_pad.Enable(False)
        self.mod_length_pad.SetToolTipString(_(u"Character to use for padding."))
        self.mod_length_pad.Bind(wx.EVT_TEXT, main.showPreview)

        self.staticText3 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT3,
              label=_(u"pad with:"), name=u'staticText3', parent=self,
              pos=wx.Point(464, 272), style=0)
        self.staticText3.Enable(False)

        self.staticText4 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT4,
              label=_(u"from the:"), name=u'staticText4', parent=self,
              pos=wx.Point(336, 272), style=0)
        self.staticText4.Enable(False)

        self.mod_length_type = wx.Choice(choices=[_(u"Cut"), _(u"Pad"),
              _(u"Both")], id=wxID_MAINPANELMOD_LENGTH_TYPE,
              name=u'mod_length_type', parent=self, pos=wx.Point(104, 264),
              style=0)
        self.mod_length_type.SetSelection(0)
        self.mod_length_type.Enable(False)
        self.mod_length_type.SetToolTipString(_(u"How to change the length."))
        self.mod_length_type.Bind(wx.EVT_CHOICE, self.Mod_length_options,
              id=wxID_MAINPANELMOD_LENGTH_TYPE)

        self.mod_length_direction = wx.Choice(choices=[_(u"right"),
              _(u"left")], id=wxID_MAINPANELMOD_LENGTH_DIRECTION,
              name=u'mod_length_direction', parent=self, pos=wx.Point(384, 264),
              style=0)
        self.mod_length_direction.SetSelection(0)
        self.mod_length_direction.Enable(False)
        self.mod_length_direction.SetToolTipString(_(u"Starting direction for modification."))
        self.mod_length_direction.Bind(wx.EVT_CHOICE, main.showPreview,
              id=wxID_MAINPANELMOD_LENGTH_DIRECTION)

        self.char_sets = wx.StaticText(id=wxID_MAINPANELCHAR_SETS,
              label=_(u"Character sets:"), name=u'char_sets', parent=self,
              pos=wx.Point(392, 128), style=0)
        self.char_sets.Enable(False)

        self.reg_exp_div = wx.StaticLine(id=wxID_MAINPANELREG_EXP_DIV,
              name=u'reg_exp_div', parent=self, pos=wx.Point(346, 127),
              size=wx.Size(2, 18), style=wx.LI_VERTICAL)

        self.staticText5 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT5,
              label=_(u"at position:"), name=u'staticText5', parent=self,
              pos=wx.Point(544, 272), style=0)
        self.staticText5.Enable(False)

        self.mod_length_position = wx.SpinCtrl(id=wxID_MAINPANELMOD_LENGTH_POSITION,
              initial=0, max=256, min=-256, name=u'mod_length_position',
              parent=self, pos=wx.Point(608, 264), size=wx.Size(50, -1),
              style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.mod_length_position.SetValue(0)
        self.mod_length_position.SetToolTipString(_(u"Position to add padding (0 = first character)."))
        self.mod_length_position.Enable(False)
        self.mod_length_position.Bind(wx.EVT_TEXT_ENTER, main.showPreview,
              id=wxID_MAINPANELMOD_LENGTH_POSITION)
        self.mod_length_position.Bind(wx.EVT_SPINCTRL, main.showPreview,
              id=wxID_MAINPANELMOD_LENGTH_POSITION)

        self.repl_move = wx.RadioButton(id=wxID_MAINPANELREPL_MOVE,
              label=_(u"Move:"), name=u'repl_move', parent=self,
              pos=wx.Point(32, 208), style=0)
        self.repl_move.SetValue(False)
        self.repl_move.Enable(False)
        self.repl_move.SetToolTipString(_(u"Move first search match to specified position."))
        self.repl_move.Bind(wx.EVT_RADIOBUTTON, self.ActivateReplaceOptions,
              id=wxID_MAINPANELREPL_MOVE)

        self.repl_move_pos = wx.RadioButton(id=wxID_MAINPANELREPL_MOVE_POS,
              label=_(u"to position:"), name=u'repl_move_pos', parent=self,
              pos=wx.Point(104, 208), style=wx.RB_GROUP)
        self.repl_move_pos.SetValue(False)
        self.repl_move_pos.Enable(False)
        self.repl_move_pos.Bind(wx.EVT_RADIOBUTTON, self.ActivateReplaceOptions,
              id=wxID_MAINPANELREPL_MOVE_POS)

        self.repl_move_pos_value = wx.SpinCtrl(id=wxID_MAINPANELREPL_MOVE_POS_VALUE,
              initial=0, max=255, min=-255, name=u'repl_move_pos_value',
              parent=self, pos=wx.Point(184, 208), size=wx.Size(50, -1),
              style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.repl_move_pos_value.SetValue(0)
        self.repl_move_pos_value.SetToolTipString(_(u"Use negative values to start from end of name."))
        self.repl_move_pos_value.Enable(False)
        self.repl_move_pos_value.Bind(wx.EVT_TEXT_ENTER, main.showPreview,
              id=wxID_MAINPANELREPL_MOVE_POS_VALUE)
        self.repl_move_pos_value.Bind(wx.EVT_SPINCTRL, main.showPreview,
              id=wxID_MAINPANELREPL_MOVE_POS_VALUE)


        self.repl_move_txt = wx.RadioButton(id=wxID_MAINPANELREPL_MOVE_TXT,
              label=_(u"to"), name=u'repl_move_txt', parent=self,
              pos=wx.Point(248, 216), style=0)
        self.repl_move_txt.SetValue(True)
        self.repl_move_txt.Enable(False)
        self.repl_move_txt.Bind(wx.EVT_RADIOBUTTON, self.ActivateReplaceOptions,
              id=wxID_MAINPANELREPL_MOVE_TXT)

        self.repl_move_txt_value = wx.TextCtrl(id=wxID_MAINPANELREPL_MOVE_TXT_VALUE,
              name=u'repl_move_txt_value', parent=self, pos=wx.Point(424, 208),
              style=0, value='')
        self.repl_move_txt_value.Enable(False)
        self.repl_move_txt_value.Bind(wx.EVT_TEXT, main.showPreview,
              id=wxID_MAINPANELREPL_MOVE_TXT_VALUE)

        self.repl_move_txt_mod = wx.Choice(choices=[_(u"before"), _(u"after"),
              _(u"replace")], id=wxID_MAINPANELREPL_MOVE_TXT_MOD,
              name=u'repl_move_txt_mod', parent=self, pos=wx.Point(288, 208),
              style=0)
        self.repl_move_txt_mod.SetSelection(0)
        self.repl_move_txt_mod.Enable(False)
        self.repl_move_txt_mod.Bind(wx.EVT_CHOICE, main.showPreview,
              id=wxID_MAINPANELREPL_MOVE_TXT_MOD)

        self.staticText6 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT6,
              label=_(u"text:"), name=u'staticText6', parent=self,
              pos=wx.Point(376, 216), style=0)
        self.staticText6.Enable(False)

        self.repl_move_txt_re = wx.CheckBox(id=wxID_MAINPANELREPL_MOVE_TXT_RE,
              label=_(u"Reg-Expr"), name=u'repl_move_txt_re', parent=self,
              pos=wx.Point(552, 216), style=0)
        self.repl_move_txt_re.SetValue(False)
        self.repl_move_txt_re.SetToolTipString(_(u"Evaluate text as regular expression."))
        self.repl_move_txt_re.Enable(False)
        self.repl_move_txt_re.Bind(wx.EVT_CHECKBOX, main.showPreview,
              id=wxID_MAINPANELREPL_MOVE_TXT_RE)

        self.apply_to_name = wx.CheckBox(id=wxID_MAINPANELAPPLY_TO_NAME,
              label=_(u"Name"), name=u'apply_to_name', parent=self,
              pos=wx.Point(88, 48), style=0)
        self.apply_to_name.SetValue(True)
        self.apply_to_name.SetToolTipString(_(u"All operations act on file or folder name."))
        self.apply_to_name.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.apply_to_ext = wx.CheckBox(id=wxID_MAINPANELAPPLY_TO_EXT,
              label=_(u"Extension"), name=u'apply_to_ext', parent=self,
              pos=wx.Point(88, 64), style=0)
        self.apply_to_ext.SetValue(False)
        self.apply_to_ext.SetToolTipString(_(u"All operations act on file extension."))
        self.apply_to_ext.Bind(wx.EVT_CHECKBOX, main.showPreview)

        self.staticText7 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT7,
              label=_(u"Operations\nact on:"), name=u'staticText7', parent=self,
              pos=wx.Point(16, 56), style=0)

        self.staticLine2 = wx.StaticLine(id=wxID_MAINPANELSTATICLINE2,
              name=u'staticLine2', parent=self, pos=wx.Point(178, 55),
              size=wx.Size(3, 30), style=wx.LI_VERTICAL)

        self.staticText8 = wx.StaticText(id=wxID_MAINPANELSTATICTEXT8,
              label=_(u"characters"), name=u'staticText8', parent=self,
              pos=wx.Point(280, 272), style=0)
        self.staticText8.Enable(False)

    def __init__(self, parent, main_window):
        global main
        main = main_window
        self._init_ctrls(parent)
        self.sizer()
        self.selected_text_box = ''


################## MAIN CHECKBOXES: ############################################
    # activates/disativates SubDir text control:
    def OnSubDirCheckbox(self, event):
        global main_pos
        if self.SubDir.GetValue():
            self.SubDir_txt.Enable(True)
            self.selected_text_box = self.SubDir_txt
            main_pos[0] = True
        else:
            self.SubDir_txt.Enable(False)
            self.selected_text_box = ''
            main_pos[0] = False
        main.showPreview(event)

    # activates/disativates prefix text control:
    def OnPrefixCheckbox(self, event):
        global main_pos
        if self.prefix.GetValue():
            self.prefix_txt.Enable(True)
            self.selected_text_box = self.prefix_txt
            main_pos[1] = True
        else:
            self.prefix_txt.Enable(False)
            self.selected_text_box = ''
            main_pos[1] = False
        main.showPreview(event)

    # activates/disativates suffix text control:
    def OnSuffixCheckbox(self, event):
        global main_pos
        if self.suffix.GetValue():
            self.suffix_txt.Enable(True)
            self.selected_text_box = self.suffix_txt
            main_pos[2] = True
        else:
            self.suffix_txt.Enable(False)
            self.selected_text_box = ''
            main_pos[2] = False
        main.showPreview(event)

    # activates/disativates main replacement options
    # (the radio buttons)
    def OnReplaceCheckbox(self, event):
        global main_pos
        replace_tup = (self.repl_textButton,self.reg_expr,
            self.repl_posButton, self.repl_replace, self.repl_operation,
            self.repl_txt, self.repl_move)
        if self.replace.GetValue():
            for option in replace_tup:
                option.Enable(True)
            self.selected_text_box = self.repl_txt
            main_pos[3] = True
        else:
            for option in replace_tup:
                option.Enable(False)
            self.selected_text_box = ''
            main_pos[3] = False
        self.ActivateReplaceOptions(event)

    # activates/disativates main insertion options:
    def OnInsertCheckbox(self, event):
        global main_pos
        self.selected_text_box
        insert_tup = (self.insert_txt, self.insert_position,
        self.insert_repetition)
        if self.insert.GetValue():
            for option in insert_tup:
                option.Enable(True)
            self.ActivateInsertOptions(event)
            self.selected_text_box = self.insert_txt
            main_pos[4] = True
        else:
            for option in insert_tup:
                option.Enable(False)
            self.ActivateInsertOptions(event)
            self.selected_text_box = ''
            main_pos[4] = False
        main.showPreview(event)

    # activates/disativates length modification options:
    def Mod_length_options(self, event):
        mod_length_tup = (self.mod_length_type, self.staticText2,
         self.staticText8, self.mod_length, self.staticText4,
         self.mod_length_direction)
        enabled = self.mod_length_chbox.GetValue()
        type = self.mod_length_type.GetSelection()
        global main_pos
        if enabled:
            main_pos[5] = True
            for option in mod_length_tup:
                option.Enable(True)
        else:
            main_pos[5] = False
            for option in mod_length_tup:
                option.Enable(False)
        #enable/disabled padding options:
        padding = (self.mod_length_pad, self.staticText3, self.staticText5,
          self.mod_length_position)
        if (type == 1 or type == 2) and enabled:
            for option in padding:
                option.Enable(True)
        else:
            for option in padding:
                option.Enable(False)
        main.showPreview(event)

################## ACTIVATE INSERT OPTIONS: ###################################
    def ActivateInsertOptions(self, event):
            if self.insert_position.GetValue() and self.insert.GetValue():
                self.insert_position_value.Enable(True)
            else:
                self.insert_position_value.Enable(False)

            if self.insert_repetition.GetValue() and self.insert.GetValue():
                self.insert_repetion_value.Enable(True)
                self.insert_char_txt.Enable(True)
            else:
                self.insert_repetion_value.Enable(False)
                self.insert_char_txt.Enable(False)
            main.showPreview(event)


################## ACTIVATE REPLACE (FIND) OPTIONS: ############################
    def ActivateReplaceOptions(self, event):
        # find text field and case insensitive chekbox:
        repl_text_tup = (self.repl_find,self.repl_case)
        if self.repl_textButton.GetValue() and self.replace.GetValue():
            for option in repl_text_tup:
                option.Enable(True)
        else:
            for option in repl_text_tup:
                option.Enable(False)
        # regular expression widgets:
        reg_exp_tup = (self.reg_exp_text, self.reg_exp_i, self.reg_exp_u,
          self.a_z,self.inverse,self.digit,self.char_sets)
        if self.replace.GetValue() and self.reg_expr.GetValue():
            for option in reg_exp_tup:
                option.Enable(True)
        else:
            for option in reg_exp_tup:
                option.Enable(False)
        # positioning widgets
        repl_pos_tup = (self.repl_txt_from,self.repl_from,
            self.repl_txt_to,self.repl_to,self.repl_end,self.repl_front)
        if self.repl_posButton.GetValue() and self.replace.GetValue():
            for option in repl_pos_tup:
                option.Enable(True)
        else:
            for option in repl_pos_tup:
                option.Enable(False)
        # replace with radio:
        if self.repl_replace.GetValue() and self.replace.GetValue():
            self.repl_txt.Enable(True)
        else:
            self.repl_txt.Enable(False)
        #opeation radio:
        if self.repl_operation.GetValue() and self.replace.GetValue():
            self.repl_operation_value.Enable(True)
        else:
            self.repl_operation_value.Enable(False)
        #move radio:
        repl_move_tuple = (self.repl_move_pos, self.repl_move_txt,
          self.repl_move_pos_value, self.repl_move_txt_mod, self.staticText6,
          self.repl_move_txt_value, self.repl_move_txt_re)
        if self.repl_move.GetValue() and self.replace.GetValue():
            for option in repl_move_tuple[0:2]: option.Enable(True)
            if repl_move_tuple[0].GetValue():
                repl_move_tuple[2].Enable(True)
                for widget in repl_move_tuple[3:]:
                    widget.Enable(False)
            else:
                repl_move_tuple[2].Enable(False)
                for widget in repl_move_tuple[3:]:
                    widget.Enable(True)
        else:
            for option in repl_move_tuple:
                option.Enable(False)
        main.showPreview(event)

################## INSERTION BUTTONS: ##########################################
    def insertText(self,value):
        if self.selected_text_box:
            main.setStatusMsg("",u'eyes')
            value = u":" + value + u":"
            self.selected_text_box.WriteText(value)
            self.selected_text_box.SetFocus()

    def OnIns_numButton(self, event):
        self.insertText(_(u"numb"))

    def OnIns_dateButton(self, event):
        self.insertText(_(u"date"))

    def OnIns_timeButton(self, event):
        self.insertText(_(u"time"))

    def OnId3Button(self, event):
        self.insertText(self.id3_select.GetStringSelection())

    def OnIns_dirButton(self, event):
        if self.selected_text_box == self.SubDir_txt:
            main.setStatusMsg("",u"eyes")
            self.selected_text_box.WriteText(u":/")
            self.selected_text_box.SetFocus()

################### TEXT BOX SELECTORS #########################################
    def OnPrefix_txtLeftDown(self, event):
        self.selected_text_box = self.prefix_txt
        event.Skip()

    def OnSuffix_txtLeftDown(self, event):
        self.selected_text_box = self.suffix_txt
        event.Skip()

    def OnInsert_txtLeftDown(self, event):
        self.selected_text_box = self.insert_txt
        event.Skip()

    def OnReplace_txtLeftDown(self, event):
        self.selected_text_box = self.repl_txt
        event.Skip()

    def OnRepl_findLeftDown(self, event):
        self.selected_text_box = ''
        event.Skip()

    def OnReg_exp_textLeftDown(self, event):
        self.selected_text_box = ''
        event.Skip()

    def OnExtension_txtLeftDown(self, event):
        self.selected_text_box = self.extension_txt
        event.Skip()

    def OnSubDir_txtLeftDown(self, event):
        self.selected_text_box = self.SubDir_txt
        event.Skip()

    def setCorrectSearchPosition(self, event):
        result = self.repl_to.GetValue() - 1
        if self.repl_end.GetValue():
            self.repl_from.SetValue(result)
        main.showPreview(event)

###### RETURN NEEDED VALUES TO MAIN APP: #######################################
    def GetReNamePosition(self):
        return main_pos


###### GET/SET CONFIGURATION SETTINGS: #########################################
    def getSettings(self):
        settings = (u"<[main]>",
          # apply to:
          u"apply_to_name>:>%s" %int(self.apply_to_name.GetValue()),
          u"apply_to_ext>:>%s" %int(self.apply_to_ext.GetValue()),
          #directory:
          u"SubDir>:>%s" %int(self.SubDir.GetValue()),
          u"SubDir_txt>:>%s" %self.SubDir_txt.GetValue(),
          #prefix:
          u"prefix>:>%s" %int(self.prefix.GetValue()),
          u"prefix_txt>:>%s" %self.prefix_txt.GetValue(),
          #suffix:
          u"suffix>:>%s" %int(self.suffix.GetValue()),
          u"suffix_txt>:>%s" %self.suffix_txt.GetValue(),
          #replace/modify/move:
          u"replace>:>%s" %int(self.replace.GetValue()),
          u"repl_textButton>:>%s" %int(self.repl_textButton.GetValue()),
          u"repl_find>:>%s" %self.repl_find.GetValue(),
          u"repl_case>:>%s" %int(self.repl_case.GetValue()),
          u"reg_expr>:>%s" %int(self.reg_expr.GetValue()),
          u"inverse>:>%s" %int(self.inverse.GetValue()),
          u"a_z>:>%s" %int(self.a_z.GetValue()),
          u"digit>:>%s" %int(self.digit.GetValue()),
          u"reg_exp_text>:>%s" %self.reg_exp_text.GetValue(),
          u"reg_exp_i>:>%s" %int(self.reg_exp_i.GetValue()),
          u"reg_exp_u>:>%s" %int(self.reg_exp_u.GetValue()),
          u"repl_posButton>:>%s" %int(self.repl_posButton.GetValue()),
          u"repl_from>:>%s" %self.repl_from.GetValue(),
          u"repl_to>:>%s" %self.repl_to.GetValue(),
          u"repl_front>:>%s" %int(self.repl_front.GetValue()),
          u"repl_end>:>%s" %int(self.repl_end.GetValue()),
          u"repl_replace>:>%s" %int(self.repl_replace.GetValue()),
          u"repl_txt>:>%s" %self.repl_txt.GetValue(),
          u"repl_operation>:>%s" %int(self.repl_operation.GetValue()),
          u"repl_operation_value>:>%s" %self.repl_operation_value.GetSelection(),
          u"repl_move>:>%s" %int(self.repl_move.GetValue()),
          u"repl_move_pos>:>%s" %int(self.repl_move_pos.GetValue()),
          u"repl_move_txt>:>%s" %int(self.repl_move_txt.GetValue()),
          u"repl_move_pos_value>:>%s" %self.repl_move_pos_value.GetValue(),
          u"repl_move_txt_mod>:>%s" %self.repl_move_txt_mod.GetSelection(),
          u"repl_move_txt_value>:>%s" %self.repl_move_txt_value.GetValue(),
          u"repl_move_txt_re>:>%s" %int(self.repl_move_txt_re.GetValue()),
          #insertion:
          u"insert>:>%s" %int(self.insert.GetValue()),
          u"insert_position>:>%s" %int(self.insert_position.GetValue()),
          u"insert_position_value>:>%s" %self.insert_position_value.GetValue(),
          u"insert_repetition>:>%s" %int(self.insert_repetition.GetValue()),
          u"insert_repetion_value>:>%s" %self.insert_repetion_value.GetValue(),
          u"insert_txt>:>%s" %self.insert_txt.GetValue(),
          #length modification:
          u"mod_length_chbox>:>%s" %int(self.mod_length_chbox.GetValue()),
          u"mod_length_type>:>%s" %self.mod_length_type.GetSelection(),
          u"mod_length>:>%s" %self.mod_length.GetValue(),
          u"mod_length_direction>:>%s" %self.mod_length_direction.GetSelection(),
          u"mod_length_pad>:>%s" %self.mod_length_pad.GetValue(),
          u"mod_length_position>:>%s" %self.mod_length_position.GetValue(),
          # buttons
          u"id3_select>:>%s" %self.id3_select.GetSelection(),
          )
        return settings

    def setSettings(self,settings):
        if len(settings) == 48: #make sure number of settings is correct
            try:
                # apply to:
                self.apply_to_name.SetValue(int(settings[0]))
                self.apply_to_ext.SetValue(int(settings[1]))
                #directory:
                self.SubDir.SetValue(int(settings[2]))
                self.SubDir_txt.SetValue(settings[3])
                #prefix:
                self.prefix.SetValue(int(settings[4]))
                self.prefix_txt.SetValue(settings[5])
                #suffix
                self.suffix.SetValue(int(settings[6]))
                self.suffix_txt.SetValue(settings[7])
                #replace/modify/move:
                self.replace.SetValue(int(settings[8]))
                self.repl_textButton.SetValue(int(settings[9]))
                self.repl_find.SetValue(settings[10])
                self.repl_case.SetValue(int(settings[11]))
                self.reg_expr.SetValue(int(settings[12]))
                self.inverse.SetValue(int(settings[13]))
                self.a_z.SetValue(int(settings[14]))
                self.digit.SetValue(int(settings[15]))
                self.reg_exp_text.SetValue(settings[16])
                self.reg_exp_i.SetValue(int(settings[17]))
                self.reg_exp_u.SetValue(int(settings[18]))
                self.repl_posButton.SetValue(int(settings[19]))
                self.repl_from.SetValue(int(settings[20]))
                self.repl_to.SetValue(int(settings[21]))
                self.repl_front.SetValue(int(settings[22]))
                self.repl_end.SetValue(int(settings[23]))
                self.repl_replace.SetValue(int(settings[24]))
                self.repl_txt.SetValue(settings[25])
                self.repl_operation.SetValue(int(settings[26]))
                self.repl_operation_value.SetSelection(int(settings[27]))
                self.repl_move.SetValue(int(settings[28])),
                self.repl_move_pos.SetValue(int(settings[29]))
                self.repl_move_txt.SetValue(int(settings[30]))
                self.repl_move_pos_value.SetValue(int(settings[31]))
                self.repl_move_txt_mod.SetSelection(int(settings[32]))
                self.repl_move_txt_value.SetValue(settings[33])
                self.repl_move_txt_re.SetValue(int(settings[34]))
                #insertion:
                self.insert.SetValue(int(settings[35]))
                self.insert_position.SetValue(int(settings[36]))
                self.insert_position_value.SetValue(int(settings[37]))
                self.insert_repetition.SetValue(int(settings[38]))
                self.insert_repetion_value.SetValue(int(settings[39]))
                self.insert_txt.SetValue(settings[40])
                #length modification:
                self.mod_length_chbox.SetValue(int(settings[41]))
                self.mod_length_type.SetSelection(int(settings[42]))
                self.mod_length.SetValue(int(settings[43]))
                self.mod_length_direction.SetSelection(int(settings[44]))
                self.mod_length_pad.SetValue(settings[45])
                self.mod_length_position.SetValue(int(settings[46]))
                # buttons:
                self.id3_select.SetSelection(int(settings[47].replace('\n','')))
            except ValueError:
                return False
            else:
                self.OnSubDirCheckbox(False)
                self.OnPrefixCheckbox(False)
                self.OnSuffixCheckbox(False)
                self.OnReplaceCheckbox(False)
                self.OnInsertCheckbox(False)
                self.Mod_length_options(False)
                return True
        else:
            return False


