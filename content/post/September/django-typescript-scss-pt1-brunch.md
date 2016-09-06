+++
date = "2016-09-06T19:00:00-07:00"
description = "For when you absolutely, positively cannot live without TypeScript and SASS (and I don't blame you!)"
categories = ['howto', 'django']
tags = ['django', 'typescript', 'sass', 'scss', 'brunch.io']
title = "Django, TypeScript and SCSS, Part 1: Brunch.io"

+++

A recent discussion with some developer friends regarding Django-rendered websites versus Single-Page Applications (SPAs) got me thinking: how difficult would it be to integrate TypeScript and SCSS into a traditional Django app? I'd grown accustomed to having them around thanks to Angular2 development the last few months, and I wanted to see if I could create a "traditional" website that still leveraged these amazing frameworks.

Before proceeding, I set some goals for myself:

1. Enable the inclusion of these technologies without substantially changing how JS and CSS files are included within Django templates (I want to be able to use `{% static ... %}` tags in my templates to "namespace" styles and scripts)
2. Allow for developers to group .ts and .scss files by page, instead of by filetype. My experience as an Angular developer inspired me to follow this methodology as it allows for a more modular directory structure that encourages code re-usability.

My first thought was to approach minification/uglification/etc... from the server side. I'd worked with [django-pipeline](https://github.com/jazzband/django-pipeline) before, so I started there and added in [django-pipeline-typescript](https://github.com/Bogh/django-pipeline-typescript). [A couple of tweaks](https://github.com/Bogh/django-pipeline-typescript/pull/1) later (to get it to work with the newest version of pipeline), django-pipeline-typescript seemed to have potential. When I ran `manage.py runserver`, my TypeScript files were successfully transpiled into vanilla JS, and were then bundled into `.js` files to be added into templates with `{% static %}` tags.

Sadly, **django-pipeline was _not_ the solution I hoped it would be.** Changes to `.ts` files required me to restart the dev server before they would go live, and when I ran `manage.py collectstatic` TypeScript and SCSS Files would both get swept up. Adding `--ignore *.ts --ignore *.scss` to `collectstatic` wasn't an option either, as it turns out that Pipeline processes files _after_ they've been copied into `STATIC_ROOT`. This meant I'd have to add an extra step to the build process that would somehow strip out all TypeScript and SCSS files from the collected static files before deployment. This, combined with the lack of live reloading when I made a change to these files, had me consider alternative methods.

A bit of research later, I decided that incorporating a front end builder like Grunt or Webpack would be the best course of action in the long run. Simply put, these tools are designed specifically for what I'm doing, so why not go with the flow?

So of course I took a sidepath and tried to find a solution that incorporated [Brunch.io](http://brunch.io/)!

If you've never heard of it before, Brunch is a heavily opinionated build pipeline that allows you to get up and running with about a dozen lines in a config file. I'd considered using this for an Angular2 project a few months back, but then [angular-cli](https://github.com/angular/angular-cli) came onto the scene and Brunch got put on the backburner. This seemed as good a time as any to take Brunch for another spin.

A few hours of experimentation later, I ended up with the [django-brunch-ts-scss](https://github.com/MasterKale/django-brunch-ts-scss) repo. This creatively-named proof-of-concept is a sample Django project that accomplishes almost all of the goals I had set out for myself. I was able to define separate TypeScript files with code intended for individual pages, I could import modules as usual, and I could use SCSS to its fullest extent.

Unfortunately, the project suffers from the following issues:

1. `.ts` and `.scss` files are transpiled appropriately, but they get mashed into a single `app.js` and `app.css` respectively. This means I have to A) use statements like `require('index/index.ts')` in my templates to trigger page-specific code, and B) make a concerted effort to namespace my CSS.
2. [Unit testing support doesn't really exist in Brunch](http://brunch.io/docs/testing). I'd have to build the files and then test them externally with another command. I _could_ incorporate this via a `package.json` testing script, but that's a task for another time.

In the end, while I'm not entirely pleased with the results of this experiment, [django-brunch-ts-scss](https://github.com/MasterKale/django-brunch-ts-scss) repo _does_ work and it _does_ prove that TypeScript and SCSS can be easily incorporated into a Django project without negatively impacting the base Django experience.

---

Tune in next time for Part 2, where I'll demonstrate this same concept but with the popular [Webpack](https://webpack.github.io/) instead.