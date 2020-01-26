from numpy import linalg as la, random as rnd
import numpy as np
import theano.tensor as T

import pymanopt
from pymanopt.manifolds import Oblique
from pymanopt.solvers import TrustRegions


def rank_k_correlation_matrix_approximation(A, k):
    """
    Returns the matrix with unit-norm columns that is closests to A w.r.t. the
    Frobenius norm.
    """
    m, n = A.shape
    assert m == n, "matrix must be square"
    assert np.allclose(np.sum(A - A.T), 0), "matrix must be symmetric"

    manifold = Oblique(k, n)
    solver = TrustRegions()
    X = T.matrix()

    @pymanopt.function.Theano(X)
    def cost(X):
        return 0.25 * T.sum((T.dot(X.T, X) - A) ** 2)

    problem = pymanopt.Problem(manifold, cost)
    return solver.solve(problem)


if __name__ == "__main__":
    # Generate random problem data.
    n = 10
    k = 3
    A = rnd.randn(n, n)
    A = 0.5 * (A + A.T)

    # Solve the problem with pymanopt.
    Xopt = rank_k_correlation_matrix_approximation(A, k)

    C = Xopt.T.dot(Xopt)
    [w, _] = la.eig(C)

    # Print information about the solution.
    print('')
    print("diagonal:", np.diag(C))
    print("trace:", np.trace(C))
    print("rank:", la.matrix_rank(C))
