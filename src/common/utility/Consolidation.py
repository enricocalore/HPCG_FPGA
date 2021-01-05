#!/usr/bin/env python

#
# utility that creates a folder that contains the common folder and
# all the files of the example 
#
#
# Copyright (C) 2021 Xilinx, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may
# not use this file except in compliance with the License. A copy of the
# License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from sys import argv
import re
import sys
import os
import os.path

path = os.getcwd()

actual_folder = path
folder_created = path + '_backup'
route = argv[0].split('common')

if(not os.path.isdir(folder_created)):
	cmd = 'cp -rf ' + actual_folder + ' ' + folder_created
	os.system(cmd)
	os.chmod(folder_created, 0o777)

	f = open(folder_created + '/Makefile', "r+")

	string = ""
	listing = ['opencl']

	for txt in f:

		x = re.search("^COMMON_REPO =.*", txt)

		if (x):
			txt = "COMMON_REPO = ./\n"

		string = string + txt

	f.close()

	f = open(folder_created + '/description.json', "r+")
	
	flag = 0
	for txt in f:
		if "\"includepaths\"" in txt:
			flag = 1
			continue

		if (flag == 1):
			if (']' in txt or '}' in txt):
				break
			else:
				listing.append(txt[txt.find("includes/") + 9 : txt.rfind('\"')])
		 
	f.close()

	commonfolders = route[0] + "common/includes/"

	for foldername in os.listdir(commonfolders):
		if foldername in listing:
			cmd1 = 'mkdir -p ' + folder_created + '/common/includes/' + foldername
			cmd2 = 'cp -rf ' + commonfolders + '/' + foldername + '/* ' + folder_created + '/common/includes/' + foldername
			os.system(cmd1)
			os.system(cmd2)

	g = open(folder_created + '/Makefile', "w")
	g.write(string)
	g.close()

	print ("The new folder's location is %s" % folder_created)
