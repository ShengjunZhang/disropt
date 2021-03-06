.. _advanced_custom_functions:

Implementing custom functions
==============================

Custom functions can be easily implemented and integrated with alredy defined functions.
They can be built on the :class:`AbstractFunction` class, by overloading the :class:`eval` method. Subgradients, jacobians and hessians are usually automatically computed through autograd_. 
If they cannot be computed, then the :class:`_alternative_jacobian` and :class:`_alternative_hessian` method must be implemented too.

WARNING: jacobian of custom functions should be implemented by using the `numerator layout <https://en.wikipedia.org/wiki/Matrix_calculus>`_ convention.

.. _autograd: https://github.com/HIPS/autograd