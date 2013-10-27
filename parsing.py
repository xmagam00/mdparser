#!/usr/bin/env python

import sys
from optparse import OptionParser
import codecs
import justext
import os
import subprocess

import linecache

punctuation_list = [".","?","!"]

usage = "usage: %prog [options] arg"
parser = OptionParser(usage)




parser.add_option("--folder", dest="folder",
                  help="Nazov adresa, ktory obsahuje subory z ClueWeb a bude rekurzive spracovany",
                  type="string", metavar="ADRESAR")


parser.add_option("--output", dest="output",
                  help="Nazov adresa, do ktoreho bude ulozeny vysledok z nastroja mantee",
                  type="string", metavar="ADRESAR")

(options, args) = parser.parse_args()


#testovanie na dostatocny pocet parametrov
if (len(sys.argv) != 1):
    sys.stderr.write("Zly pocet parametrov")
    sys.exit(1)




#pretypovanie na retazec
options.folder=str(options.folder)
pom_prem=str(options.folder)


#kontrola cesty options.folder
if (move_on == 0):
#odstranim / zo zaciatku parametra input
    if (options.folder[0] == '/'):
        pom_prem=input_file_name
        input_file_name=input_file_name.strip('/')
        tag_remove=1

        #otestujem, ci bol zadany priecinok
    if (os.path.isdir(options.folder) == True):
        move_on=1
#ak bol tak nacitam vsetky hlavickove subory do zoznamu fileList
        for root, subFolders, files in os.walk(options.folder):
            for file in files:
                if file.endswith("txt"):
                    fileList.append(os.path.join(root,file))
            is_param_file=0
    else:
        move_on=0
#testujem ci parameter input nie je priecinok s / na zaciatku
    if (tag_remove == 1):
        input_file_name=pom_prem
#pokial je to priecinok
        if (os.path.isdir(input_file_name) == True):
            move_on=1
            pom_prem=""
            #prehladavam vsetky priecinky a ukladam si do fileListu hlav.sub.
            for root, subFolders, files in os.walk(input_file_name):
                for file in files:
                    if file.endswith("txt"):
                        fileList.append(os.path.join(root,file))
            is_param_file=0
        else:
            if (input_file_name[0] == '/'):
                input_file_name=input_file_name.strip('/')
                tag_sek=1
            if (move_on !=1):
                move_on=0
                
#testujem, ci nahodou nebol zadany subor na prehladavanie
if (move_on == 0):
    pomles=""
    move_on=0
    move_on2=0
    tag_sek=0
    input_file_name=str(options.file)
    input_file_name='/'+input_file_name
    #testuje, ci nebola zadana absolutna cesta k suboru
    if (os.path.isabs(input_file_name) == True):
        
        #pokusim sa subor otvorit 
        try:
            f = codecs.open(input_file_name, "r", "utf-8")
        except IOError:
            move_on2=1
        is_param_file=1
        if (move_on2 == 1):
            if (pom_prem[0] == '/'):
                tag_sek=1
            input_file_name=input_file_name.strip('/')
            try:
                f = codecs.open(input_file_name, "r", "utf-8")
            #pokial zadany subor neexistuje ukoncim program
            except IOError:
                sys.stderr.write("Neznamy subor/ priecinok\n")
                sys.exit(1)
        move_on=1
#testujem, ci bola zadana relativna cesta k suboru a ci esubor existuje
    if (os.path.isabs(input_file_name) == False and move_on==0):
        if (input_file_name[0] != '/'):
#ulozim subor s absolutnou cestou
            pomles=os.getcwd()+'/'+input_file_name
        else:
            pomles=os.getcwd()+input_file_name
        if (os.path.isfile(pomles) == True):
            is_param_file=1
        else:
            sys.stderr.write("Neexistujuci subor/priecinok\n")
            sys.exit(1)


#vytvorim priecinok na vysledok
try:
	os.makedirs(options.output)
except:
    pass
#riadok
line=""
tag = ""
attached_sentence = ""

try:
	subor = codecs.open(options.output+"/"+"clueweb.parsed")
except:
	sys.stderr.write("Chyba pri vytvarani suboru clueweb.parsed")
	sys.exit(1)



try:
	xml_mdparser = codecs.open("mdpfull.xml","r+","utf-8")
except:
	sys.stderr.write("Chyba pri otvarani xml_mdparser properties")
	sys.exit(1)


parsed_line = ""
for hh in range(0,len(fileList)):

	f = codecs.open(fileList[hh],"r","utf-8")

	while(0==0):

		line = f.readline()

		line=unicode(line)
            if not line:
                break
        
        if (line.find("<doc") != -1):
        	subor.write(line)
        

        else if (attached_sentence in punctuation_list):
        	try:
				pom_subor = codecs.open("input/sentence.txt","w","utf-8")
			except:
				sys.stderr.write("Chyba pri otvarani suboru")
				sys.exit(1)

        	pom_subor.write(sentence)
        	pom_subor.close()

        	try:
                subprocess.call(['java -jar mdpfull.jar', 'mdpfull.xml' ])
            except:
                sys.stderr.write("Error in MDParser\n")
             
                sys.exit(1)

            try:
            	output = codecs.open("temp/1.txt","r","utf-8")
            except:
            	sys.stderr.write("Chyba pri otvarani vyparsovaneho suboru")
            	sys.exit(1)
            while (0 == 0):
            	parsed_line = output.readline()
            	if not parsed_line:
            		break
            	subor.write(parsed_line)



            attached_sentence = ""
        	





        else:
        	attached_sentence = attached_sentence + line


os.remove("sentence")
subor.close()
sys.exit(0)



