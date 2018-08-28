+++
title = "Ignoring Self-Signed SSL Certificate Errors while using Git"
date = 2018-04-19T10:43:11-07:00
description = "How to get Git to play along with self-managed Git servers"
keywords = ["git", "ssl", "sslVerify"]
categories = ["git"]
+++
When I interact with most code repositories they're often hosted on Github, or Gitlab, or some other managed Git service. By and large HTTPS support is a foregone conclusion; I never have issues using `git` commands or GUI clients to interact with those repositories.

Sometimes, though, I find myself working with a repository located in an internal instance of Github Enterprise. When self-managed servers like these have HTTPS support added to them it's via a self-signed certificate. In these cases I often run up against errors like this after trying to clone a repository or fetch the latest remote changes:

> fatal: unable to access 'https://git.foo.bar/FIZZ/repo-buzz/': SSL certificate problem: unable to get local issuer certificate

When this happens, I do one of two things:

If I'm initially cloning the repo down to my machine then I add `-c http.sslVerify=false` to my `git` command:

```sh
git -c http.sslVerify=false clone https://git.foo.bar/FIZZ/repo-buzz/
```

Afterwards I open up a cloned repository's **.git/config** file and add the following setting:

```
[http]
  sslVerify = true
```

This eliminates the need for me to add the `http.sslVerify` flag to subsequent Git commands. Additionally, interactions with the repository via GUI client will also ignore self-signed certificate errors and function as expected.
