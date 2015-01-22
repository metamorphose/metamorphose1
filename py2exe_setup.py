# -*- coding: 1252 -*-

#  Here we have the py2exe setup file
#
#  Call this file with py2exe to compile for the Windows platform.

"""
Copyright (c) 2005-2008 Ianaré Sévi <ianare@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


This applies to this file only, Métamorphose itself is licensed under GPLv3
"""

from distutils.core import setup
import py2exe
import os , glob
import sys

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources:
        self.version = "1.1.2"
        self.company_name = "Ianaré Sévi"
        self.copyright = "(c) 2005-2009 Ianaré Sévi"
        #self.name = "Métamorphose File -n- Folder renamer"


# The manifest will be inserted as resource into the exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24


Metamorphose = Target(
    description = "Métamorphose: a file n folder renamer",
    icon_resources = [(1, "icons/metamorphose.ico")],
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="Metamorphose"))],
    #options = {"py2exe": {"packages": ["encodings","_gdi_"]}}
    script = "metamorphose.py",
    )


files = [("icons",glob.glob("icons/*.*")),
         ("icons/flags",glob.glob("icons/flags/*.*")),
         ("configs",glob.glob("configs/*.cfg")),
         ("",glob.glob("*.html")),
		 ("",("version",)),
        ]

langPath = os.path.abspath("messages")
for lang in os.listdir(langPath):
    if '.' not in lang:
        files.append(("messages/%s/LC_MESSAGES"%lang,["messages/%s/LC_MESSAGES/metamorphose.mo"%lang]))

docPath = os.path.abspath("docs")
for lang in os.listdir(docPath):
    if '.' not in lang:
        files.append(("docs/%s"%lang,glob.glob(u"docs/%s/*.*"%lang)))
        if os.path.exists(os.path.join(docPath,lang,'images')):
            files.append(("docs/%s/images"%lang,glob.glob(u"docs/%s/images/*.*"%lang)))
#print files
#sys.exit()

setup(
    data_files = files,

    # don't compress, use NSIS for that
    options = {"py2exe": {"optimize": 2,
                          #"dist_dir": "dir/goes/here",
                          "bundle_files": 3,
                          "excludes": "_ssl, _socket, bz2",
                }},

    zipfile = None,
    windows = [Metamorphose],
    )
