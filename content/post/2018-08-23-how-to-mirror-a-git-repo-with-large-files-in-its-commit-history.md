+++
title = "How to mirror a git repo with large files in its commit history"
description = "For when Github's 100MB file size restriction bumps up against previously-committed files"
date = "2018-08-28T10:00:00-07:00"
categories = ["git", "howto"]
tags = ["Github", "git"]
draft = false
+++
I was tasked at work recently with mirroring a client's codebase to our internal Github organization. Unfortunately, the initial clone of the repo from the customer's git server took a long time - a _suspiciously_ long time. I've developed a feel for cloning times after working with repos containing all manner of web applications, so right away the time it took to pull down the client's codebase felt "wrong". I immediately suspected that I'd run into issues pushing it up to Github.

Sure enough, when I attempted to push the master branch up to our repo, the process eventually errored out with a message like this:

```sh
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
remote: error: Trace: e3688f9d27edc7d94098eca76412391d        
remote: error: See http://git.io/iEPt8g for more information.        
remote: error: File static/images.zip is 436.46 MB; this exceeds GitHub's file size limit of 100.00 MB        
remote: error: File source-code/static/images.zip is 436.43 MB; this exceeds GitHub's file size limit of 100.00 MB        
To https://github.com/ourcompany/project-name.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'https://MasterKale@github.com/ourcompany/project-name.git'
```

What's this? **A 436MB ZIP file?** No wonder it felt slow!

Upon further investigation, I identified a _second_ instance of this file in another commit! Together, **these two files added up to over 800MB of data** that needed to get pulled down any time the repo was cloned, despite the fact that they existed only in the repo's commit history (neither of these files existed in HEAD when it finished cloning - both were removed within a week of their introduction).

Removing these files from the commit history turned into a three-step process:

1. **Remove the files with `git-filter-branch`:**


```
$> git filter-branch -f --index-filter "git rm --cached --ignore-unmatch static/images.zip" -- --all
$> git filter-branch -f --index-filter "git rm --cached --ignore-unmatch source-code/static/images.zip" -- --all`
```

The **static/images.zip** and **source-code/static/images.zip** paths were pulled from the commits where these files were introduced. This command completely removes these files from their respective commits, as though they never existed in the first place.

2. **Remove the original commit IDs:**


```
$> rm -rf .git/refs/original/
```

3. **Recalculate commit IDs and clean up the repo:**


```
$> git reflog expire --expire=now --all
$> git gc --prune=now --aggressive
```

When all was said and done, the repo dropped from almost 1GB to a paltry 50MB. And of course, without any files larger than 100MB in its commit history, the repo pushed up to Github just fine.

**Unfortunately, this is not a true mirror!**

Try as I might, I could not identify a way to remove the ZIP files while preserving the existing commit IDs. As such, the last step in this process was to reach out to the client with a proposal that included us force-pushing over their master branch with our pruned version. It's a bit of an extreme solution, but due to the way Git works, there wasn't any other way.

For a bit of closure, the client understood why this was necessary and allowed us to update their repo. We were able to proceed with maintenance work and periodically push to their remote server to keep the repos synced.
