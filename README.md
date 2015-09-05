treestr
-------

An over-engineered solution to an unimportant problem, by [Allison
Parrish](http://www.decontextualize.com/)

This is really raw software and it's probably not suitable for use by anyone
other than me. I just wanted it on Github so I can include it in
`pip` requirements files.

##Motivation and examples

Say you start out with a series of strings, like:

    >>> parts = ["it was the best of times, it was the worst of times",
    ...     "happy families are all alike",
    ...     "once upon a time and a very good time it was"]

... and then you do some random recombinations of these strings to make
something new and interesting:

    >>> from random import sample, randrange
    >>> first, second = sample(parts, 2)
    >>> result = first[:randrange(len(first))] + second[randrange(len(second)):]
    >>> print(result) 
    once upon a time and the best of times, it was the worst of times

The resulting string is amusing, but there's no way to tell *which* strings
from the original list were the ultimate sources of the string's component
parts. It might be helpful in some circumstances to retain this information,
such as for the purpose of attribution, or to make further decisions about how
the strings should be combined with other strings, etc. etc. etc. But working
with strings this way is *so easy* and it would be a drag to introduce an
entirely new abstraction just to keep this metadata with the string.

To solve this problem, I give you... the `treestr`.

    >>> parts = [t("it was the best of times, it was the worst of times"),
    ...     t("happy families are all alike"),
    ...     t("once upon a time and a very good time it was")]
    >>> first, second = sample(parts, 2)
    >>> result = first[:randrange(len(first))] + second[randrange(len(second)):]
    >>> print(result)
    it was the best of times, it was families are all alike
    >>> print(result.parents)
    ('it was the best of times, it was ', 'families are all alike')
    >>> print(result.parents[0].parents)
    ('it was the best of times, it was the worst of times',)
    >>> print(result.parents[1].parents)
    ('happy families are all alike',)

The `treestr` class is a subtype of `str`, but it adds an attribute `parents`
that is a tuple of all of the strings that the string is derived from. You can
use this to trace the ultimate source of any given string. The only limitation
is that `treestr` only works with methods on the `str` type (including
operators implemented with special methods like `__add__`, `__getitem__` and
`__mod__`). If you manipulate the string using other methods, you can create a
`treestr` object and set its parent manually:

    >>> import re
    >>> orig = "it was the best of times, it was the worst of times"
    >>> repl = t(re.sub("times", "programs", orig), parents=(orig,))
    >>> print(repl)
    it was the best of programs, it was the worst of programs
    >>> print(repl.parents)
    ('it was the best of times, it was the worst of times',)

##Keeping track of tags

The `treestr` also allows you to keep track of metadata on a string through a
mechanism called `tags`. The `tags` attribute on a `treestr` is a Python
`set()`; you can either set the tags using the `tags` parameter when
initializing the object, or add tags using the regular `.add()` method:

    >>> test = t("hi there", tags={'foo', 'bar'})
    >>> print(test)
    hi there
    >>> print(test.tags)
    {'foo', 'bar'}
    >>> test.tags.add('baz')
    >>> print(test.tags)
    {'baz', 'foo', 'bar'}

The `.rtags()` method of a `treestr` object recursively constructs a set of
tags for the given `treestr` object *and* the tags of all of its parents. This
allows you to easily, e.g., get a list of authors whose work is included in
your remixed string:

    >>> parts = [t("it was the best of times, it was the worst of times", tags={'dickens'}),
    ...     t("happy families are all alike", tags={'tolstoy'}),
    ...     t("once upon a time and a very good time it was", tags={'joyce'})]
    >>> first, second = sample(parts, 2)
    >>> result = first[:randrange(len(first))] + second[randrange(len(second)):]
    >>> print(result)
    once upon a time and a very  best of times, it was the worst of times
    >>> print(result.rtags())
    {'joyce', 'dickens'}

Easy peasy, and if you're just using regular string methods, you don't have to
change any of your code!

##The strange case of `.join()`

You can mix and match regular `str` objects with `treestr` objects, no problem.
But be aware of `.join()`: if you want it to work properly, you need to call
the `.join()` method of a `treestr` object (otherwise the result will be a
regular `str`):

    >>> result = t(' ').join([first[:5], second[-5:]])
    >>> type(result)
    <class 'treestr.treestr'>
    >>> result.rtags()
    {'joyce', 'dickens'}
    >>> print(result)
    once  times

##Installation

Install from Github with `pip` like so:

    $ pip install git+https://github.com/aparrish/treestr#egg=treestr

Not putting this on PyPI until I'm convinced it actually has utility for anyone
other than me.

##Compatibility

Only tested with Python 3.4. (There's some stuff in Python 3.4 that makes it
easier to subtype `str` and I'm too lazy to backport everything.)

##License

Copyright (c) 2015, Allison Parrish
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of pronouncing nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
