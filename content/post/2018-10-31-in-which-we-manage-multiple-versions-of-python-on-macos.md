+++
title = "In which we manage multiple versions of Python on macOS"
description = "Using Pipenv and pyenv to pick up where Homebrew leaves off"
date = "2018-10-31T21:25:34.636Z"
categories = ["python", "howto"]
keywords = ["python", "pipenv", "pyenv", "macos", "homebrew"]
draft = false
+++
I discovered the hard way recently that Homebrew on macOS will only install the latest version of Python available in its collection of formulae. This frustrated me recently after I accidentally upgraded my Python version to 3.7 in the middle of working on projects that were pinned to 3.6. With no way to revert back via Homebrew, I decided to finally take [pyenv](https://github.com/pyenv/pyenv) out for a spin to see how it'd work along with my [Pipenv](https://pipenv.readthedocs.io/en/latest/)-dominated Python workflow.

Getting pyenv install is fairly simple, as it too can be installed via Homebrew:

```sh
$> brew install pyenv
```

I want to focus next on Pipenv and what it takes to get it and pyenv working together. It's important to note that by default Pipenv is limited to creating virtual environments using existing installations of Python. This effectively limits macOS users to the system Python v2.7.15, or Homebrew-installed v3.7.0 without getting something like pyenv installed.

With the declaration of a single environment variable in your shell config, though, you can activate Pipenv's built-in support for pyenv, thus bypassing this limitation!

After installing pyenv, open up your preferred shell's config file and add a **`PYENV_ROOT`** environment variable that points to **`~/.pyenv`**:

```
export PYENV_ROOT="$HOME/.pyenv"
```

Upon restarting your shell, you _should_ be able to create a new Pipenv environment using the `--python` flag to specify a specific version:

```sh
$> pipenv --python 3.6.7
```

If that particular version isn't installed, then you'll be prompted by Pipenv to allow pyenv to download and install it:

```
$> pipenv --python 3.6.7
Warning: Python 3.6.7 was not found on your system…
Would you like us to install CPython 3.6.7 with pyenv? [Y/n]:
```

Even better, the Python version declared in a project's Pipfile will also be respected! And, if the specified version wasn't already installed, Pipenv will prompt you to allow pyenv to install it:

```sh
$> pipenv install
Warning: Python 3.6 was not found on your system…
Would you like us to install CPython 3.6.7 with pyenv? [Y/n]:
```

In a perfect world we'd be able to give Homebrew a specific Python version as a flag at install time. For now, though, we can "settle" for the excellent interplay between Pipenv and pyenv!

----
### Addendum:

I ran into a curious issue on macOS 10.14 (Mojave) that prevented me from installing any version of Python through pyenv:

> zipimport.ZipImportError: can't decompress data; zlib not available

Further investigation dug up [an open issue on pyenv's Github repo](https://github.com/pyenv/pyenv/issues/1219) that reveals that [current versions of Xcode 10 no longer install headers](https://github.com/pyenv/pyenv/issues/1219#issuecomment-428700763) that pyenv relies on to build Python. 

To get around this for now, it's possible to pass in a [custom **`CFLAGS`** variable](https://github.com/pyenv/pyenv/issues/1219#issuecomment-429331397) when calling `pyenv install` to help it find the build tools it needs:

```sh
$> CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install -v 3.6.7
```

This will almost certainly get sorted out in a future version of pyenv, but until then we're stuck needing to pass in that flag any time we need to install a new version of Python.
