#goals
 * establish coding conventions that make sense
 * establish file naming conventions that make sense.

#general principles
In keeping with Python's design principles, we will assume that code is read more than it is written, and thus readable is preferable to shorter.

In general, names should be lowercase with underscores separating them. Class names in which there is an intent that the classes will be used for testing (i.e., subclasses of exceptions or classes that will be used with isinstance()) are classes that may be CamelCase.

#method naming
Methods with no arguments should be present-tense verbs.

Methods with one argument should either be prepositions, conjunctions, or verbs that take an object.

Methods with multiple arguments should be such that, with the possible exception of the first argument, if all other arguments are passed in via keyword arguments then this will be readable and provide an indication to the reader what each argument does. Where possible, default arguments will be provided.

#class naming
Classes are treated differently depending on their intended use.

If classes are going to be used in conjunction with "isinstance" then they are to be capitalized (in camel case).

If classes are not going to be used in conjunction with "isinstance" then they should be lowercased with underscores.

#Use of \_\_init\_\_
Inheriting from

 * 	declare.initializers (or)
 * 	declare.values

is to be preferred to creating an \_\_init\_\_ method.

In general, it is preferable that those that use a module never explicitly invoke the constructor, but instead use (helper) function(s) in the module to create the object.

Functions that are named:

		new_***

(where *** is replaced by a lowercase underscore separated form of the class name) are the preferred way to create new instances.

All implementations of \_\_init\_\_ should call super() to pass it along. In general, however, implementing \_\_init\_\_ should be avoided.

The recommendation against the use of \_\_init\_\_ does not apply to "foundational" classes that would be used before the "declare" module could be imported (such as within the "declare" module itself, along with anything that would manipulate the search path so as to help find the "declare" moduel).

#Testing instances
(This section is under review because it is possible that the use of abstract base classes may provide a better approach to this, but more investigation is necessary.)

In general,	instead of using isinstance(), classes are to implement a is\_\*\*\* method that returns 1. This way creating another class that implements the same interface can be done, and it can be used instead with no type hierarchy issues.

Use declare.test_for.whatever (where 'whatever' is replaced with what is to be tested for) as much as possible to generate testing methods.

Assume that all variable/attribute access is to be done through methods on the object. (Directly accessing variables results in syntactic inconsistency, and prevents subclasses from restricting access later.)

(Properties are not to be used, because using them results in more inconsistencies.)

The exception to the above is when a class is explicitly a model.
