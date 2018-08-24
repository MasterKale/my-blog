+++
title = "How to mirror a git repo with large files in its commit history"
description = "For when Github's 100MB file size restriction bumps up against previous bad decisions"
date = "2018-08-23T16:43:06-07:00"
categories = ["git", "howto"]
tags = ["Github", "macOS"]
draft = true
+++
I was recently tasked with mirroring a client's git repo to our company's Github organization. The initial clone of the repo from the customer's git server took a suspiciously long time, so right off the bat I suspected that I'd run into issues pushing it up to Github.

Sure enough, when I attempted to push it all up to our repo, the process eventually errored out with a message like this:

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

Frustratingly, **images.zip** didn't exist in HEAD because they were deleted in a separate commit several days after they had been initially committed. Despite that, they still existed in the repo's commit history, and thus had to be purged.

After some digging, I initially attempted to remove these files with a call to `git-filter-branch` followed by a `git gc` command or two. The files persisted.

What ended up working for me was a program called [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)! It's a JAR file you can execute with a couple of flags to replace these large files with empty placeholders while preserving commit IDs and the overall history of the repo.

To install BFG on macOS High Sierra, I installed Java using Homebrew:

```sh
$> brew cask install java
```

Once Java finished installing, I [downloaded the latest version](http://repo1.maven.org/maven2/com/madgag/bfg/) (**v1.13.0** as of writing this) and dropped it in the root folder of the problematic repo (at the same level as the **.git/** directory.)

Running BFG was pretty simple. I used the flag that told it to prune any file larger than 100M:

```sh
$> java -jar bfg-1.13.0.jar --strip-blobs-bigger-than 100M .git
```

In seconds, BFG crawled through all commits leading up to HEAD and replaced any blob larger than 100M with a tiny plaintext file containing the git hash of the file itself:

![Showing off BFG's file replacement of large files](/images/screen-shot-2018-08-23-at-5.03.48-pm.png)

**Warning:** BFG will tell you to run \`git reflog expire --expire=now --all && git gc --prune=now --aggress\` afterwards. **DON'T DO THIS! **This will recreate _all_ commit IDs, making it impossible for the two repos to mirror each other since none of the commits will line up!

Instead, to finish things up I ran just the garbage collection command:

```sh
$> git gc --prune=now --aggressive
```

Once that finished, a push up to our Github repo succeeded just fine:

```sh
$> git push ourcompany master
Counting objects: 5130, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (1442/1442), done.
Writing objects: 100% (5130/5130), 58.50 MiB | 1.66 MiB/s, done.
Total 5130 (delta 3120), reused 5122 (delta 3116)
remote: Resolving deltas: 100% (3120/3120), done.
To https://github.com/ourcompany/project-name.git
 * [new branch]      master -> master
```

That's quite an improvement! From here on, we could commit and push to either remote without issue. Additionally, our devs can clone our copy of the repo in a fraction of the time 😉
