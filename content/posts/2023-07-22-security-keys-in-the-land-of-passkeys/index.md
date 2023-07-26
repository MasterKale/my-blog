+++
title = "Security keys in the land of passkeys"
date = "2023-07-22T00:00:03.351Z"
description = "Protect your passkey provider with FIDO's gold standard in multi-factor authenticators."
categories = ["webauthn"]
keywords = ["passkeys", "security keys", "passkey providers"]
hasCode = false
+++

Security keys are great! They're considered [the "gold standard" in FIDO2 authenticators](https://fidoalliance.org/fido-alliance-releases-guidelines-for-optimizing-user-experiences-with-fido-security-keys/) because they very strongly protect the private keys that power WebAuthn-based authentication. A credential registered via a security key is *guaranteed* never to appear for use from another security key. Compromising a security-key-protected account thus requires interception of the physical security key as well as a PIN needed to unlock use of it. This gives users and Relying Parties alike confidence that users are who they say they are when they use a security key to log in.

## The trouble with discoverable credentials

While security keys consistently generate "[device-bound passkeys](https://passkeys.dev/docs/reference/terms/#device-bound-passkey)", most typical users are being moved towards using "[synced passkeys](https://passkeys.dev/docs/reference/terms/#synced-passkey)" to help address the historically-lacking account recovery story in the case of device loss.

This fact raises a non-obvious issue with security keys in a passkey world: passkeys, whether device-bound or synced, must be stored by the authenticator that creates them. Platform authenticators embedded in a phone, laptop, or computer can store a near-infinite number of passkeys in the hundreds of gigabytes of available storage. Security keys, however, can only store a around 25 ([Yubikeys](https://support.yubico.com/hc/en-us/categories/360002541740-Devices)) to 50 passkeys ([SoloKeys](https://github.com/solokeys/solo1/issues/156#issuecomment-477645573)).

After a bit of math, an internet power-user like myself who wanted to maximize their security and only use security keys with WebAuthn-backed authentication could laughably **require 15-30 security keys or more just to replace all of their current passwords with device-bound passkeys**:

![A screenshot of the right-click menu in 1Password with all of my logins highlighted. It reveals I have accumulated over 700 username+password logins over the years](images/password_locker_login_count.png)

## Additional complications

What further complicates things for security keys is that passkeys management (e.g. the ability to delete individual discoverable credentials to free up space) is either A) not supported, B) only supports deleting *all* discoverable credentials, or C) properly supports deleting individual credentials. Which FIDO2 security key supports which management capability is not obvious at first glance and requires digging into manufacturer docs to fully understand.

Another fly in the ointment is the fact that Android 9+ now requires RP's to pass in `residentKey: "preferred"` or `residentKey: "required"` during registration to opt into its new passkeys support and ensure that the user ends the registration with a synced passkey. This option must also be passed in during `authenticatorAttachment: "cross-platform"` flows, which were historically only for security key registration, as browsers now allow for platform authenticator registration on a separate device (a.k.a. "cross-device registration") during this flow as well.

## A brief recap

I want to pause for a second to reiterate the following points:

1. Security keys are the **strongest FIDO2 authenticators** on the market.
2. Security keys can **store a very limited number** of discoverable credentials.
3. Passkeys are leading RP's to call WebAuthn with **options "optimized" for platform authenticator passkeys** support.
4. These optimized options lead to **security keys always creating discoverable credentials**.
5. Security keys have a **non-obvious level of support** for individual credential management.

Now I'm going to add the following opinions of mine to the list:

6. **Platform authenticators are superior** to security keys for authentication because **no extra device is needed**.
7. **Synced passkeys are a good thing**, because no one should get locked out of all of their internet accounts if they drop their phone into the ocean, or simply trade in their phone to upgrade to something newer.

In the spectrum that is "absolute security" vs "absolute usability", security keys represent a position that sacrifices usability for tighter security. The small, small minority of security-key-only users are willing to accept this trade off. However the majority of WebAuthn users will exclusively used synced passkeys and never touch a security key in their life.

But what if there was some way for those **security-minded individuals** in the middle to get the best of both worlds here? How might they leverage the superior protection of device-bound security keys passkeys while still benefiting from the people-centric usability of a synced passkey?

## Dressing in layers

TODO: Protect your passkey providers with security keys.

<!--
Use them to secure your passkey provider accounts! Then you can rest easy as you adopt passkeys with that protected passkey provider syncing all your other passkeys for the usability win.

That's my position and I'm sticking to it 🔐
 -->
