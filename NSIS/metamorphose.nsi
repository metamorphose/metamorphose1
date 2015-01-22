;Based on :
;Welcome/Finish Page Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI.nsh"

;--------------------------------
;General

  ;Name and file
  !define VERSION "1.1.2"

  Name "Métamorphose"
  OutFile "metamorphose_${VERSION}_setup.exe"
  !define MUI_ICON "metsetup.ico"
  !define MUI_UNICON "metsetup.ico"
  !define MUI_WELCOMEFINISHPAGE_BITMAP "wizard_i.bmp"
  !define MUI_UNWELCOMEFINISHPAGE_BITMAP "wizard_u.bmp"

  ;Get installation folder from registry if available
  InstallDirRegKey HKLM "Software\metamorphose" ""
  
  ;Default installation folder
  InstallDir "$PROGRAMFILES\metamorphose"
  
  VIProductVersion "1.1.2.0"
  VIAddVersionKey "ProductName" "Métamorphose"
  VIAddVersionKey "CompanyName" "Ianaré Sévi"
  VIAddVersionKey "LegalCopyright" "(c) 2005-2007 Ianaré Sévi"
  VIAddVersionKey "FileDescription" "Installer for Métamorphose ${VERSION}"
  VIAddVersionKey "FileVersion" "${VERSION}"

  !define CSIDL_SYSTEM "0x25" ;System path

  XPStyle on
  SetCompressor /SOLID lzma
  
  ;Request application privileges for Windows Vista / 7
  RequestExecutionLevel admin

;--------------------------------
;Variables

  Var MUI_TEMP
  Var STARTMENU_FOLDER
  
;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING
  !define MUI_COMPONENTSPAGE_CHECKBITMAP "checks.bmp"

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "License.rtf"
  !insertmacro MUI_PAGE_COMPONENTS 
  !insertmacro MUI_PAGE_DIRECTORY
  ;Start Menu Folder Page Configuration
  ;!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  ;!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\metamorphose" 
  ;!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER
  
  !insertmacro MUI_PAGE_INSTFILES
  !define MUI_FINISHPAGE_RUN "$INSTDIR\metamorphose.exe"
  !insertmacro MUI_PAGE_FINISH

  ;uninstall
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_COMPONENTS
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Métamorphose" Application

  SectionIn RO
  SetOutPath "$INSTDIR"

  File /r _win_bin\*
  
  ;Install for all users
  SetShellVarContext all

  ;Store installation folder
  WriteRegStr HKCU "Software\metamorphose" "" $INSTDIR
  WriteRegStr HKLM "Software\metamorphose" "version" ${VERSION}

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
   
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Métamorphose.lnk" "$INSTDIR\metamorphose.exe"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

Section "Right-click menu" Shell
  WriteRegStr HKCR "Directory\shell\Rename with Métamorphose" "" ""
  WriteRegStr HKCR "Directory\shell\Rename with Métamorphose\command" "" "$INSTDIR\metamorphose.exe %L"
SectionEnd

Section "Desktop Shortcut" DShortCut
  CreateShortCut "$DESKTOP\Métamorphose.lnk" "$INSTDIR\metamorphose.exe"
SectionEnd

Section /o "Quicklaunch Shortcut" QShortCut
  CreateShortCut "$QUICKLAUNCH\Métamorphose.lnk" "$INSTDIR\metamorphose.exe"
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_Application ${LANG_ENGLISH} "The main application files (required)."
  LangString DESC_Shell ${LANG_ENGLISH} "Add this right-click menu option: 'Rename with Métamorphose'."
  LangString DESC_DShortCut ${LANG_ENGLISH} "Create a Desktop shortcut."
  LangString DESC_QShortCut ${LANG_ENGLISH} "Create a Quickstart shortcut."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Application} $(DESC_Application)
    !insertmacro MUI_DESCRIPTION_TEXT ${Shell} $(DESC_Shell)
    !insertmacro MUI_DESCRIPTION_TEXT ${DShortCut} $(DESC_DShortCut)
    !insertmacro MUI_DESCRIPTION_TEXT ${QShortCut} $(DESC_QShortCut)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END


;--------------------------------
;Uninstaller Section

Section "un.Métamorphose" Uninstall

  SectionIn RO

  Delete "$DESKTOP\Métamorphose.lnk"
  Delete "$QUICKLAUNCH\Métamorphose.lnk"
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $MUI_TEMP
  RMDir /r "$SMPROGRAMS\$MUI_TEMP"
  
  RMDir /r "$INSTDIR"

  DeleteRegKey HKCU "Software\metamorphose"
  DeleteRegKey HKCR "Directory\shell\Rename with Métamorphose"
  DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\metamorphose"

SectionEnd

Section /o "un.User files" UninstallUser

  RMDir /r "$APPDATA\.metamorphose"

SectionEnd

  ;Language strings
  LangString DESC_Uninstall ${LANG_ENGLISH} "The main application files (required)."
  LangString DESC_UninstallUser ${LANG_ENGLISH} "User configuration and history files."

  ;Assign language strings to sections
  !insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Uninstall} $(DESC_Uninstall)
    !insertmacro MUI_DESCRIPTION_TEXT ${UninstallUser} $(DESC_UninstallUser)
  !insertmacro MUI_UNFUNCTION_DESCRIPTION_END
