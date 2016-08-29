+++
title = "Adding email functionality to a static site with Formspree"
date = "2016-08-29T08:00:00-07:00"
description = "It's easier than you think to set up emailing from a statically-generated site!"
categories = ['howto']
tags = ['static site', 'formspree']

+++

Github Pages is incredibly useful for hosting pages with largely static content. Create a repo, add a `CNAME` file with the desired domain name, point DNS to Github and boom, you're done! Site changes are as simple as a `git push`, too, making it a quick and painless way to get a basic, informational website up and running.

The downside to this is that you have absolutely no access to server-side scripts of any kind. That basic PHP emailer script you've used before to power Contact Us forms? Not an option here.

Fortunately for you I stumbled upon a free service called [**Formspree**](https://formspree.io/).

Formspree's premise is simple: whenever a visitor fills out and submits a `<form>` on your site, Formspree will email you a message containing whatever values were entered:

![Formspree-generated email containg form values](/images/adding-email-to-static-sites-with-formspree/formspree-email.png)

Integrating it into your site is as simple as adding `https://formspree.io/your@email.com` into your form's `action` attribute:

```
<!-- Make sure you replace `your@email.com` with an actual email address -->
<form action="https://formspree.io/your@email.com" method="post">
    <label for="name">Name:
        <input type="text" name="name" id="name" />
    </label>
    <label for="email">Email:
        <input type="email" name="email" id="email" />
    </label>
    <button type="submit">Send</button>
</form>
```

The next step is to confirm your email address. Fill out and submit your form once. You'll be taken to the Formspree website and asked to check your email:

![Formspree Confirmation Message](/images/adding-email-to-static-sites-with-formspree/formspree-confirm.png)

In your inbox you'll find a confirmation e-mail like this one:

![Formspree Confirmation Email](/images/adding-email-to-static-sites-with-formspree/formspree-confirm-email.png)

Just click the **Confirm Form** button and you're done! From this point on Formspree will send you an email every time the form is filled out:

![Typical Formspree Email](/images/adding-email-to-static-sites-with-formspree/formspree-email.png)

There are some advanced features you can enable, including setting reply-to and CC addresses, email subject text, and a few more. Check out the Formspree site for more information: https://formspree.io/

As far as caveats go, you're limited to 1000 form submissions per month. If you need to handle any more than that then Formspree offers Formspree Gold for $9.99/mo. In addition to unlimited submissions per month, it comes with a few other features like invisible emails and an archive of previous submissions.

If you're interested in adding Contact Us-like forms on a static site hosted on Github Pages, or if you just don't want to mess with server-side email scripts, then I'd highly recommend Formspree. It's dead-simple to set up and maintain, and it takes away a lot of the headaches of dealing with email on your own. Give it a try!