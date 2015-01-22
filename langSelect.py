# -*- coding: utf-8 -*-
#Boa:Dialog:langSelect

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

def create(parent, Title, event):
    return langSelect(parent, Title, event)

languages = (
    ('ar', u'العربية', 'sa'),
    #('ca', u'Català', 'es_ct'),
    #('da', u'Dansk', 'dk'),
    ('de', u'Deutsch', 'de'),
    ('el', u'Ελληνικά', 'gr'),
    ('en_US', u'US English', 'us'),
    ('es', u'Español', 'es'),
    ('fr', u'Français', 'fr'),
    #('he', u'עברית', 'il'),
    #('hi', u'हिन्दी', 'in'),
    ('hu', u'Magyar', 'hu'),
    ('it', u'Italiano', 'it'),
    ('ja', u'日本語', 'jp'),
    ('ko', u'한국어', 'kr'),
    ('nl', u'Nederlands', 'nl'),
    ('pl', u'Polski', 'pl'),
    ('pt_BR', u'Português do Brasil', 'br'),
    ('tr', u'Türkçe', 'tr'),
    ('ru', u'Русский', 'ru'),
    ('sk', u'Slovenčina', 'si'),
    ('sv', u'Svenska', 'se'),
    ('zh_CN', u'中文', 'cn'),
)


class langSelect(wx.Dialog):
    def Sizer(self):
        optionsSizer = wx.FlexGridSizer(cols=4, hgap=10, vgap=10)

        # add languages to sizer
        for lang_info in languages:
            lang_flag = getattr(self, '%s_flag'%lang_info[0])
            lang_select = getattr(self, lang_info[0])
            optionsSizer.Add(lang_flag,0, wx.ALIGN_CENTRE|wx.RIGHT, 5)
            optionsSizer.Add(lang_select)

        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.AddSpacer((10,10))
        buttonsSizer.Add(self.ok,0,wx.RIGHT|wx.LEFT,5)
        buttonsSizer.Add(self.cancel,0,wx.RIGHT,5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(optionsSizer,0,wx.ALIGN_CENTRE|wx.ALL,10)
        sizer.Add(buttonsSizer,0,wx.BOTTOM|wx.TOP,5)

        self.SetSizerAndFit(sizer)

    def _init_ctrls(self, prnt, Title):
        wx.Dialog.__init__(self, id=-1, name=u'langSelect',
              parent=prnt, size=wx.Size(281, 292),
              style=wx.DEFAULT_DIALOG_STYLE, title=Title)
        self.SetIcon(wx.Icon(prnt.realPath(u'icons/metamorphose.ico'), wx.BITMAP_TYPE_ICO))
        
        def getBitmap(lang):
            return wx.Bitmap(prnt.realPath(u'icons/flags/%s.png'%lang), wx.BITMAP_TYPE_PNG)

        # add languages selection to interface
        for lang_info in languages:
            lang = lang_info[0]
            setattr(self, lang, wx.RadioButton(id=-1, label=lang_info[1],
                                name=lang, parent=self, style=0))
            getattr(self, lang).SetToolTipString(u"%s (%s)"%(lang_info[1], lang))
            setattr(self, '%s_flag'%lang, wx.StaticBitmap(parent=self, id=-1,
                                          bitmap=getBitmap(lang_info[2])))

        self.ok = wx.Button(id=wx.ID_OK, name=u'ok',
              parent=self, pos=wx.Point(20, 300), style=0)

        self.cancel = wx.Button(id=wx.ID_CANCEL, name=u'cancel',
              parent=self, pos=wx.Point(120, 300), style=0)

    def __init__(self, parent, Title, event):
        self._init_ctrls(parent, Title)
        self.Sizer()
        if event:
            self.FindWindowByName(event).SetValue(True)
        else:
            self.en_US.SetValue(True)
            self.cancel.Show(False)
        
    def GetLanguage(self):
        notLangs = ('staticBitmap', 'ok', 'cancel')
        for child in self.GetChildren():
            name = child.GetName()
            if name not in notLangs:
                if child.GetValue():
                    return name
