#!/usr/bin/python

import urllib2
import os
import signal
import sys

# 0. this is pkg list what we want to sync
PKG_FILE = "http://download.tizen.org/snapshots/tizen/3.0-mobile/tizen-3.0-mobile_20170627.1/images/target-TM1/mobile-wayland-armv7l-tm1/tizen-3.0-mobile_20170627.1_mobile-wayland-armv7l-tm1.packages"
ID = "[need your id for tizen public git]"
OUTPUT_DIR = "source/"

# to stop the loop when ctrl+c is comming
def signal_handler(signal, frame):
	print("you pressed ctrl+c!. exit");
	sys.exit(0);

signal.signal(signal.SIGINT, signal_handler)


# 1. read pkg list file
f = urllib2.urlopen(PKG_FILE)

start_dir = os.getcwd()


# 2. parsing to get revision and git path
lines = f.readlines()
for line in lines:
	git_path = (line.split(' ')[2]).split('#')[0]
	git_commit = line.split('#')[1]

	try:
		print git_path + " " + git_commit
	except:
		print("Unexpected error:", sys.exe_info()[0])
		raise

# 3. git clone
	git_clone = "git clone ssh://" + ID + "@review.tizen.org:29418/" + git_path + " " + OUTPUT_DIR + git_path
	print "\n" + git_clone
	os.system(git_clone)

# 4. git reset
	print "git reset --hard " + git_commit
	os.chdir(OUTPUT_DIR + git_path)
	os.system("git reset --hard " + git_commit)
	os.chdir(start_dir)

print "\n all git is clonsed ============================================================\n"


