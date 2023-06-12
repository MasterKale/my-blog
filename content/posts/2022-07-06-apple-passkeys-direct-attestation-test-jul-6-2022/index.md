+++
title = "Apple Passkeys - Direct Attestation Test (July 6, 2022)"
date = "2022-07-07T06:27:31.032Z"
description = ""
categories = ["webauthn", "macos", "safari", "apple"]
keywords = ["apple", "passkeys", "webauthn"]
hasCode = true
+++

Testing passkey registration with "direct" attestation and tracking what happens.

A reminder that the [SimpleWebAuthn response debugger](https://debugger.simplewebauthn.dev) is available for those who wish to directly introspect the registration or authentication responses.

## macOS Ventura Beta 2 - Safari Version 16.0 (18614.1.16.11.3)

### Registration

```json
// Registration Options
{
  "challenge": "8qhl0nJ-cKUJhfEmwULBUIRtsoNAbd1q2mHYWfJd6IQ",
  "rp": {
    "name": "SimpleWebAuthn Example",
    "id": "dev.dontneeda.pw"
  },
  "user": {
    "id": "internalUserId",
    "name": "user@dev.dontneeda.pw",
    "displayName": "user@dev.dontneeda.pw"
  },
  "pubKeyCredParams": [
    {
      "alg": -7,
      "type": "public-key"
    },
    {
      "alg": -257,
      "type": "public-key"
    }
  ],
  "timeout": 60000,
  "attestation": "direct",
  "excludeCredentials": [],
  "authenticatorSelection": {
    "userVerification": "required",
    "residentKey": "required",
    "requireResidentKey": true
  },
  "extensions": {
    "credProps": true
  }
}

// Registration Response
{
  "id": "AXdreeORcwhCCiy8RMNW71xINK0",
  "rawId": "AXdreeORcwhCCiy8RMNW71xINK0",
  "response": {
    "attestationObject": "o2NmbXRkbm9uZWdhdHRTdG10oGhhdXRoRGF0YViYPdxHEOnAiLIp26idVjIguzn3Ipr_RlsKZWsa-5qK-KBdAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAF3a3njkXMIQgosvETDVu9cSDStpQECAyYgASFYIBEtMfThOHMz9o8bq1KONhE59gUHOFeIvo93pbDu6OusIlgg8FOvHtoKW_Sdif0qQHGhEJir8xMkHX4OPtY1RYRtDko",
    "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiOHFobDBuSi1jS1VKaGZFbXdVTEJVSVJ0c29OQWJkMXEybUhZV2ZKZDZJUSIsIm9yaWdpbiI6Imh0dHBzOi8vZGV2LmRvbnRuZWVkYS5wdyJ9"
  },
  "type": "public-key",
  "clientExtensionResults": {},
  "authenticatorAttachment": "platform",
  "transports": [
    "internal",
    "cable"
  ]
}

// Server Response
{
  "verified": true,
  "fmt": "none",
  "aaguid": "00000000-0000-0000-0000-000000000000",
  "credentialDeviceType": "multiDevice",
  "credentialBackedUp": true,
  "userVerified": true
}
```

### Authentication (typical WebAuthn)

```json
// Authentication Options
{
  "challenge": "b77cNsEplP9J2L0gBc5egNBFWcvOzY5DlJVNiKiFJGE",
  "allowCredentials": [
    {
      "id": "AXdreeORcwhCCiy8RMNW71xINK0",
      "type": "public-key",
      "transports": [
        "internal",
        "cable"
      ]
    }
  ],
  "timeout": 60000,
  "userVerification": "required",
  "rpId": "dev.dontneeda.pw"
}

// Authentication Response
{
  "id": "AXdreeORcwhCCiy8RMNW71xINK0",
  "rawId": "AXdreeORcwhCCiy8RMNW71xINK0",
  "response": {
    "authenticatorData": "PdxHEOnAiLIp26idVjIguzn3Ipr_RlsKZWsa-5qK-KAdAAAAAA",
    "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uZ2V0IiwiY2hhbGxlbmdlIjoiYjc3Y05zRXBsUDlKMkwwZ0JjNWVnTkJGV2N2T3pZNURsSlZOaUtpRkpHRSIsIm9yaWdpbiI6Imh0dHBzOi8vZGV2LmRvbnRuZWVkYS5wdyJ9",
    "signature": "MEUCIQCdfofdfCbR1YUNOMUXdX10O4_340C2GC1K5GoIVJGQzQIgbCAM9RIeTN92pfd_iyhKw_Xi6zKhJ49ptnKzMG3vnNA",
    "userHandle": "internalUserId"
  },
  "type": "public-key",
  "clientExtensionResults": {},
  "authenticatorAttachment": "platform"
}

// Server Response
{
  "verified": true,
  "credentialDeviceType": "multiDevice",
  "credentialBackedUp": true
  // "userVerified": true (manually verified via debugger)
}
```

### Authentication (Conditional UI)

```json
// Authentication Options (Autofill)
{
  "allowCredentials": [
    {
      "id": "AXdreeORcwhCCiy8RMNW71xINK0",
      "type": "public-key",
      "transports": ["internal", "cable"]
    }
  ],
  "challenge": "L2raOSCqlLyFns5cFXgucNU__lZYWX3om4CnKdkYvrU",
  "rpId": "dev.dontneeda.pw",
  "timeout": 60000,
  "userVerification": "required"
}

// Authentication Response (Autofill)
{
  "id": "AXdreeORcwhCCiy8RMNW71xINK0",
  "rawId": "AXdreeORcwhCCiy8RMNW71xINK0",
  "response": {
    "authenticatorData": "PdxHEOnAiLIp26idVjIguzn3Ipr_RlsKZWsa-5qK-KAZAAAAAA",
    "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uZ2V0IiwiY2hhbGxlbmdlIjoiREtUTGVLQ1otZm14eXZNMHVoTzBuS3NrT0R6NmY0dWtYellQcy12TDZVRSIsIm9yaWdpbiI6Imh0dHBzOi8vZGV2LmRvbnRuZWVkYS5wdyJ9",
    "signature": "MEQCIFlGrrjwc4pjgHXSzWuFENLy7eQFUf64q2Ja4CoYx3VQAiAaB-uAApF7rF9tV2UhyDVnQ63Y98kkHWJU2Q35IaHLhw",
    "userHandle": "internalUserId"
  },
  "type": "public-key",
  "clientExtensionResults": {},
  "authenticatorAttachment": "platform"
}

// Server Response (Autofill)
{
  "verified": true,
  "credentialDeviceType": "multiDevice",
  "credentialBackedUp": true
  // "userVerified": false (manually verified via debugger)
}
```

## Observations

### Registration

- Requesting `"direct"` attestation still leads to a successful execution but generates a `fmt: "none"` response
- The authenticator returns `["internal", "cable"]` for transports
- The `credProps` client extension is still not supported
- The "backup eligibility" authenticator data flag returns `true`
- The "backup status" authenticator data flag returns `true`
- Requiring user verification returns `uv: true`

### Authentication

- Requiring user verification during **typical WebAuthn authentication** (i.e. clicking a button to invoke the API call) returns `uv: true`
- Requiring user verification during **conditional UI authentication** returns `uv: false` for some reason, despite both involving Touch ID
