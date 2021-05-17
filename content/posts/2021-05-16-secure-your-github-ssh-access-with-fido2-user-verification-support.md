+++
title = "Secure your GitHub ssh access with FIDO2 User Verification support"
description = "Improve security with a user-verifying PIN, because a tap just isn't good enough for us"
date = 2021-05-16T22:14:34.290Z
categories = ["github", "fido2", "howto"]
keywords = ["github", "ssh", "fido2", "UV", "PIN", "security", "key", "authenticator"]
hasCode = true
draft = false
+++
Early in May [GitHub announced support for securing SSH git operations with security keys](https://github.blog/2021-05-10-security-keys-supported-ssh-git-operations/) instead of with a traditional public+private key pair. One of the greatest benefits of using a security key is that the private key never leaves the secure hardware device itself. This makes it highly improbable that anyone could gain the ability to impersonate you after a computer or account compromise, unlike traditional private keys that reside on your computer.

Disappointingly GitHub only covers how to set this all up to support "User Presence" mode - that is, you're only required to tap your security key without proving who you are. This has the undesirable side effect of giving *anyone* who has access to your key the power to access your repositories!

Fortunately there's a better way to protect your account. FIDO2 (the security key capability that enables all of this) offers an additional level of security through "User Verification". In the land of WebAuthn this means PIN entry or local biometric scan, combining "something you have" with "something you know" or "something you are" (the basic tenets of multifactor authentication). In the context of ssh access this means requiring a PIN to access your repositories (biometrics aren't yet supported by OpenSSH).

What follows is a guide to securing git operations with a higher degree of scrutiny over user identity. When you finish you can rest easy knowing that not just anyone with your security key can commit to your repos both public and private.

Let's begin.

#### Step 1: Pick a security key (skip this if you already have one)

Anything fairly recent with "FIDO2" or "WebAuthn" support will work. The [YubiKey Security Key](https://www.yubico.com/product/security-key-nfc-by-yubico/) is an affordable (USB-A) starter choice, while the [YubiKey 5 series](https://www.yubico.com/store/#yubikey-5-series) offer more variety and capabilities (including USB-C) for a bit of a premium. [Feitian](https://www.ftsafe.com/Products/FIDO) and [TrustKey](https://www.trustkeysolutions.com/security-keys) are also reputable brands with their own varieties of FIDO2 security keys.

#### Step 2: Generate a keypair

> NOTE: You _must_ have a PIN set on your security key to continue. If one isn't set then I suggest using desktop Chrome > `about:settings` > **Security** > **Manage security keys** > **Create a PIN** to set one. Your PIN _must_ be at least four characters long, but beyond that you're free to set whatever you want (including an entire passphrase)!

Take GitHub's `ssh-keygen` command and add the [`-O verify-required`](https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html) flag:

```sh
$> ssh-keygen -t ecdsa-sk -C <email address> -O verify-required
```

`ssh-keygen` will prompt you for your security key's PIN. Make sure to tap the key when it starts blinking afterwards to continue.

Next you'll be asked for a passphrase - you can skip this as your key's PIN will take the place of it.

Finally when prompted enter the **full path** you want to save the keypair to (e.g. `/Users/you/ssh/security-key-name-uv`).

When you're finished, you'll end up with two files:

- **/Users/you/.ssh/security-key-name-uv**
- **/Users/you/.ssh/security-key-name-uv.pub**

#### Step 3: Add the public key to Github

Head to your [SSH and GPG keys](https://github.com/settings/keys) settings in Github and click **New SSH key**. Enter a value for the key's **Title**, like "security-key-name-uv.pub", then paste in the value of **/Users/you/.ssh/security-key-name-uv.pub** into the **Key** textbox:

![screenshot of SSH keys / Add new screen with Title and Key populated](/static/images/add_key_to_github.jpg)

Click **Add SSH key** to save the public key to your account.

#### Step 4: Update your ssh config to use the "private key"

Open **~/.ssh/config** in your favorite editor and add the following:

```
Host github.com
  IgnoreUnknown UseKeychain
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/security-key-name-uv
```

`IdentityFile /Users/you/.ssh/security-key-name-uv` tells SSH to authenticate with your security key whenever you try to access GitHub. It's worth noting that this "private key" on your computer is useless without the corresponding security key that generated it, hence the quotes around "private key"!

#### Step 5: Confirm ssh access

Open up a terminal and `ssh` into github.com to confirm that your SSH key is properly set up:

```sh
$> ssh -T git@github.com
```

`ssh` will prompt you for your security key's PIN, and then require you to tap the security key. You should see a message like this when everything is set up properly:

```
Hi MasterKale! You've successfully authenticated, but GitHub does not provide shell access.
```

And that's it! You've successfully leveraged FIDO2's User Verification feature for greater access control to your GitHub account. If you ever lose or replace your security key you can simply repeat these steps to add the new key to your account (make sure to delete the old one when you do.) Happy coding!

### Troubleshooting:

#### - "unknown key type ecdsa-sk"

```sh
$> ssh-keygen -t ecdsa-sk -C <email address> -O verify-required
unknown key type ecdsa-sk
$> ssh -V
OpenSSH_8.1p1, LibreSSL 2.7.3
```

OpenSSH 8.2 was the first version to support ecdsa-sk key types. Installing the latest version of OpenSSH should fix the problem. As of May 2021 the latest version is OpenSSH 8.6.

> On macOS you can easily accomplish this with `brew install openssh`

#### - "Key enrollment failed: invalid format"

```sh
$> ssh-keygen -t ecdsa-sk -C <email address> -O verify-required
Generating public/private ecdsa-sk key pair.
You may need to touch your authenticator to authorize key generation.
Enter PIN for authenticator:
Key enrollment failed: invalid format
```

Desktop Chrome is the most reliable way to set a PIN. Open up a tab and head to `about:settings` > **Security** > **Manage security keys** > **Create a PIN** to set one.

#### - "Bad configuration option: usekeychain"

```sh
$> ssh -T git@github.com
/Users/you/.ssh/config: line 3: Bad configuration option: usekeychain
/Users/you/.ssh/config: terminating, 1 bad configuration options
```

Add `IgnoreUnknown UseKeychain` to the top of your github.com Host entry in **~/.ssh/config**:

```txt
Host github.com
    IgnoreUnknown UseKeychain
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/security-key-name-uv
```
