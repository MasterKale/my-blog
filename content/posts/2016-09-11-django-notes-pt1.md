+++
date = "2016-09-11T01:00:00-07:00"
description = "In which I learn to preload JSON on the server to reduce page load times."
categories = ['django']
keywords = ['django', 'rest', 'framework']
title = "Django Notes: Part 1"
hasCode = true
+++

I spent the better part of Saturday working on my latest personal project. Things were going alright within the limitations of using Django for routing and page rendering. I occasionally rued my decision to eschew Angular for a traditional Django app, but I forced myself to adapt and was making good progress.

Things took a turn for the interesting, though, when a good friend of mine clued me in on how I might implement a kind of "[isomorphic](http://isomorphic.net/)" website. That is, how to prepare an initial JSON payload on the server and inject it into the page in a way that allows for it to be displayed via Javascript after the page is loaded. As an added bonus, page content could be refreshed afterwards with simple AJAX calls to REST API endpoints exposing the very same class used to generate the initial JSON payload.

It sounds a little unorthodox, but the end goal is that your pages won't experience two loads: the first one when the server delivers the initial HTML, JS, and CSS, and the second as the SPA framework bootstraps itself.

The trick, I've found, is that you need to first set up a ViewSet to simplify the process of generating and returning JSON suitable for injection into `<script></script>` tags within a template. I've had initial success implementing one fairly cleanly with [Django Rest Framework](http://www.django-rest-framework.org/)'s (DRF) [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset), as well as a few [ModelSerializers](http://www.django-rest-framework.org/api-guide/serializers/#modelserializer) to help turn model instances into JSON. Once everything is in place, the real magic comes from calling the ViewSet programmatically to get back JSON:

```py
# CustomViewSet inherits rest_framework.viewsets.ModelViewSet
final_json = CustomViewSet.as_view({'get': 'list'})(request).render().content
```

Once you have your JSON, your can add it to the context that gets passed to the template:

```py
def get_context_data(self, **kwargs):
    context = super(SomeTemplateView, self).get_context_data(**kwargs)
    # Preload data for the initial view, Javascript will take care of the rest
    final_json = CustomViewSet.as_view({'get': 'list'})(self.request).render().content
    context['final_json'] = final_json
    return context
```

And then output it within the template:

```py
{% block scripts %}
<script>
    // Tell the template rendering engine that it's okay to include
    // `final_json` as-is, so it won't escape all of the quotes
    var finalJson = {{ final_json|safe }};
    // This'll run client-side and render the JSON elements to the page
    loadContent(finalJson);
</script>
{% endblock %}
```

In my experience the page appears to load pre-populated - that is to say, `loadContent()` loads everything so quickly that it seems as though the page and all of its visible content was rendered on the server. This is a much nicer experience than loading the page, waiting several seconds for the SPA framework to load, waiting for the initial API call to request the initial information, and then waiting for that information to get loaded into view.

As an added bonus, page content can be easily refreshed by making AJAX calls to the same `ModelViewSet`. The JSON response from the server can then be passed easily to `loadContent()`, just as it was when the page first loaded, to refresh the entire page without reloading it. In addition, I've noticed that page load times are also reduced because the logic within the template is kept to a minimum.

There's one more thing worth mentioning: AJAX calls made via Javascript will automatically inherit the Django session that keeps track of your authentication status. This means you don't have to pass any additional tokens or whatnot to the server when you make additional requests to the API endpoints. You'll definitely want to add a default permission class to your app's `settings.py`, though, to ensure that only authenticated users can access your API endpoints:

```py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

I have to admit, I have a newfound respect for Django and Django Rest Framework. With minimal changes to my existing codebase, I was able to create an almost "Angular-lite" type of webpage that avoids the issues of a long bootstrapping process that's indicative of an SPA. And hey, if this general technique is good enough for Twitter, then it's good enough for me!
