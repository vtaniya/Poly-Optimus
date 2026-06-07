"""
Poly-Optimus: Benchmark Suite
Executes the Algorithmic Race and streams results to data_bridge.json.
"""

import time
import json
import random
import os
import schoolbook
import karatsuba
import ntt

def run_benchmark():
    N_VALUES = [256, 512, 1024, 2048]
    BRIDGE_FILE = os.path.join(os.path.dirname(__file__), "..", "data_bridge.json")
    
    # Clear previous results
    with open(BRIDGE_FILE, "w") as f:
        json.dump([], f)
        
    results = []

    for n in N_VALUES:
        print(f"Benchmarking N={n}...")
        
        # Generate random coefficients
        p1 = [random.randint(0, 3328) for _ in range(n)]
        p2 = [random.randint(0, 3328) for _ in range(n)]
        
        # 1. Schoolbook
        start = time.perf_counter_ns()
        _ = schoolbook.multiply(p1, p2)
        end = time.perf_counter_ns()
        school_time = (end - start) / 1000.0 # to microseconds
        
        # 2. Karatsuba
        start = time.perf_counter_ns()
        _ = karatsuba.multiply(p1, p2)
        end = time.perf_counter_ns()
        karat_time = (end - start) / 1000.0
        
        # 3. NTT
        start = time.perf_counter_ns()
        _ = ntt.multiply(p1, p2)
        end = time.perf_counter_ns()
        ntt_time = (end - start) / 1000.0
        
        entry = {
            "N": n,
            "Schoolbook": school_time,
            "Karatsuba": karat_time,
            "NTT": ntt_time
        }
        
        results.append(entry)
        
        # Atomic-ish write to bridge file
        with open(BRIDGE_FILE, "w") as f:
            json.dump(results, f, indent=4)
            
        print(f"Completed N={n}: School={school_time:.2f}us, Karat={karat_time:.2f}us, NTT={ntt_time:.2f}us")
        
        # Small sleep to simulate realistic heavy compute for UI smoothness
        time.sleep(0.5)

if __name__ == "__main__":
    run_benchmark()
