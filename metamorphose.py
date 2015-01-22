#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:App:BoaApp

#
# This is the control module, it loads the main application.
#
# This is what you should run to start the program.
#

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

--

All translations also copyright (c) Ianaré Sévi, under BSD license.

"""

import sys

# Choose wxPython version if not running as frozen binary
if not hasattr(sys, "frozen"):
    try:
        import wxversion
    except:
        print "\nwxPython is required!\nRefer to 'readme_xx.html'",\
              "for installation instructions.\n"
        sys.exit()
    else:
        try:
            wxversion.select(['2.6', '2.8'])
        except:
            print "wxPython version 2.6 or 2.8 is required.\n"
            sys.exit()
import wx
import os
import platform

modules ={u'DateTime': [0, '', u'DateTime.py'],
 u'PyAlpha': [0, '', u'PyAlpha.py'],
 u'about': [0, u'about box', u'about.py'],
 u'errors': [0, '', u'errors.py'],
 u'examples': [0, '', u'examples.py'],
 u'helpDiag': [0, '', u'helpDiag.py'],
 u'id3reader': [0, '', u'id3reader.py'],
 u'langSelect': [0, '', u'langSelect.py'],
 u'main': [0, '', u'main.py'],
 u'main_window': [1, u'Main frame of Application', u'main_window.py'],
 u'numbering': [0, '', u'numbering.py'],
 u'picker': [0, '', u'picker.py'],
 u'preferences': [0, u'preferences selection', u'preferences.py'],
 u'roman': [0, '', u'roman.py']}

class BoaApp(wx.App):
    def OnInit(self):
        import main_window
        wx.InitAllImageHandlers()
        self.main = main_window.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    if platform.system() == 'Linux':
        try:
            # to fix some KDE display issues:
            del os.environ['GTK_RC_FILES']
            del os.environ['GTK2_RC_FILES']
        except (ValueError, KeyError):
            pass
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    if 'unicode' not in wx.PlatformInfo:
        print "\nInstalled version: %s\nYou need a unicode build of wxPython to run Metamorphose.\n"%wxversion.getInstalled()
    else:
        main()
