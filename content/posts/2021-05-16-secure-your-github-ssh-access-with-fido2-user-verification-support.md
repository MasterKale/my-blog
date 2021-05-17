+++
title = "Secure your GitHub ssh access with FIDO2 User Verification support"
description = "Authenticate with PIN or biometrics, because User Presence just isn't good enough for us"
date = 2021-05-16T22:14:34.290Z
categories = ["github", "fido2", "howto"]
keywords = ["github", "ssh", "fido2", "UV"]
hasCode = true
draft = false
+++
Early in May [GitHub announced support for securing SSH access with FIDO2 security keys](https://github.blog/2021-05-10-security-keys-supported-ssh-git-operations/) instead of a traditional public+private key pair. The benefits of this are...

However, GitHub only covered how to set this up to support "User Presence", giving *anyone* who has access to your security key the power to tap it to gain ssh access to your repositories. Fortunately there's a better way to protect your repos if you decide to go down this route. When you're done with this guide, you'll have set up access to require a PIN or biometric scan before you can access your repositories. Here's how:

**Step 1: Pick a security key**

Anything fairly recent with "FIDO2" or "WebAuthn" support will work. The [YubiKey Security Key](https://www.yubico.com/product/security-key-nfc-by-yubico/) is an affordable starter choice, while the [Yubikey 5 series](https://www.yubico.com/store/#yubikey-5-series) offer more variety and capabilities for a bit of a premium. [Feitian](https://www.ftsafe.com/Products/FIDO) and [TrustKey](https://www.trustkeysolutions.com/security-keys) are also reputable brands with their own varieties of security keys.

**Step 2: Generate a keypair**

The key to all of this is to take GitHub's `ssh-keygen` command and add the [`-O verify-required`](https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html) flag.

> A couple of things to remember before you begin:
> 1. You'll need to tap the authenticator **after** you enter your security key's PIN.
> 2. Don't bother entering a passphrase. Your PIN will take the place of that.
> 3. When prompted enter the **full path** you want to save the keypair to (e.g. `/Users/you/ssh/<filename>`)

```sh
$> ssh-keygen -t ecdsa-sk -C matthew@millerti.me -O verify-required
Generating public/private ecdsa-sk key pair.
You may need to touch your authenticator to authorize key generation.
Enter PIN for authenticator:
Enter file in which to save the key (/Users/you/.ssh/id_ecdsa_sk): /Users/you/.ssh/security-key-name-uv
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/you/.ssh/security-key-name-uv
Your public key has been saved in /Users/you/.ssh/security-key-name-uv.pub
The key fingerprint is:
SHA256:BunchofRandomStuffHere <email address>
The key's randomart image is:
+-[ECDSA-SK 256]--+
|.o.+ ..          |
|..B *.Eo .       |
|.o.B+=. B        |
|o.=o..+* o       |
|oo . ..oS        |
|o =    o+o       |
|.+oo    o+       |
|=*.     .        |
|B.               |
+----[SHA256]-----+
```

**Step 3: Add your public key to Github**

The command above should have produced two files:

- **/Users/you/.ssh/security-key-name-uv**
- **/Users/you/.ssh/security-key-name-uv.pub**

Head to your [SSH and GPG keys](https://github.com/settings/keys) settings in Github and click **New SSH key**. Enter a value for the key's **Title**, like "security-key-name-uv.pub", then paste in the value of **/Users/you/.ssh/security-key-name-uv.pub** into the **Key** textbox.

**Step 4:



### Troubleshooting:

#### When you try to generate the key you might see the following error:

```sh
$> ssh-keygen -t ecdsa-sk -C foo@bar.com
unknown key type ecdsa-sk
$> ssh -V
OpenSSH_8.1p1, LibreSSL 2.7.3
```

OpenSSH 8.2 was the first version to support ecdsa-sk key types. Installing the latest version of OpenSSH should fix the problem. As of May 2021 the latest version is OpenSSH 8.6.

> On macOS you can easily accomplish this with `brew install openssh`

#### Key enrollment failed: invalid format

```
$> ssh-keygen -t ecdsa-sk -C <email address> -O verify-required
Generating public/private ecdsa-sk key pair.
You may need to touch your authenticator to authorize key generation.
Enter PIN for authenticator:
Key enrollment failed: invalid format
```

Solution: set up a PIN first. Chrome most reliable way, `about:settings` > Security > Manage security keys > Create a PIN. Add a PIN, then retry.