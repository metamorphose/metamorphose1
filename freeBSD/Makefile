# New ports collection makefile for:   metamorphose
# Date created:        28 September 2007
# Whom:                javier
#
# $FreeBSD$
#

PORTNAME=	metamorphose
PORTVERSION=	1.1
CATEGORIES=	sysutils
MASTER_SITES=	${MASTER_SITE_SOURCEFORGE}
MASTER_SITE_SUBDIR=	file-folder-ren
DISTNAME=	metamorphose_1.1.1

MAINTAINER=	javpra@FreeBSD.org
COMMENT=	A program to rename files and folders

RUN_DEPENDS=	python:${PORTSDIR}/lang/python24 wxgtk2-unicode:${PORTSDIR}/x11-toolkits/wxgtk26-unicode

USE_GMAKE=	YES
USE_GETTEXT=	YES
MANCOMPRESSED=	YES
USE_PYTHON=	2.4-2.5
USE_WX=	2.6
WITH_UNICODE=	YES
WX_COMPS=	python
WX_UNICODE=	YES

NO_INSTALL_MANPAGES=	YES

.include <bsd.port.pre.mk>

.if ((${OSVERSION} < 500000))
IGNORE=	systems prior to FreeBSD 5.0 do not support Unicode
.endif

.if defined (WITHOUT_NLS)
USE_GETTEXT=	NO
.endif

.include <bsd.port.post.mk>
