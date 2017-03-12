
import sys
import os
import time
import shutil

# As of right now, commits are on the file level
# For each file you can make several versions and move around

# TODO
# - commit multiple files at a time
# - goto a commit for multiple files at a time
# - list commits should be more universal
# - don't make a new versions directory if you happen to be
#   inside a directory (recursively look up directories for versions/)

# Make the copies directory if it doesn't already exist

versions_dir = "versions/"

if not os.path.isdir(versions_dir):
	os.mkdir(versions_dir)

def list_commits(file):

	directory = versions_dir + "/" + file + "/"
	print os.listdir(directory)

def go_to_commit(commit, file):

	# Replaces file with the copy at the commit

	old_copy = versions_dir + "/" + file + "/" + commit
	shutil.copy2(old_copy, file)

def make_commit(commit_name, file):

	# Creates a new file at versions/filename/commit_name

	directory = versions_dir + "/" + file + "/"
	if not os.path.isdir(directory):
		os.makedirs(directory)
	shutil.copy2(file, directory + commit_name)


args = sys.argv

# Drop the first arg
args.pop(0)

# Case analysis on the new first arg

if (args[0] == "commit"):
	make_commit(args[1], args[2])
elif (args[0] == "goto"):
	go_to_commit(args[1], args[2])
elif (args[0] == "list"):
	list_commits(args[1])
