+++
title = "WWDC23: Passkeys"
date = "2023-06-10T15:32:29.589Z"
description = ""
categories = ["apple", "wwdc", "webauthn"]
keywords = []
hasCode = true
+++

There wasn't a lot of news about passkeys at WWDC23. And in fact I had to go digging to find more than the single passkeys-specific "Deploy passkeys at work" video available on the Apple Developer app:

![A screenshot of the Apple Developers app on macOS. A search for "passkeys" brings up a list of collections, videos, and articles with the keyword highlighted, but a mix of content from both WWDC22 and WWDC23. Only one video, "Deploy passkeys at work", is specifically about passkeys.](images/developers_app_passkeys_search.png)

Last week I managed to glean more insights into Apple's continuing evolution of their passkeys support from other places online so I decided to pull together all the latest news I found about Apple's evolving passkeys support coming in **iOS 17**, **iPadOS 17**, and **macOS 14**.

## Deploy passkeys at work

This was the one video at WWDC23 that was specifically about passkeys. And surprisingly, it was about how to enable use of **`"enterprise"` attestation with platform authenticators** on managed Apple devices!

The long and short of this new capability seems to be that Apple is enabling companies with device management solutions in place to deploy new policies out to devices that enable a couple of things:

1. Controls on iCloud Keychain sync to ensure that passkeys registered on managed iCloud accounts will only save to the managed iCloud Keychain and sync to approved devices. Even tighter restrictions can be enforced on "supervised" managed devices, which might be specific to [Apple Business Manager](https://www.apple.com/business/enterprise/it/) and [Apple School Manager](https://www.apple.com/education/). Deploying the device policies related to iCloud Keychain sync with managed iCloud accounts is *not* restricted to these two device management solutions, though.
2. "Attestation configurations" to provision an identity certificate that devices that will then use when providing enterprise attestation to specific Relying Parties. This certificate can chain back to an organization's root certificate, and include whatever identifying information about the device that might be useful to receive back during a WebAuthn registration requesting `"attestation": "enterprise"`.

These two new types of managed device policies should give RP's the controls they need to start feeling comfortable deploying FIDO2-based authentication internally.

For those who are interested, here's an example of a **passkey attestation configuration**:

```json
// Example configuration: com.apple.configuration.security.passkey.attestation

{
  "Type": "com.apple.configuration.security.passkey.attestation",
  "Identifier": "B1DC0125-D380-433C-913A-89D98D68BA9C",
  "ServerToken": "8EAB1785-6FC4-4B4D-BD63-1D1D2A085106",
  "Payload": {
    "AttestationIdentityAssetReference": "88999A94-B8D6-481A-8323-BF2F029F4EF9",
    "RelyingParties": [
      "www.example.com"
    ]
  }
}
```

And **enterprise attestation statements** returned by managed devices will be `"packed"` format with the AAGUID `dd4ec289-e01d-41c9-bb89-70fa845d4bf2`:

```js
// WebAuthn Packed Attestation Statement Format

attestationObject: {
  "fmt": "packed",
  "attStmt": {
    "alg": -7, // for ES256
    "sig": bytes,
    "x5c": [ attestnCert: bytes, * (caCert: bytes) ]
  }
  "authData": {
    "attestedCredentialData": {
      "aaguid": "dd4ec289-e01d-41c9-bb89-70fa845d4bf2", // for Apple devices
      // ...
    },
    // ...
  }
  // ...
}
```

Check out the video here for full details and the above code snippets. It's a short one at just over 16 minutes: https://developer.apple.com/wwdc23/10263

P.S. I'm not as knowledgeable about managing Apple devices (most of the work I do is in service of supporting unmanaged "BYOD" devices) so please let me know if I got something wrong here and I'll set the record straight.
{.note role="note"}

## Support for new WebAuthn extension

Good news, WebAuthn extension lovers: Safari 17 will include [official support for the `largeBlob` extension](https://developer.apple.com/documentation/safari-release-notes/safari-17-release-notes#Authentication) from local platform authenticators! Security keys have supported this extension for a while, but it'll be nice for platform authenticators to start supporting it as well. I've heard it can open up some novel use cases, for example storing with a credential an SSH certificate to authenticate server connections from a CLI tool 🤯

You can read more information about the `largeBlob` extension in the WebAuthn L2 spec here: https://www.w3.org/TR/webauthn-2/#sctn-large-blob-extension
{.note role="note"}

## Third-party passkey providers

This last one is the most exciting for me so I'll end with this: we are rapidly approaching the next phase of passkeys support in which third-party "**passkey providers**" can tap into OS-level APIs to create and use passkeys on behalf of their users. This means power users will soon have the freedom to choose which app they use to manage their passkeys, if first-party passkey providers are not to their liking. It should also bring with it some consistency in how users interact with the OS to complete WebAuthn ceremonies while third-parties are in play.

Google released the alpha of [Android's upcoming Credential Manager](https://developer.android.com/training/sign-in/passkeys) passkey provider API support [earlier this year](https://android-developers.googleblog.com/2023/02/bringing-together-sign-in-solutions-and-passkeys-android-new-credential-manager.html). I was pleased to hear [through the grapevine](https://hachyderm.io/@rmondello/110509448037547578) that Apple has also publicly revealed their own passkey provider API in the form of additional functionality added to the existing [ASCredentialProviderViewController](https://developer.apple.com/documentation/authenticationservices/ascredentialproviderviewcontroller), "a view controller that a password manager app uses to extend Password AutoFill:"

- `prepareInterface(forPasskeyRegistration:)` ([link](https://developer.apple.com/documentation/authenticationservices/ascredentialproviderviewcontroller/4172626-prepareinterface))
- `prepareInterfaceToProvideCredential(for:)` ([link](https://developer.apple.com/documentation/authenticationservices/ascredentialproviderviewcontroller/4172627-prepareinterfacetoprovidecredent))
- `provideCredentialWithoutUserInteraction(for:)` ([link](https://developer.apple.com/documentation/authenticationservices/ascredentialproviderviewcontroller/4172628-providecredentialwithoutuserinte))

Documentation for these methods are light on details so that's about all I could make sense of. These new instance methods say they'll become available for third-party passkey providers to use in **iOS 17**, **iPadOS 17**, and **macOS 14**.

What's more, these view controller improvements will enable third-party browsers on macOS that integrate the [ASAuthorizationWebBrowserPublicKeyCredentialManager](https://developer.apple.com/documentation/authenticationservices/asauthorizationwebbrowserpublickeycredentialmanager) class to also support use of third-party passkey providers. In fact it's this class, available since macOS 13.3(!), that offers a path towards **macOS browsers all having a unified interface for WebAuthn interactions!** Soon RP's won't have to worry about per-browser credential stores when all macOS browsers can access the same iCloud Keychain-stored passkeys (and third-party-managed passkeys through the same interface) 🚀

## Wrap-Up

And that's everything I could find. It's not WWDC22 levels of hype from Apple for passkeys, but the company is clearly putting in the work to support more nuanced enterprise use cases.

I'm most excited for the API's that add support for third-party passkey providers because it means my password manager can also manage my passkeys - I already trust it with my passwords, so why not my passkeys? I'm also glad to see third-party macOS browsers have a path forward to support use of passkeys managed by first- _and_ third-party passkey providers via a unified interface.

Here's to a great year for passkeys! I can't wait to come back to this post after WWDC24 to see how things played out... 🔐
