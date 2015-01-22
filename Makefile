#
# Makefile tested on Linux and FreeBSD.
# May work with other UNIXes.
#
# Authors : Ianaré Sévi, Javier Prats, Pierre-Yves Chibon
#

# Specify an alternate install root
DESTDIR=

PACKAGE=metamorphose

# Change to 1 to remove all metamorphose user files
remusr=0

OS=`uname -s`

all: build install
 
build:
	# make needed directories
	mkdir -p $(DESTDIR)/usr/share/doc/$(PACKAGE)/;
	mkdir -p $(DESTDIR)/usr/share/$(PACKAGE)/;


remove:
	rm -fR $(DESTDIR)/usr/share/doc/$(PACKAGE);
	rm -fR $(DESTDIR)/usr/share/$(PACKAGE);
	rm -f $(DESTDIR)/usr/bin/$(PACKAGE);
	rm -f $(DESTDIR)/usr/share/man/man1/$(PACKAGE).1.gz;
	
	# delete icon and launcher if folders exist
	if [ -d $(DESTDIR)/usr/share/pixmaps ]; then\
		rm -f $(DESTDIR)/usr/share/pixmaps/$(PACKAGE).png;\
	fi;
	if [ -d $(DESTDIR)/usr/share/applications ] ; then\
		rm -f $(DESTDIR)/usr/share/applications/$(PACKAGE).desktop;\
	fi;
	if [ -d $(DESTDIR)/usr/share/app-install/icons ] ; then\
		rm -f $(DESTDIR)/usr/share/app-install/icons/$(PACKAGE).png;\
    fi;
	if [ -d $(DESTDIR)/usr/share/app-install/desktop ] ; then\
    	rm -f $(DESTDIR)/usr/share/app-install/desktop/$(PACKAGE).desktop;\
    fi;
	
	# delete translation files
	if [ -d /usr/share/locale ] ; then\
		find /usr/share/locale -name $(PACKAGE).mo -delete;\
	fi;\
	
	# delete user files
	if [ ${remusr} = 1 ] ; then\
		find /home/ -depth -name .$(PACKAGE) -exec rm -fR {} \; ;\
		find /root/ -depth -name .$(PACKAGE) -exec rm -fR {} \; ;\
	fi;\


makedirs:
	# Normally these directories are already present on the system,
	# in some cases they need to be created
	mkdir -p $(DESTDIR)/usr/bin
	mkdir -p $(DESTDIR)/usr/share/app-install
	mkdir -p $(DESTDIR)/usr/share/pixmaps
	mkdir -p $(DESTDIR)/usr/share/applications
	mkdir -p $(DESTDIR)/usr/share/app-install/icons
	mkdir -p $(DESTDIR)/usr/share/app-install/desktop
	mkdir -p $(DESTDIR)/usr/share/locale
	mkdir -p $(DESTDIR)/usr/share/man/man1


clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*~" -exec rm -f {} \;


install: install-doc
	# make sure all permissions are correct
	chmod -R a+r *;
	find . -type d ! -regex '.*/\..*' -exec chmod 755 {} \;

	# copy program files and libraries
	cp -p *.py $(DESTDIR)/usr/share/$(PACKAGE)/;
	cp -pR docs $(DESTDIR)/usr/share/$(PACKAGE)/;
	cp -pR configs $(DESTDIR)/usr/share/$(PACKAGE)/;
	cp -pR icons $(DESTDIR)/usr/share/$(PACKAGE)/;
	cp -p version $(DESTDIR)/usr/share/$(PACKAGE)/;
	
	# install translation files
	if [ ${OS} = "Linux" ]; then\
		for lang in `ls -1 messages`; do\
			if [ -d messages/$${lang} ]; then\
				mkdir -p $(DESTDIR)/usr/share/locale/$${lang}/LC_MESSAGES;\
				cp -p messages/$${lang}/LC_MESSAGES/$(PACKAGE).mo $(DESTDIR)/usr/share/locale/$${lang}/LC_MESSAGES/;\
			fi;\
		done;\
	fi;\
	if [ ${OS} != "Linux" ]; then\
		cp -pR messages $(DESTDIR)/usr/share/$(PACKAGE)/;\
	fi;\

	# install the executables
	install -m 755 $(PACKAGE) $(DESTDIR)/usr/bin/;

	# copy icon and launcher if folders exist
	if [ -d $(DESTDIR)/usr/share/pixmaps ]; then\
		install -m 644 icons/metamorphose64.png $(DESTDIR)/usr/share/pixmaps/$(PACKAGE).png;\
	fi;
	if [ -d $(DESTDIR)/usr/share/applications ]; then\
		install -m 644 $(PACKAGE).desktop $(DESTDIR)/usr/share/applications/;\
	fi;
	if [ -d $(DESTDIR)/usr/share/app-install/icons ]; then\
		cp icons/metamorphose64.png $(DESTDIR)/usr/share/app-install/icons/$(PACKAGE).png;\
	fi;
	if [ -d $(DESTDIR)/usr/share/app-install/desktop ]; then\
		install -m 644 $(PACKAGE).desktop $(DESTDIR)/usr/share/app-install/desktop/;\
	fi;


install-doc:
	gzip -c9 $(PACKAGE).1 > $(DESTDIR)/usr/share/man/man1/$(PACKAGE).1.gz;
	cp *.html $(DESTDIR)/usr/share/doc/$(PACKAGE)/;

# EOF
