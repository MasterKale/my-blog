+++
title = "WebAuthn sneak peek: hints"
date = "2023-11-15T04:08:42.334Z"
description = "Previewing an upcoming option for Relying Parties to guide users through passkeys registration."
categories = ["webauthn", "passkeys"]
keywords = ["webauthn", "hints"]
hasCode = true
+++

When WebAuthn first hit the scene, Relying Parties (RP's) could choose to launch `navigator.credentials.create()` with one of two values for `authenticatorAttachment` (introduced in [WebAuthn L1](https://www.w3.org/TR/2019/REC-webauthn-1-20190304/#dom-authenticatorselectioncriteria-authenticatorattachment)):

- `"cross-platform"` would have browsers guide users through security key registration
- Browsers would focus on local platform authenticator registration with `"platform"`

Things were simple, and predictable, and some larger Relying Parties crafted UX guidance around this predictability to help users understand what was expected of them.

Then came [synced passkeys](https://passkeys.dev/docs/reference/terms/#synced-passkey); many of those larger Relying Parties reeled from the appearance of [hybrid registration](https://passkeys.dev/docs/reference/terms/#cross-device-authentication-cda). What was previously security-key-only `"cross-platform"` registration now offered users (not yet familiar even with WebAuthn) a third choice involving a mysterious QR code and their mobile devices. Browsers did their best to help users understand what to do next, but RP's who had optimized their cross-platform registration flow with images and text guiding users through "security key registration" found their guidance now only partially informative.

The call went out to the W3C's [Web Authentication Working Group](https://www.w3.org/groups/wg/webauthn/) (WAWG) to offer RP's some ability to break apart the `"cross-platform"` registration flow, to trigger a browser's security key and hybrid registration experiences individually. Triggering these separately would enable impacted RP's to prime their users for registration success by displaying additional context before each ceremony.

After a few weeks of discussion, the WAWG settled on a solution. This is a quick preview of the new `hints` option arriving soon in WebAuthn L3.

NOTE: I focus on registration use cases below, but `hints` are also defined in the spec for use during authentication. In my opinion it'll continue to be best to specify `transports` in `allowCredentials` and let browsers subjectively pick the "best" available authenticator when calling `navigator.credentials.get()`.
{.note role="note"}

## A preview of PublicKeyCredentialHints

The new `hints` option will be passed in with the options given to `navigator.credentials.create()`. This string array can contain one to three of the following possible values constituting the new `PublicKeyCredentialHints` enum (see [WebAuthn L3 draft](https://w3c.github.io/webauthn/#enum-hints)):

- `"client-device"`
- `"security-key"`
- `"hybrid"`

RP's can pass in one value at a time, for example to offer three separate passkey registration flows. Multiple values can also be specified, with the first value as the **most desirable** type of authenticator to register. Browsers can take these hints and tailor their modal registration experience accordingly:

### "client-device"

An RP that sends this value wants the browser to get the user to register their **platform authenticator**. This is similar to sending `authenticatorAttachment: "platform"`.

### "security-key"

This value communicates to the browser that the user should be guided to register a security key. Iconography and text should emphasize the use of **security keys**. This is similar to sending `authenticatorAttachment: "cross-platform"` before the introduction of hybrid registration.

### "hybrid"

RP's can send this value when they want users to register a passkey using their mobile device by scanning a QR code that's displayed on a computer. This is the newest registration flow that is currently grouped together with security keys during `authenticatorAttachment: "cross-platform"` registration ceremonies.

## How hints will eventually be used

An RP can pass in a single option when they want the user to **register the platform authenticator**:

```js
const resp = await navigator.credentials.create({
  publicKey: {
    // ...
    // Equivalent to authenticatorAttachment: 'platform'
    hints: ['client-device'],
  },
});
```

An RP can also specify multiple hints when the goal is for the user to **register a cross-platform authenticator**:

```js
const resp = await navigator.credentials.create({
  publicKey: {
    // ...
    // Equivalent to authenticatorAttachment: 'cross-platform'
    hints: ['hybrid', 'security-key'],
  },
});
```

Hints will also help RP's **only interested in security key registration** to hide hybrid registration in a way that the current `authenticatorAttachment` option can't support:

```js
const resp = await navigator.credentials.create({
  publicKey: {
    // ...
    hints: ['security-key'],
  },
});
```

This new option will give RP's greater opportunities to display helpful text to users before registration, that can contextualize the upcoming WebAuthn call, to better prepare the user for successful passkey registration.

## Will hints satisfy RP's needs?

Efficacy of this new option is entirely hypothetical right now, especially as nothing supports hints as of the date this post was published. And truthfully most RP's won't need these; consumer-centric RP's should allow users to register and authenticate with the authenticator of their choice. But for RP's that can invest some design and development talent to streamline passkey registration UX then `hints` are likely to offer a greater degree of flexibility than the status quo.

I'll note here, a bit more explicitly than in the code samples above, that **`hints` are intended to completely replace the use of `authenticatorAttachment`** - see [here in the L3 draft](https://w3c.github.io/webauthn/#enum-hints):

> Hints MAY contradict information contained in...`authenticatorAttachment`. When this occurs, the hints take precedence.

And finally, even with hints in play, just because a Relying Party passes in `hints: ['security-key']` does not mean the browser is guaranteed to only allow security keys to be registered. Hints are merely a UX optimization and nothing more. **Relying Parties must still verify authenticator responses to then decide whether to accept and recognize a new credential.**

## Current browser support

- TBD
