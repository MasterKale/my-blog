+++
title = "In which we manage multiple versions of Python on macOS"
description = "Using Pipenv and pyenv to pick up where Homebrew leaves off"
date = 2018-10-31T21:25:34.636Z
categories = ["python", "howto"]
keywords = ["python", "pipenv", "pyenv", "macos", "homebrew"]
draft = true
+++
I discovered the hard way recently that Homebrew on macOS seems to only be able to install the latest version of Python. This frustrated me recently when I accidentally upgraded my Python version to 3.7 when I was working on projects that were pinned to 3.6. With no way to work this out via Homebrew, I decided to finally take [pyenv](https://github.com/pyenv/pyenv) out for a spin to see how it'd work along with my [Pipenv](https://pipenv.readthedocs.io/en/latest/)-dominated Python workflow.

Getting pyenv install is fairly simple, as it too can be installed via Homebrew:

```sh
$> brew install pyenv
```

I want to focus next on Pipenv and what it takes to get it and pyenv working together. It's important to note first that Pipenv typically can only use system versions of python when you create a new environment. With the declaration of a single environment variable in your shell config, though, you can activate Pipenv's built-in support for pyenv!

First, open up your preferred shell's config file and add a **`PYENV_ROOT`** variable that points to **`~/.pyenv`**:

```
export PYENV_ROOT="$HOME/.pyenv"
```

Upon restarting your shell, you _should_ be able to specify specific versions of 

In a perfect world I'd be able to give Homebrew a specific Python version as a flag at install time.
