Python Package Inspector
========================

This [django](https://www.djangoproject.com/) project was inspired by the
[django-cbv-inspector](https://github.com/refreshoxford/django-cbv-inspector)
produced at [Refresh Oxford](http://refreshoxford.co.uk/) in Feb 2012. My aim
for this project is for it to be a generic python package inspector (i.e.: for
making python code easier to browse and understand). In particular, I aim to
clarify inheritance by showing classes with all the properties they have
inherited from elsewhere, as this makes multiple inheritance easier to cope
with for me.

As the nature of python allows for some pretty liberal nested definitions, it
makes sense to me to store the data in a graph based database, and --- probably
just because I want to play with it --- I'll be using [neo4j](http://neo4j.org/)
for this. Also, as I understand it, [pypy](http://pypy.org/) offers the only
true python [sandboxing](http://doc.pypy.org/en/latest/sandbox.html), so that's
what I'll attempt to use for importing all that scary untrusted code :)
