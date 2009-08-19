d51_django_auth
===============
This is a package that'll eventually hook into all of the popular means of
distributed authentication.  The first pass is Facebook Connect, which works.

Installation notes
------------------
'''TODO'''

    AUTHENTICATION_BACKENDS = (
        'd51_django_auth.backends.FacebookConnectBackend',
        'django.contrib.auth.backends.ModelBackend',
    )



How to run the tests
--------------------
d51_django_auth is a Django application, so it needs Django and a few various
third-party libraries to run.  This repository ships with the scripts
necessary for buildout to build the various pieces necessary for testing.

To run the tests, clone the repository, change into the repository directory
and run the following commands:

    prompt> python bootstrap.py
    ... will initialize buildout ...
    prompt> bin/buildout
    ... will take a few minutes while it downloads Django ...
    prompt> bin/django test d51_django_auth

You can also test it directly inside your Django project, by adding
`d51_django_auth` to the `INSTALLED_APPS` setting and running the following
command:

    prompt> python manage.py test d51_django_auth






Known Issues
------------
This is one day's work, hardly enough time to know what issues there are.
It's in the "works for me" category of code.

That said, I've yet to look at how to adjust the included admin's logout
button to work.  If you're interested in tackling it, you need to add an
onclick handler that calls FB.Connect.logoutAndRedirect() and pass in the
href for the admin.

