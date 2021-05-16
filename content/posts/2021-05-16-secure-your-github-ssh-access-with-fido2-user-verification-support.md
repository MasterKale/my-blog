+++
title = "Secure your GitHub ssh access with FIDO2 User Verification support"
description = "Because User Presence just isn't good enough for us"
date = 2021-05-16T22:14:34.290Z
categories = ["github", "fido2", "howto"]
keywords = ["github", "ssh", "fido2", "UV"]
hasCode = true
draft = false
+++
Early in May Github announced support for using FIDO2 security keys to protect ssh access to your repos:

https://github.blog/2021-05-10-security-keys-supported-ssh-git-operations/

However, they only detail how to set this up to support "User Presence", requiring *anyone* to tap your authenticator to log in as you. Sadly they fail to mention that security keys support "User Verification", via a PIN or biometric, that can prevent your security key from being used by others. Here's how:

1. 



### Troubleshooting:

- When you try to generate the `ecdsa-sk` key you might see the following error (w/OpenSSH_8.1p1, LibreSSL 2.7.3):

```
unknown key type ecdsa-sk
```
This usually means you need to update SSH. On macOS you should be able to update with `brew install openssh` to get things new enough to support generating these kinds of keys.