d51_django_auth
===============
This is a package that'll eventually hook into all of the popular means of
distributed authentication.  The first pass is Facebook Connect, which works.

Known Issues
------------
This is one day's work, hardly enough time to know what issues there are.
It's in the "works for me" category of code.

That said, I've yet to look at how to adjust the included admin's logout
button to work.  If you're interested in tackling it, you need to add an
onclick handler that calls FB.Connect.logoutAndRedirect() and pass in the
href for the admin.

