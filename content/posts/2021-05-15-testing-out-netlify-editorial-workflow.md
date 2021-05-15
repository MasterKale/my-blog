+++
title = "Testing out Netlify Editorial Workflow"
description = "It's been a while - can I grok how this works?"
date = 2021-05-15T17:38:35.057Z
categories = ["netlify"]
keywords = ["netlifycms", "editorial", "workflow"]
hasCode = false
draft = false
+++
So apparently when I "Save" this post, Netlify CMS will create a new branch for the article and then spawn a PR to merge it into master. Changes to the article get tracked as commits to the branch. Then, when I'm ready for the article to go live, I can "Publish" it to squash merge the PR into master, and the branch will get deleted.

Let's find out if it works as advertised. SAVE!