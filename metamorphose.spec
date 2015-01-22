Name:           metamorphose
Version:        1.1.1 
Release:        1%{?dist}
Summary:        A cross platform file and folder mass renamer
Summary(fr):    Un renommeur massif pour fichiers et dossiers

Group:          Applications/File
License:        GPLv3
URL:            http://sourceforge.net/projects/file-folder-ren/
Source0:        http://downloads.sourceforge.net/file-folder-ren/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python desktop-file-utils gettext
Requires:       wxPython wxGTK

%description
A cross platform file and folder mass renamer, allows many different 
renaming operations in a GUI. Features include search and replace (with RE), 
insert, numbering, date/time, id3 & EXIF tag read, change length, get all 
files in sub-dirs, undo/redo, etc.

%prep
%setup -q -n %{name}-%{version}

iconv -f ISO-8859-1 -t UTF-8 -o metamorphose.1.temp metamorphose.1  
mv metamorphose.1.temp metamorphose.1 

sed -i -e 's|Version=1.0.6||' %{name}.desktop
chmod +x EXIF.py

%build


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} build DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/man/man1/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_bindir}

sed -i -e 's/\r$//'  readme_en.html
sed -i -e 's/\r$//'  readme_fr.html
sed -i -e 's/\r$//'  readme_pl.html
sed -i -e 's/\r$//'  translations.html

make install DESTDIR=$RPM_BUILD_ROOT

#chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/generate_pot.sh

desktop-file-install --vendor="fedora"                              \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications/              \
        metamorphose.desktop

rm -rf $RPM_BUILD_ROOT%{_datadir}/applications/metamorphose.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/fedora-metamorphose.desktop
%{_bindir}/%{name}

%changelog
* Mon May 05 2008 Pingou <pingoufc4@yahoo.fr> 1.1.1-1
- Update to version 1.1.1

* Fri Oct 19 2007 Pingou <pingoufc4@yahoo.fr> 1.1.0-1
- Update to version 1.1.0

* Mon Oct 08 2007 Pingou <pingoufc4@yahoo.fr> 1.0.6-1
- Update to version 1.0.6

* Mon Jul 30 2007  Pingou <pingoufc4@yahoo.fr> 1.0.5-4
- Add the desktop install section

* Thu Jul 12 2007  Pingou <pingoufc4@yahoo.fr> 1.0.5-3
- Changse in the requires

* Wed Jul 11 2007  Pingou <pingoufc4@yahoo.fr> 1.0.5-2
- Add the BR
- Changes in the file section to avoid the conflicts

* Wed Jul 11 2007  Pingou <pingoufc4@yahoo.fr> 1.0.5-1
- initial package for Fedora

