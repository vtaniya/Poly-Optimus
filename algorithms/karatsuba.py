"""
Poly-Optimus: Karatsuba Polynomial Multiplication
Time Complexity: O(N^log2(3)) ≈ O(N^1.58)
Syllabus Mapping: Divide and Conquer polynomial multiplication.
"""

from typing import List

def add_polys(p1: List[int], p2: List[int], q: int) -> List[int]:
    n = max(len(p1), len(p2))
    res = [0] * n
    for i in range(n):
        v1 = p1[i] if i < len(p1) else 0
        v2 = p2[i] if i < len(p2) else 0
        res[i] = (v1 + v2) % q
    return res

def sub_polys(p1: List[int], p2: List[int], q: int) -> List[int]:
    n = max(len(p1), len(p2))
    res = [0] * n
    for i in range(n):
        v1 = p1[i] if i < len(p1) else 0
        v2 = p2[i] if i < len(p2) else 0
        res[i] = (v1 - v2) % q
    return res

def multiply(p1: List[int], p2: List[int], q: int = 3329) -> List[int]:
    """
    Karatsuba multiplication modulo q.
    Reduces 4 multiplications to 3 at each recursion step.
    """
    n1, n2 = len(p1), len(p2)
    n = max(n1, n2)
    
    # Base case for small N
    if n <= 32:
        res = [0] * (n1 + n2 - 1)
        for i in range(n1):
            for j in range(n2):
                res[i+j] = (res[i+j] + p1[i] * p2[j]) % q
        return res

    # Padding to make n even
    m = (n + 1) // 2
    
    low1 = p1[:m]
    high1 = p1[m:]
    low2 = p2[:m]
    high2 = p2[m:]
    
    # Three recursive calls
    z0 = multiply(low1, low2, q)
    z2 = multiply(high1, high2, q)
    
    mid1 = add_polys(low1, high1, q)
    mid2 = add_polys(low2, high2, q)
    z1 = multiply(mid1, mid2, q)
    
    # z1 = (low1+high1)*(low2+high2) - z0 - z2
    z1 = sub_polys(z1, z0, q)
    z1 = sub_polys(z1, z2, q)
    
    # Combine results: z2*x^(2m) + z1*x^m + z0
    res_len = n1 + n2 - 1
    result = [0] * res_len
    
    for i, val in enumerate(z0):
        result[i] = (result[i] + val) % q
        
    for i, val in enumerate(z1):
        if i + m < res_len:
            result[i + m] = (result[i + m] + val) % q
            
    for i, val in enumerate(z2):
        if i + 2 * m < res_len:
            result[i + 2 * m] = (result[i + 2 * m] + val) % q
            
    return result
