+++
title = "Security keys in the land of passkeys"
date = "2023-07-22T00:00:03.351Z"
description = "Protect your synced passkey provider accounts with the gold standard in multi-factor authenticators."
categories = ["webauthn"]
keywords = ["passkeys", "security keys", "passkey providers"]
hasCode = false
+++

Security keys are great! They're considered [the "gold standard" of FIDO2 authenticators](https://fidoalliance.org/fido-alliance-releases-guidelines-for-optimizing-user-experiences-with-fido-security-keys/) because they very strongly protect the private keys that power WebAuthn-based authentication. A credential registered via a security key is *guaranteed* never to appear for use from another security key. Compromising a security-key-protected account thus requires interception of the physical security key as well as a PIN needed to unlock use of it. This gives users and Relying Parties alike confidence that users are who they say they are when they use a security key to log in.

## The trouble with discoverable credentials

While security keys consistently generate "[device-bound passkeys](https://passkeys.dev/docs/reference/terms/#device-bound-passkey)", most typical users are being moved towards using "[synced passkeys](https://passkeys.dev/docs/reference/terms/#synced-passkey)" to help address the historically-lacking account recovery story in the case of device loss.

This fact raises a non-obvious issue with security keys in a passkey world: passkeys, whether device-bound or synced, must be stored by the authenticator that creates them. Platform authenticators embedded in a phone, laptop, or computer can store a near-infinite number of passkeys in the hundreds of gigabytes of available storage. Security keys, however, can only store a around 25 ([Yubikeys](https://support.yubico.com/hc/en-us/categories/360002541740-Devices)) to 50 passkeys ([SoloKeys](https://github.com/solokeys/solo1/issues/156#issuecomment-477645573)).

After a bit of math, an internet power-user like myself who wanted to maximize their security and only use security keys with WebAuthn-backed authentication could laughably **require 15-30 security keys or more just to replace all of their current passwords with device-bound passkeys**:

![A screenshot of the right-click menu in 1Password with all of my logins highlighted. It reveals I have accumulated over 700 username+password logins over the years](images/password_locker_login_count.png)

## Additional complications

What further complicates things for security keys is that passkeys management (e.g. the ability to delete individual discoverable credentials to free up space) is either A) not supported, B) only supports deleting *all* discoverable credentials, or C) properly supports deleting individual credentials. Which FIDO2 security key supports which management capability is not obvious at first glance and requires digging into manufacturer docs to fully understand.

Another fly in the ointment is the fact that Android 9+ now requires RP's to pass in `residentKey: "preferred"` or `residentKey: "required"` during registration to opt into its new passkeys support and ensure that the user ends the registration with a synced passkey. This option must also be passed in during `authenticatorAttachment: "cross-platform"` flows, which were historically only for security key registration, as browsers now allow for platform authenticator registration on a separate device (a.k.a. "cross-device registration") during this flow as well.

## A passkey-driven shift in threat modeling

I believe that the gradual adoption of synced passkeys by internet users will force attackers to adapt. As phishing-resistant WebAuthn credentials replace the use of passwords, attackers won't be able to rely on database dumps or phishing sites to collect potential victims' usernames and passwords.

One way attackers will adapt is by setting their sights on passkey provider accounts. Passkey provider account recovery processes have to account for a multitude of scenarios in which a user may be unable to access their account, including in case of total trusted device loss. The use of emailed magic links, or the dreaded one-time code sent via SMS, offer phishable opportunities for attackers to commandeer the recovery process to gain control of the passkey provider account that contains the victim's synced passkeys.

After all, "extracting HSM-protected passkeys from a victim's stolen phone" is an impossibly higher bar to overcome than "phishing a victim for their email account credentials to grab their passkey provider account recovery magic link."

## A brief recap

I want to pause for a second to reiterate the following points:

1. Security keys are the **strongest FIDO2 authenticators** on the market.
2. Security keys can **store a very limited number** of discoverable credentials.
3. Passkeys are leading RP's to call WebAuthn with **options "optimized" for platform authenticator passkeys** support.
4. These optimized options lead to **security keys always creating discoverable credentials**.
5. Security keys have a **non-obvious level of support** for individual credential management.
6. Attackers will shift to **targeting passkey provider account recovery mechanisms** to gain access to a victim's synced passkeys.

And I'm going to add the following considerations to the list:

7. **Platform authenticators are superior** to security keys for authentication because **no extra device is needed**. The majority of WebAuthn users will use passkeys synced via their mobile phone and never touch a security key in their life.
8. **Synced passkeys are a good thing**, because no one should get locked out of all of their internet accounts if they drop their phone into the ocean, or simply trade in their phone to upgrade to something newer.

One can acknowledge that platform authenticators that sync passkeys offer a superior experience for users both for ease of use and after device loss. One can also acknowledge that security keys offer far superior security than synced passkeys because security key passkeys never leave the security key.

After considering all of this, a question arises: **can we enjoy the usability benefits of synced passkeys *and* benefit from the higher level of protection afforded by security keys?**

<!-- In the spectrum that is "absolute security" vs "absolute usability", security keys represent a position that sacrifices usability for tighter security. The small, small minority of security-key-only users are willing to accept this trade off. However

But what if there was some way for **security-minded individuals** in the middle to get the best of both worlds here? How might they leverage the superior protection of security-key-generated device-bound passkeys while still benefiting from the people-centric usability of a synced passkey? -->

## Dressing in layers

I believe the answer to this question is simple: **use security keys to protect your passkey provider accounts!**

Get two FIDO2-compatible security keys, then head over to your [Google account](https://g.co/passkeys) or your [Apple account](https://support.apple.com/en-us/HT213154) or whatever passkey provider account is synchronizing your passkeys and add both of those security keys as additional authentication factors. Keep one of those security keys in a safe place afterwards, and keep the other one nearby.

From this point on, use one of your security keys to securely sign into your passkey provider account any time you set it up on a new device. Once you've authenticated into your passkey provider account and your synced passkeys have been pulled down, you can resume using your device's platform authenticator to quickly sign into websites. The security key goes back in the drawer till the next time you need to set up a new device.

One thing you'll notice after doing this is that passkey providers will drop the use of other (potentially phishable) second-factor methods. For example, both **Google**...

> If your account has 2-Step Verification or is enrolled in the Advanced Protection Program, **you will bypass your second authentication step** by signing in with a passkey, since this verifies that you have possession of your device.

...and **Apple** drop other second-factors over the use of security keys:

> Because you use a physical key **instead of the six-digit code**, security keys strengthen the two-factor authentication process and help prevent your second authentication factor from being intercepted or requested by an attacker.

This should give most higher-security-minded individuals greater peace of mind that their synced passkeys are now safe from potential phishing attacks too.

## Conclusion

This post was inspired by [a post of mine on Mastodon](https://infosec.exchange/@iamkale/110713564857409117):

> Security keys are great! Use them to secure your passkey provider accounts! Then you can rest easy as you adopt passkeys with that protected passkey provider syncing all your other passkeys for the usability win.
>
> That's my position and I'm sticking to it 🔐
>
> #passkeys #webauthn

One lesson I've learned after participating in the Web Authentication Working Group, helping to evolve the WebAuthn standard, is that all standards involve people making compromises along the way. Synced passkeys traded device binding for a chance at wider consumer adoption, but also introduced the possibility of a user potentially getting phished during account recovery.

While passkeys are touted as being phishing-resistant (they really are), the truth is it's hard to remove the phishable elements of account recovery because we're all only human. Passkey providers must design attack-resistant UX that enables everyone from tech-savvy moms to tech-illiterate grandpas to get back into their accounts after losing their devices. It's during these human-first account recovery flows that even the earliest passkey adopters can get taken advantage of. This post is my attempt to propose a path towards achieving a higher level of account protection for those who want it.
