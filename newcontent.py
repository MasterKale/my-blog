#!/usr/bin/env python
import os
import argparse
from datetime import date

"""
A simple script to quickly create new content with a specific archetype.

Example:
./newcontent.py A New Blog Post
./newcontent.py --archetype gaming God of War 2018
"""

"""
Prepare a parser to simplify reading in commandline arguments
"""
parser = argparse.ArgumentParser(
    description="A simple script for generating new blog posts with Hugo."
)
parser.add_argument(
    "--archetype",
    choices=["posts", "gaming"],
    default="posts",
    help="The type of content to create"
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
folder_name = "-".join(args.title).lower()
# Use spaces for the actual post title
title = ' '.join(args.title)

"""
Prepare the date variables for the path
"""
today = date.today()

if args.archetype == "posts":
    # Create the path as "posts/2021-05-14-title-goes-here/index.md"
    path = "posts/{}-{}/index.md".format(
        today.strftime("%Y-%m-%d"),
        folder_name,
    )
elif args.archetype == "gaming":
    # Create the path as "gaming/2022/title-goes-here/index.md"
    path = "gaming/{}/{}/index.md".format(
        today.strftime("%Y"),
        folder_name,
    )
else:
    raise Exception(f"Unexpected content type {args.content}")

"""
Execute the Hugo command
"""
# Final command: hugo new posts/2021-05-14-a-new-post/index.md --editor code
# The exported TITLE gets picked up in the default.md archetype with the `getenv` template function
os.system("export TITLE=\"{}\"; ./hugo new {} --editor code".format(title, path))
