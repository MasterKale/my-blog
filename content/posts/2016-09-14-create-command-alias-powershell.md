+++
title = "Creating Command Aliases in PowerShell"
date = "2016-09-14T09:00:00-07:00"
description = "Figuring out the Windows equivalent to ~/.bash_aliases"
categories = ['howto', 'powershell']
keywords = ['powershell', 'command', 'alias', '.bash_aliases']
hasCode = true
+++

I've been using the Docker for Windows beta lately and things have been going rather smoothly. I got tired of typing `docker-compose` all the time, though, so I dug around a bit and figured out how to create PowerShell aliases to shorten this long command into the much easier `dc`. [MSDN articles](https://msdn.microsoft.com/en-us/powershell/scripting/core-powershell/ise/how-to-use-profiles-in-windows-powershell-ise) aren't the most readable, though, so I distilled things down to this simple guide.

To start, run the following command from within PowerShell to create your personal PowerShell profile:

```powershell
new-item -type file -path $profile -force
```

This will create a file called `Microsoft.PowerShell_profile.ps1` in `Documents\WindowsPowerShell\`. This is the PowerShell-equivalent to `~/.bash_aliases` in Linux.

Next, add `Set-Alias` commands to `Microsoft.PowerShell_profile.ps1`. The format is:

```sh
> Set-Alias alias command-to-alias
```

For example, here's how you can create an alias `dc` for the `docker-compose` command:

```sh
Set-Alias dc docker-compose
```

Now, whenever you open PowerShell you can type `dc up` instead of `docker-compose up` to manage your Compose environment. Pretty simple, right?
