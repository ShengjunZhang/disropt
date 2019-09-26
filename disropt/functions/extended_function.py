import numpy as np
import warnings
from .abstract_function import AbstractFunction
from .utilities import check_input


class ExtendedFunction(AbstractFunction):
    """Function with extended variable

    .. math::

        f(x, y) = x

    with :math:`x\\in \\mathbb{R}^{n}, y\\in \\mathbb{R}^{m}`

    Args:
        fn (AbstractFunction): input function
        n_var: number of additional variables. Defaults to 1
        axis: axis along which the additional variables are appended. Defaults to -1 (the last valid one)

    Raises:
        TypeError: fn must be a AbstractFunction
        TypeError: n_var must be a positive int
        TypeError: axis must be int
    """

    # TODO implement __new__ to maintain existing structure (e.g. QuadraticForm, AffineForm)

    def __new__(cls, fn: AbstractFunction, n_var: int=1, axis: int=-1):
        instance = object.__new__(cls)
        if fn.is_affine:
            # TODO extend to non mono-dimensional case
            from .variable import Variable
            from .affine_form import AffineForm

            A, b = fn.get_parameters()
            A_new = np.vstack((A, np.zeros((n_var, A.shape[1]))))
            instance = AffineForm(Variable(A.shape[0] + n_var), A_new, b)
        elif fn.is_quadratic:
            # TODO extend to non mono-dimensional case
            from .variable import Variable
            from .quadratic_form import QuadraticForm

            P, q, r = fn.get_parameters()
            P_new = np.pad(P, ((0, n_var), (0, n_var)), 'constant')
            q_new = np.vstack((q, np.zeros((n_var, 1))))
            instance = QuadraticForm(Variable(P.shape[0] + n_var), P_new, q_new, r)
        return instance

    def __init__(self, fn: AbstractFunction, n_var: int=1, axis: int=-1):
        if not isinstance(fn, AbstractFunction):
            raise TypeError("fn must be a AbstractFunction object")
        
        if not isinstance(n_var, int) or n_var <= 0:
            raise TypeError("n_var must be a positive int")
        
        if not isinstance(axis, int):
            raise TypeError("axis must be int")
        
        # internal variables
        self.n_var = n_var
        self.axis = [i for i in range(len(fn.input_shape)) if fn.input_shape[i] > 1][axis]
        self.fn = fn
        self.input_shape_original = fn.input_shape
        self.eval_index = np.ix_(*tuple([range(i) for i in fn.input_shape]))

        # AbstractFunction variables
        new_shape = list(fn.input_shape)
        new_shape[self.axis] += n_var
        self.input_shape = tuple(new_shape)
        self.output_shape = fn.output_shape
        self.differentiable = fn.differentiable
        self.affine = False
        self.quadratic = False
    
    def _expression(self):
        expression = 'Extended Function({}, {} additional vars along axis {})'.format(self.fn._expression(), self.n_var, self.axis)
        return expression 

    @check_input
    def eval(self, x: np.ndarray) -> np.ndarray:
        return self.fn.eval(x[self.eval_index])
