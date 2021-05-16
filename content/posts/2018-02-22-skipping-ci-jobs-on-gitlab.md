+++
title = "Skipping CI Jobs on GitLab"
date = "2018-02-22T16:35:17Z"
description = "tl;dr: Add [skip ci] to your commit messages"
categories = ['howto', 'gitlab']
keywords = ['gitlab', 'continuous integration', 'ci']
+++

In the last year or so I've earnestly incorporated Continuous Integration (CI) pipelines into a couple of projects to automate the testing, building, and deployment of various sites and packages. My personal projects have yet to achieve critical mass and so thus far I've been able to get by with GitLab's free tier. The most "onerous" restriction of this tier is that it includes a finite amount of pipeline execution time that resets on a monthly basis.

To remain able to deploy as needed, I've developed a constant mindfulness of the fact that each commit can consume valuable execution time, even if the changes are for a trivial tweak to a comment, variable renaming, or other such inconsequential change. To that end, one of the things I look up early on when evaluating a CI solution is how I, as a developer, can indicate to the build system, "don't process this commit!"

Fortunately, on GitLab [the solution is pretty simple](https://docs.gitlab.com/ee/ci/yaml/README.html#skipping-jobs): **add `[skip ci]` to your commit message!** `[ci skip]` works too, but I prefer the more naturally-worded alternative above.

For example, let's say you've updated your repo's **README.md** file. To prevent a pipeline execution, write out your commit message as usual, then append either of those tags:

> Updated README\
> [skip ci]

When you then push that commit to GitLab, your CI configuration will be ignored and those precious execution minutes will persist till the next build.

**A word of caution**: if one of those commit messages makes it into a merge commit from, say, a PR to merge a `feature` branch into `master`, that merge won't get processed! In these instances a squash-and-merge with a clean commit message should prevent any such issue.
