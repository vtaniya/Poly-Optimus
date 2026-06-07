"""
Poly-Optimus: Schoolbook Polynomial Multiplication
Time Complexity: O(N^2)
Syllabus Mapping: Standard iterative convolution of two polynomials.
"""

from typing import List

def multiply(poly1: List[int], poly2: List[int], q: int = 3329) -> List[int]:
    """
    Standard O(N^2) polynomial multiplication modulo q.
    Resulting polynomial degree is (len(poly1) + len(poly2) - 2).
    """
    n, m = len(poly1), len(poly2)
    result = [0] * (n + m - 1)
    
    for i in range(n):
        for j in range(m):
            result[i + j] = (result[i + j] + poly1[i] * poly2[j]) % q
            
    return result
