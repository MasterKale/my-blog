+++
title = "Tracking Docker Image Updates: Attempt 1"
description = "Let's try using Github's Atom feeds to track updates via RSS"
date = "2018-09-21T00:10:10.566Z"
categories = ["docker"]
keywords = ["docker", "github", "rss"]
draft = false
+++
I'm a huge fan of Docker, and so I run a few web applications at home on my own personal Docker host. Unfortunately, keeping these applications up-to-date with their latest Docker images often devolves into my remembering to peruse Docker Hub to see how out of date the version I declared in docker-compose.yml is with whatever tag is the latest.

After this most recent round of update wrangling, I decided to try and figure out a more automated way of keeping track of these releases. For this attempt, I've decided to use Github's Atom feeds to track image releases via their respective repositories.

If you've never used [RSS](https://en.wikipedia.org/wiki/RSS) before, suffice to say that many sites offer a URL "feed" you can track via an "RSS reader". Feeds are periodically updated with new content by their respective site, at which point you can access your chosen reader to view them in a personally-tailored newsfeed.

> Many such RSS readers exist. I'm a lifetime Pro user of [Feedly](https://feedly.com/) so I'm biased towards it. They have a Free tier as well so you can try it out with no commitment! There are even options for self-hosted RSS readers if you so choose.

It may surprise you to hear that Github offers the ability to track various types of activity for any given repo with a number of different Atom feeds. To find these feed URLs, **view a repo's page source** and search for `application/atom+xml`. At the time of this writing, you'll find feeds tracking a repo's **releases**, **tags**, and **commits**!

For this particular solution, I'm interested in the **releases** feed. The URL for this feed typically looks like this (in this case it's the image for the controller software I use to maintain my Ubiquiti Unifi WAP):

> https://github.com/jacobalberty/unifi-docker/releases.atom

The idea is, when a new image goes out to Docker Hub, it means a corresponding release has been tagged on Github. In response, the repo's **releases.atom** feed will update to show this new release. Thus, to track releases of this image, I can simply add this URL to my reader!

Over time, new items in my newsfeed will appear specifically from these repos. When I see one, I know it's time to log into my Docker host and update a particular docker-compose.yml file to point to the new image tag. I can then relaunch the container and presto, updated application!

And before you say it, yes, I'll admit that this process is still needlessly manual. However, I'll take this over administrating an intranet copy of a CI/CD solution any day! Curse you, Jenkins...

_P.S.: Has it really been been five years since Google shuttered Reader?_ 😢
