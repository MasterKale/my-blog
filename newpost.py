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
joined_filename = "-".join(args.title)
# Specify the file name including extension
filename = "{}.md".format(joined_filename.lower())
# Use spaces for the actual post title
title = ' '.join(args.title)

"""
Prepare the date variables for the path
"""
today = date.today()
# Create the path as "post/2018/February"
path = today.strftime("posts/%Y-%m-%d")

"""
Execute the Hugo command
"""
# Final command: hugo new posts/2021-05-14-a-new-post.md --editor code
# The exported TITLE gets picked up in the default.md archetype with the `getenv` template function
os.system("export TITLE=\"{}\"; ./hugo new {}-{} --editor code".format(title, path, filename))
