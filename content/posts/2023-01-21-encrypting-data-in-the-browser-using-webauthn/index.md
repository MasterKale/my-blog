+++
title = "Encrypting Data in the Browser Using WebAuthn"
date = "2023-01-22T02:54:33.323Z"
description = "My sneakernet fantasies have become reality 👟"
categories = ["webauthn"]
keywords = ["webauthn", "encryption"]
hasCode = true
+++

When I discovered WebAuthn three years ago a quirky idea came to me: "what if you could **also** protect data with a security key?" The idea of a physical authenticator being used to encrypt and decrypt information stuck with me, even after I came to understand that WebAuthn couldn't be used in that way.

Fast forward to 2023. The recent addition of [the `prf` extension to the WebAuthn L3 Draft spec](https://w3c.github.io/webauthn/#prf-extension) is introducing functionality to WebAuthn that makes my crazy idea possible! Imagine it: a quick tap to encrypt a super secret message, a short journey via [sneakernet](https://en.wikipedia.org/wiki/Sneakernet), then a quick tap to decrypt the message...

I'm happy to report that my "crazy idea" has become a reality. And even better, it can all be done entirely in the browser 😏

> Disclaimer: for as in-depth as I can speak to the practical use of cryptographic concepts vis-a-vis WebAuthn, I am still early in my education of many other fundamentals of cryptography. This post represents my deepest dive yet into more complex concepts like HMACs, key derivation, and encryption. While I took steps to verify the content of this post, I apologize for any inaccuracies. Please feel free to [contact me]({{< ref "about" >}}) if I'm off the mark on anything.

## A summary of the `prf` WebAuthn extension

Briefly, `prf` passes bytes from the "Relying Party" (that's you, using WebAuthn) to the authenticator during a WebAuthn authentication ceremony. The authenticator "hashes" (HMACs) these bytes with secret bytes internally associated with a previously registered credential (as per[ CTAP's `hmac-secret` extension](https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html#sctn-hmac-secret-extension)) and returns the resulting bytes to the browser in the output from `navigator.credentials.get()`.

The high-entropy bytes returned from the authenticator are perfect input key material for an "HMAC-based Key Derivation Function" (HKDF), which helps us generate a "key derivation key". The key derivation key is then used to derive _another_ symmetric key that's used to perform the actual data encryption.

Something to remember is that output from the `prf` extension will be **the same for every authentication ceremony** so long as A) the same WebAuthn credential is used, and B) the bytes the RP passes to the authenticator are the same. These two come together to make it possible to **deterministically recreate** the symmetric encryption key protecting the data at any time. And even better, the secret bytes within the authenticator are origin-bound as well because of the origin-bound credential they are associated with!

## Practical use

You can follow along in just a few steps:

1. Install Chrome Canary (at least Version 111.0.5548.0)
2. Navigate to `chrome://flags/#enable-experimental-web-platform-features` and enable it
3. Grab a FIDO2 security key manufactured in the last couple of years. `hmac-secret` exists in CTAP as early as 2018 so you shouldn't need the latest and greatest. I used a [YubiKey Security Key](https://www.yubico.com/products/security-key/) for this.

Let's get down to brass tacks.

### Step 1: Register to prime the authenticator

Make a typical call to `navigator.credentials.create()` with the `prf` extension defined:

```js
/**
 * This value is for sake of demonstration. Pick 32 random
 * bytes. `salt` can be static for your site or unique per
 * credential depending on your needs.
 */
const firstSalt = new Uint8Array(new Array(32).fill(1)).buffer;

const regCredential = await navigator.credentials.create({
  publicKey: {
    challenge: new Uint8Array([1, 2, 3, 4]), // Example value
    rp: {
      name: "SimpleWebAuthn Example",
      id: "dev.dontneeda.pw",
    },
    user: {
      id: new Uint8Array([5, 6, 7, 8]),  // Example value
      name: "user@dev.dontneeda.pw",
      displayName: "user@dev.dontneeda.pw",
    },
    pubKeyCredParams: [
      { alg: -8, type: "public-key" },   // Ed25519
      { alg: -7, type: "public-key" },   // ES256
      { alg: -257, type: "public-key" }, // RS256
    ],
    authenticatorSelection: {
      userVerification: "required",
    },
    extensions: {
      prf: {
        eval: {
          first: firstSalt,
        },
      },
    },
  },
});
```

> NOTE: The `first` passed in here isn't currently used during registration, but the `prf` extension requires it to be set.

Tap your security key, follow the browser prompts, then call `getClientExtensionResults()` afterwards and look for a `prf` entry:

```js
console.log(regCredential.getClientExtensionResults());
// {
//   prf: {
//     enabled: true
//   }
// }
```

If you see `enabled: true` then you're good to continue. If you don't then you'll need to try it again with another security key until you find one that works.

### Step 2: Authenticate to encrypt

The next step is to call `navigator.credentials.get()` and pass in our `firstSalt`:

```js
const auth1Credential = await navigator.credentials.get({
  publicKey: {
    challenge: new Uint8Array([9, 0, 1, 2]), // Example value
    allowCredentials: [
      {
        id: regCredential.rawId,
        transports: regCredential.response.getTransports(),
        type: "public-key",
      },
    ],
    rpId: "dev.dontneeda.pw",
    // This must always be either "discouraged" or "required".
    // Pick one and stick with it.
    userVerification: "required",
    extensions: {
      prf: {
        eval: {
          first: firstSalt,
        },
      },
    },
  },
});
```

Tap your security key again, then call `getClientExtensionResults()` afterwards and look for the `prf` entry:

```js
const auth1ExtensionResults = auth1Credential.getClientExtensionResults();
console.log(auth1ExtensionResults);
//   prf: {
//     results: {
//       first: ArrayBuffer(32),
//     }
//   }
// }
```

The `first` bytes returned here are the key (no pun intended) to the next steps involving [WebCrypto's SubtleCrypto](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto) browser API:

#### Step 2.1: Import the input key material

Create a key derivation key using `crypto.subtle.importKey()`:

```js
const inputKeyMaterial = new Uint8Array(
  auth1ExtensionResults.prf.results.first,
);
const keyDerivationKey = await crypto.subtle.importKey(
  "raw",
  inputKeyMaterial,
  "HKDF",
  false,
  ["deriveKey"],
);
```

#### Step 2.2: Derive the encryption key

Next, create the symmetric key that we'll use for encryption with `crypto.subtle.deriveKey()`:

```js
// Never forget what you set this value to or the key can't be
// derived later
const label = "encryption key";
const info = textEncoder.encode(label);
// `salt` is a required argument for `deriveKey()`, but should
// be empty
const salt = new Uint8Array();

const encryptionKey = await crypto.subtle.deriveKey(
  { name: "HKDF", info, salt, hash: "SHA-256" },
  keyDerivationKey,
  { name: "AES-GCM", length: 256 },
  // No need for exportability because we can deterministically
  // recreate this key
  false,
  ["encrypt", "decrypt"],
);
```

#### Step 2.3: Encrypt the message

Now we can encrypt our message using the aptly named `crypto.subtle.encrypt()` method:

```js
// Keep track of this `nonce`, you'll need it to decrypt later!
// FYI it's not a secret so you don't have to protect it.
const nonce = crypto.getRandomValues(new Uint8Array(12));

const encrypted = await crypto.subtle.encrypt(
  { name: "AES-GCM", iv: nonce },
  encryptionKey,
  new TextEncoder().encode("hello readers 🥳"),
);
```

### Step 3: Authenticate to decrypt

Decrypting the message looks almost the same as everything in Step 2, except during the last step you'll call `crypto.subtle.decrypt()` instead:

```js
const decrypted = await crypto.subtle.decrypt(
  // `nonce` should be the same value from Step 2.3
  { name: "AES-GCM", iv: nonce },
  encryptionKey,
  encrypted,
);
```

If you did everything right, you should see your super secret message:

```js
console.log((new TextDecoder()).decode(decrypted));
// hello readers 🥳
```

## Proof

Here's a screenshot of Chrome Canary after I wired all of this up into my [SimpleWebAuthn example server](https://github.com/MasterKale/SimpleWebAuthn/tree/master/example):

![A screenshot of Chrome with the SimpleWebAuthn example site loaded. The left side shows a successful authentication message, and raw JSON inputs and outputs into the WebAuthn authentication API method. The right half of the browser window shows the console with a sequence of cryptographic events ending in the output of the encrypted message, "hello readers", after having been successfully decrypted.](images/proof.png)

## Things to remember

- The `prf` extension is currently available in Chrome Canary 111. According to the [Chrome Roadmap](https://chromestatus.com/roadmap) we can probably expect to see `prf` support roll out to everyone when Chrome 111 debuts around March 2023.
- Even though the encryption key can be deterministically recreated, the bytes used to derive it are the result of a hash of `bytes within the authenticator || bytes provided by the RP` (see [here](https://w3c.github.io/webauthn/#prf-extension) for how the browser actually salts `bytes provided by the RP` before passing them to the authenticator). An attacker will easily see `bytes provided by the RP` as the inputs for the `prf` extension. However they shouldn't ever be able to get to `bytes within the authenticator`, making it safer to perform the actual encryption and decryption in the browser.
- This encryption scheme is largely protected from **remote threats** thanks to WebAuthn's phishing resistance. This is because the authenticator associates its contribution to the input key material to a specific **origin-bound** credential.
- **Local threats** like JavaScript injection attacks, though, could exfiltrate the value of `inputKeyMaterial` from Step 2.1 and store it away for later use. The [Content Security Policy HTTP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) can help control what JavaScript executes on your site. Unfortunately it won't protect against malicious browser extensions which are often able to ignore CSP headers.
- User verification should always be `"required"`, or always be `"discouraged"`. The authenticator uses two sets of bytes with `hmac-secret`, and chooses which to use based on [the `"userVerification"` argument passed into `navigator.credentials.get()`](https://w3c.github.io/webauthn/#dom-publickeycredentialrequestoptions-userverification). See references to "CredRandomWithUV" and "CredRandomWithoutUV" in [the CTAP spec](https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html#sctn-hmac-secret-extension) for more info.
- I recommend you **always require user verification**. This protects your secret data with the security key's PIN as well since the PIN will be needed to complete the WebAuthn authentication ceremonies.
- The `nonce` value must **always be unique for any single encryption** (and its corresponding decryption) when using AES-GCM encryption keys like in the code above. I've learned it's not a secret, though, so it can be safely transported with the encrypted data for later decryption.
- I protected a simple UTF-8 string in the example above, but the encryption and decryption **should work fine over any arbitrary bytes.**
- There isn't anything preventing platform authenticators from supporting `prf`, but I haven't found one that does yet. I'll update this post if/when any start supporting it.

## In Conclusion

So there you have it, data encryption using WebAuthn. I'm excited by the possibilities this brings to websites, and I know that it's just a matter of time before others find novel ways to apply this technique to strongly protect your secrets.

And heck, now that I've written this I might just try to creating something novel with `prf` too...
