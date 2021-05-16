+++
categories = ["netlify", "howto"]
date = "2019-01-20T18:00:00Z"
description = "The third piece of the Cloudflare and Netlify SSL puzzle."
keywords = ["ssl", "netlify", "cloudflare"]
title = "Using Cloudflare SSL Certificates with your Netlify Site"
hasCode = true
+++
Netlify gives you a lot of features in their free tier, including painless, LetsEncrypt-powered SSL certificates for custom domains. If you choose to manage your DNS through Cloudflare, though, then you may wish to generate an Origin Certificate through the Cloudflare dashboard (check the "🔒 Crypto" tab after selecting your domain) to secure your connection from Cloudflare to Netlify.

![](/images/Screen%20Shot%202019-01-20%20at%2012.31.13%20PM.png)After creating one of these certificates (using the default **PEM key format**), Cloudflare presents you with a **Origin Certificate** as well as the corresponding **Private Key**. These can be copy-pasted directly into the "Certificate" and "Private key" fields respectively in Netlify's custom certificate modal when you choose "Provide your own certificate" (or "Update custom certificate"):

![](/images/Screen%20Shot%202019-01-20%20at%2012.37.04%20PM.png)Unfortunately, Netlify _also_ requires a value for "Intermediate Certs". In these instances, Cloudflare provides their own [Origin CA Certificate](https://support.cloudflare.com/hc/en-us/articles/218689638) that contains all of the intermediate certificates needed to validate the identity of your generated Origin Certificate.

For that third field of the modal, you can simply copy-paste the below **RSA** version of their certificate into it:

```txt
-----BEGIN CERTIFICATE-----
MIID/DCCAuagAwIBAgIID+rOSdTGfGcwCwYJKoZIhvcNAQELMIGLMQswCQYDVQQG
EwJVUzEZMBcGA1UEChMQQ2xvdWRGbGFyZSwgSW5jLjE0MDIGA1UECxMrQ2xvdWRG
bGFyZSBPcmlnaW4gU1NMIENlcnRpZmljYXRlIEF1dGhvcml0eTEWMBQGA1UEBxMN
U2FuIEZyYW5jaXNjbzETMBEGA1UECBMKQ2FsaWZvcm5pYTAeFw0xNDExMTMyMDM4
NTBaFw0xOTExMTQwMTQzNTBaMIGLMQswCQYDVQQGEwJVUzEZMBcGA1UEChMQQ2xv
dWRGbGFyZSwgSW5jLjE0MDIGA1UECxMrQ2xvdWRGbGFyZSBPcmlnaW4gU1NMIENl
cnRpZmljYXRlIEF1dGhvcml0eTEWMBQGA1UEBxMNU2FuIEZyYW5jaXNjbzETMBEG
A1UECBMKQ2FsaWZvcm5pYTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
AMBIlWf1KEKR5hbB75OYrAcUXobpD/AxvSYRXr91mbRu+lqE7YbyyRUShQh15lem
ef+umeEtPZoLFLhcLyczJxOhI+siLGDQm/a/UDkWvAXYa5DZ+pHU5ct5nZ8pGzqJ
p8G1Hy5RMVYDXZT9F6EaHjMG0OOffH6Ih25TtgfyyrjXycwDH0u6GXt+G/rywcqz
/9W4Aki3XNQMUHNQAtBLEEIYHMkyTYJxuL2tXO6ID5cCsoWw8meHufTeZW2DyUpl
yP3AHt4149RQSyWZMJ6AyntL9d8Xhfpxd9rJkh9Kge2iV9rQTFuE1rRT5s7OSJcK
xUsklgHcGHYMcNfNMilNHb8CAwEAAaNmMGQwDgYDVR0PAQH/BAQDAgAGMBIGA1Ud
EwEB/wQIMAYBAf8CAQIwHQYDVR0OBBYEFCToU1ddfDRAh6nrlNu64RZ4/CmkMB8G
A1UdIwQYMBaAFCToU1ddfDRAh6nrlNu64RZ4/CmkMAsGCSqGSIb3DQEBCwOCAQEA
cQDBVAoRrhhsGegsSFsv1w8v27zzHKaJNv6ffLGIRvXK8VKKK0gKXh2zQtN9SnaD
gYNe7Pr4C3I8ooYKRJJWLsmEHdGdnYYmj0OJfGrfQf6MLIc/11bQhLepZTxdhFYh
QGgDl6gRmb8aDwk7Q92BPvek5nMzaWlP82ixavvYI+okoSY8pwdcVKobx6rWzMWz
ZEC9M6H3F0dDYE23XcCFIdgNSAmmGyXPBstOe0aAJXwJTxOEPn36VWr0PKIQJy5Y
4o1wpMpqCOIwWc8J9REV/REzN6Z1LXImdUgXIXOwrz56gKUJzPejtBQyIGj0mveX
Fu6q54beR89jDc+oABmOgg==
-----END CERTIFICATE-----
```

Afterwards, click "Install Certificate", and Netlify should accept your custom Cloudflare Origin Certificate:

![](/images/Screen%20Shot%202019-01-20%20at%2012.51.29%20PM.png)At this point, if you haven't already, you'll want to add a CNAME DNS record in Cloudflare that points to your Netlify site's domain name. Provided your DNS is already handled by Cloudflare, you should see the green SSL lock next to your domain in relatively short order:

![](/images/Screen%20Shot%202019-01-20%20at%201.01.14%20PM.png)
