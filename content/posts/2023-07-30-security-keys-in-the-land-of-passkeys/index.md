+++
title = "Security keys in the land of passkeys"
date = "2023-07-30T00:00:03.351Z"
description = "Protect your synced passkey provider accounts with the gold standard in multi-factor authenticators."
categories = ["webauthn"]
keywords = ["passkeys", "security keys", "passkey providers"]
hasCode = false
+++

Security keys are great! They're considered [the "gold standard" of FIDO2 authenticators](https://fidoalliance.org/fido-alliance-releases-guidelines-for-optimizing-user-experiences-with-fido-security-keys/) because they strongly protect the private keys that power WebAuthn-based authentication. A credential registered via a security key is *guaranteed* never to appear from another security key. Compromising a security-key-protected account thus requires interception of the physical security key as well as a PIN needed to unlock use of it. This gives users and Relying Parties alike confidence that users are who they say they are when they use a security key to log in.

## The trouble with discoverable credentials

While security keys consistently generate "[device-bound passkeys](https://passkeys.dev/docs/reference/terms/#device-bound-passkey)", most users are being moved towards "[synced passkeys](https://passkeys.dev/docs/reference/terms/#synced-passkey)" to help address the historically-lacking account recovery story, for example how users regain login access to their favorite websites in the case of device loss.

This fact raises a non-obvious issue with security keys in a passkey world: **passkeys, whether device-bound or synced, must be stored by the authenticator that creates them**. Platform authenticators embedded in a phone, laptop, or computer can store a near-infinite number of passkeys. Security keys, however, can only store 25 ([Yubico](https://support.yubico.com/hc/en-us/categories/360002541740-Devices)) to as many as 150 ([TrustKey](https://www.trustkeysolutions.com/en/sub/support.form)).

After a bit of math, an internet power-user who wants to maximize their security and only use security keys with WebAuthn-backed authentication would **require 5-30 security keys just to replace all of their *current* passwords with device-bound passkeys**:

![A screenshot of the right-click menu in 1Password with all of my logins highlighted. It reveals I have accumulated over 700 username+password logins over the years](images/password_locker_login_count.png)

Even five is too many security keys for someone like me...

## Additional complications

What further complicates things for security key users is that passkeys management (e.g. the ability to delete individual passkeys to free up space for others) is either A) not supported, B) only supports deleting *all* credentials, both discoverable and non-discoverable, or C) properly supports deleting individual credentials. Which FIDO2 security key supports which management capability is not obvious at first glance and requires digging into manufacturer docs to fully understand.

Another fly in the ointment is the fact that Android 9+ now requires Relying Parties (the websites users are logging into; a.k.a. "RP's") to pass in `residentKey: "preferred"` or `residentKey: "required"` during registration to opt into Android's new passkeys support; this ensures that users end the registration ceremony with a synced passkey. This option must also be passed in during `authenticatorAttachment: "cross-platform"` flows, which were historically only for security key registration but now also allow for registration of a platform authenticator on a separate device (a.k.a. "cross-device registration".)

## A brief recap

Here are the main points so far:

1. Security keys are the **strongest FIDO2 authenticators** on the market.
2. A single security key **cannot store as many discoverable credentials** as people have logins, so users must use multiple keys.
3. Passkeys are leading RP's to call WebAuthn with **options optimized for platform authenticator passkeys support**.
4. These optimized options lead to **security keys always creating discoverable credentials** which quickly exhaust security key internal storage.
5. Security keys have a **non-obvious level of support** for individual credential management.

And I'm going to add the following considerations to the list:

6. **Platform authenticators are superior** to security keys for authentication because **no extra device is needed**. The majority of WebAuthn users will use passkeys synced between their mobile phone and computer and never touch a security key in their life.
7. **Synced passkeys are a good thing**, because no one should get locked out of all of their internet accounts if they drop their phone into the ocean, or simply trade in their phone to upgrade to something newer.

One can acknowledge that platform authenticators that sync passkeys offer a superior experience for users both for ease of use and after device loss. One can also acknowledge that security keys offer far superior security than synced passkeys because security key passkeys never leave the security key.

The two ideas are seemingly at odds, but after some consideration a question arises: **can we enjoy the usability benefits of synced passkeys *and* benefit from the higher level of protection afforded by security keys?**

## A passkey-driven shift in threat modeling

Before I answer that, I want to talk briefly about how I think passkeys adoption will shift the focus of attackers trying to gain illicit access to users accounts. As phishing-resistant WebAuthn credentials replace the use of passwords, attackers won't be able to rely anymore on crawling through database dumps for account credentials, or on deploying phishing sites to collect victims' usernames and passwords.

One way I believe attackers will adapt is by setting their sights on first- and third-party "**passkey provider**" accounts, like victims' Apple IDs and 1Password accounts among others. Passkey provider account recovery processes have to consider a multitude of scenarios in which a user may be unable to access their account, including in case of total device loss. **The use of emailed magic links, or the dreaded one-time code sent via SMS, will still offer phishable opportunities** for attackers to commandeer the recovery process and gain control of the passkey provider account that contains the victim's synced passkeys. Once an attacker compromises a passkey provider account they can sync the victim's passkeys to an attacker-owned phone and begin wreaking havoc.

From the attacker's perspective, "extracting HSM-protected passkeys from a victim's stolen phone" is an impossibly higher bar to overcome than "phishing a victim for their email account credentials to grab their passkey provider account recovery magic link."

## Dressing in layers

Returning to the question at hand...

> Can we enjoy the usability benefits of synced passkeys *and* benefit from the higher level of protection afforded by security keys?

...I believe the answer to this question is simple: **use security keys to protect your passkey provider accounts!**

Get **two FIDO2-compatible security keys**, then head over to your your [Apple account](https://support.apple.com/en-us/HT213154) or [Google account](https://g.co/passkeys) or whichever passkey provider account is synchronizing your passkeys **and add both security keys as additional authentication factors**. Keep one of those security keys in a safe place afterwards; keep the other one nearby, like on your literal keychain.

From this point on, **use the nearby security key to securely sign into your passkey provider account any time you set it up on a new device**. Once you've authenticated into your passkey provider account and your synced passkeys have been pulled down, you can resume using your device's platform authenticator to quickly sign into websites. The nearby security key will come back out the next time you need to set up a new device.

One thing you'll notice after doing this is that passkey providers will drop the use of other (potentially phishable) second-factor methods. For example, both **Google**...

> If your account has 2-Step Verification or is enrolled in the Advanced Protection Program, **you will bypass your second authentication step** by signing in with a passkey, since this verifies that you have possession of your device.

...and **Apple** drop other second-factors over the use of security keys:

> Because you use a physical key **instead of the six-digit code**, security keys strengthen the two-factor authentication process and help prevent your second authentication factor from being intercepted or requested by an attacker.

This should give most higher-security-minded individuals greater peace of mind that their synced passkeys are now safe from potential phishing attacks too.

## Conclusion

This post was inspired by [a post of mine on Mastodon](https://infosec.exchange/@iamkale/110713564857409117):

![Security keys are great! Use them to secure your passkey provider accounts! Then you can rest easy as you adopt passkeys with that protected passkey provider syncing all your other passkeys for the usability win. That's my position and I'm sticking to it 🔐 #passkeys #webauthn](images/toot.png)

One lesson I've learned from participating in the [Web Authentication Working Group](https://www.w3.org/groups/wg/webauthn/), where I help evolve the WebAuthn standard, is that all standards involve people making compromises along the way. Synced passkeys trade device binding for wider consumer adoption, but also shift phishing attacks that target individual site logins to instead target passkey provider account recovery flows.

While passkeys are touted as being phishing-resistant (they really are), the truth is it's hard to remove the phishable elements of account recovery because we're all still human. Passkey providers must design attack-resistant UX that enables everyone from tech-savvy moms to tech-illiterate grandpas to get back into their accounts after losing their devices. It's during these human-first account recovery flows that even the savviest passkey adopters can get taken advantage of. This post is my attempt to propose a path towards achieving a higher level of account protection for those who want it as we all (hopefully) continue on towards a passkeys-first future.
