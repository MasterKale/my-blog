#!/usr/bin/env python
import os
import argparse
from datetime import date

"""
Prepare a parser to simplify reading in commandline arguments
"""
parser = argparse.ArgumentParser(
    description="A simple script for generating new blog posts with Hugo."
)
parser.add_argument(
    "title",
    nargs="+",
    help="The title of the new post. Example: \"A new post\""
)

"""
Read commandline arguments
"""
args = parser.parse_args()

"""
Construct a filename from the title
"""
# Join all of the words together with dashes in between
joined_filename = '-'.join(args.title)
# Specify the file name including extension
filename = '{}.md'.format(joined_filename.lower())

"""
Prepare the date variables for the path
"""
today = date.today()
# Create the path as "2018/February"
path = today.strftime('%Y/%B')

"""
Execute the Hugo command
"""
# Final command: hugo new post/2018/February/a-new-post.md
os.system('hugo new post/{}/{}'.format(path, filename))