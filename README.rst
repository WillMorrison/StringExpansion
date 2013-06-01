===============
StringExpansion
===============

Introduction
------------

StringExpansion is a Python script that implements a syntax for expressing lists of
strings, and a generator to create those strings. It was inspired by the syntax
curl uses to expand lists of URLs, but could be applied to other things.
Although it is not as expressive as regular expressions, it has the benefit that
it will not allow one to generate infinitely expanding expressions.

Examples
--------

Ranges of numbers with optional zero padding are supported. For example,::
  file_[00-04]

would expand to::
  file_00
  file_01
  file_02
  file_03
  file_04

Lists of predefined strings can also be used. For example,::
  thing {one,two}

would expand to::
  thing one
  thing two

Backreferences are supported, allowing one sequence to be duplicated in multiple places. For example,::
  {foo,bar,baz}-const-(1)

would expand to::
  foo-const-foo
  bar-const-bar
  baz-const-baz

All these features can be mixed together to create powerful generators.::
  http://filehost.example.com/{vacation,photos-[2011-2012]}/(2)-[01-03].jpg

would expand to::
  http://filehost.example.com/vacation/vacation-01.jpg
  http://filehost.example.com/vacation/vacation-02.jpg
  http://filehost.example.com/vacation/vacation-03.jpg
  http://filehost.example.com/photos-2011/photos-2011-01.jpg
  http://filehost.example.com/photos-2011/photos-2011-02.jpg
  http://filehost.example.com/photos-2011/photos-2011-03.jpg
  http://filehost.example.com/photos-2012/photos-2012-01.jpg
  http://filehost.example.com/photos-2012/photos-2012-02.jpg
  http://filehost.example.com/photos-2012/photos-2012-03.jpg

