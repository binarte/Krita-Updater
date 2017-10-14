#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Licensed by the terms of the MIT license, read the LICENSE file for details
# Licenciado pelos termos da licença MIT, leia o arquivo LICENSE para detalhes
# Licenciado por los termos de la licencia MIT, lea el archivo LICENSE para más detalles
#
# Refer to the README file for usage information
# Consulte o arquivo LEIAME para informações de uso
#

import sys
import os.path
import os
import stat
import urllib2
import re
import subprocess
import locale
from distutils.version import LooseVersion, StrictVersion
from subprocess import call
from os import listdir
from os.path import isfile, join

repoStable = "https://download.kde.org/stable/krita/"
repoUnstable = "https://download.kde.org/unstable/krita/"
priority = ["STABLE","rc","beta","alpha","prealpha"]

localdir = os.path.dirname(sys.argv[0]);
files = [f for f in listdir(localdir) if isfile(join(localdir, f))]
locale = locale.getdefaultlocale()[0]
language = locale.split("_")[0]

versions = {}
bestVersions = {}
bestVersions["STABLE"] = "0.0.0"

#get the appropriate string for the locale
def loc(strings, fallback):
	if locale in strings:
		return strings[locale]
	if language in strings:
		return strings[language]
	return fallback

#find the versions present in a repository
def findVersions(url):
	data = urllib2.urlopen(url).read()
	
	rversions = []

	for m in re.finditer(r"<tr.*?>\s*(.*?)\s*</tr>", data):
		trdata = m.group(1);
		vals =[]
		for m in re.finditer(r"<td.*?>\s*(.*?)\s*</td>",trdata):
			vals.append(m.group(1))
		if len(vals) and vals[3] == "-":
			href = re.search(r"href=\"(.*?)\"", vals[1])
			path = href.group(1)
			if path[0] != '/':
				rversions.append (path.strip("/"))
	return rversions

#create command and run krita
def runKrita(location):
	st = os.stat(location)
	os.chmod(location, st.st_mode | stat.S_IEXEC)
	cmd = [location]
	i = 2
	while i < len(sys.argv):
		cmd.append(sys.argv[i])
		i = i+1
	subprocess.Popen(cmd);

def showMsg(message):
	print(message)
	call(["notify-send", message]);

#find out which versions are currently available
for fname in files:
	fmatch = re.match(r"^krita-([0-9]*(\.[0-9]*)*)(-(.*?)[0-9]*)?-x86_64.appimage$",fname)
	if fmatch:
		vnum = fmatch.group(1)
		vtype = "STABLE"		
		if fmatch.group(4):
			vtype = fmatch.group(4).replace("-","")		
		
		if vtype not in versions:
			versions[vtype] = {}
			bestVersions[vtype] = "0.0.0"
			
		if LooseVersion(bestVersions[vtype]) < vnum:
			bestVersions[vtype] = vnum
		
		versions[vtype][vnum] = fname
		
#show the latest versions available
for i in bestVersions.iterkeys():
	print (loc({
	 "pt":"Versão " + i + " mais recente disponível: " + bestVersions[i],
	 "es":"Versión " + i + " más reciente disponible: " + bestVersions[i]	
	},"Latest " + i + " version available: " + bestVersions[i]))

#run the program before updating
exectype = "STABLE"
runLater = 0
if len (sys.argv) > 1:
	exectype = sys.argv[1]
if exectype != "norun":

	vnum = bestVersions[exectype]	
	i = 0
	
	#switch to a more stable version if possible
	while i < len(priority):
		ptype = priority[i]
		if ptype == exectype:
			break;
		if ptype in bestVersions and LooseVersion(vnum) <= bestVersions[ptype]:
			vnum = bestVersions[ptype]
			exectype = ptype;
			i = 0
		else:
			i = i+1
	if  vnum == '0.0.0':
		showMsg(loc({
		 "pt":"Krita não encontrado, procurando pela mais nova versão.",
		 "es":"Krita no se encuentra, buscando por la versión más nueva."
		},"Krita not Found, searching for the newest version."))
		runLater = 1
	else:
		print(loc({
		 "pt":"Executando versão " + exectype + " " +vnum,
		 "es":"Ejecutando versión " + exectype + " " +vnum
		},"Running " + exectype + " " +vnum + " version"))
		runKrita(join(localdir,versions[exectype][vnum]))

print(loc({
	"pt":"Procurando por novas versões...",
	"es":"Buscando por nuevas versiones...",
	},"Searching for new versions..."))

#check for the latest version
curVersion = bestVersions["STABLE"];
for i in findVersions(repoStable):
	if LooseVersion(curVersion) < LooseVersion(i) :
		curVersion = i

#update if the latest version is newer than the currently most recent
if curVersion != bestVersions["STABLE"]:
	showMsg(loc({
		"pt":"Foi encontrada uma nova versão do Krita: " + curVersion + ", baixando",
		"es":"Se ha encontrado una nueva versión del Krita: " + curVersion + ", bajando"
	},"Found new Krita version: " + curVersion + ", downloading"))
	
	filename = "krita-" + curVersion + "-x86_64.appimage"
	localfile = join(localdir,filename);
	call(["wget", "-cO", localfile + ".download", repoStable + "/" + curVersion + "/" + filename]);
	
	os.rename(localfile + ".download", localfile)
	st = os.stat(localfile)
	os.chmod(localfile, st.st_mode | stat.S_IEXEC)
	
	if runLater:
		print(loc({
		 "pt":"Krita " + curVersion + " obtido, executando.",
		 "es":"Krita " + curVersion + " obtenido, execujando.",
		},"Krita " + curVersion + " obtained, running."))
		runKrita(localfile);
	else:
		showMsg(loc({
		 "pt":"Foi obtido o Krita " + curVersion + ", reinicie o Krita para usá-lo",
		 "es":"Se ha obtido el Krita " + curVersion + ", reinicie Krita para utilizarlo"
		},"Krita " + curVersion + " was obtained, restart Krita to use it"))
else:
	print(loc({
	 "pt":"Nenhuma nova versão encontrada",
	 "es":"Ninguna nueva versión encontrada"
	},"No newer version found"))

print(loc({
	 "pt":"Concluído.",
	 "es":"Concluido."
	},"Done."))
