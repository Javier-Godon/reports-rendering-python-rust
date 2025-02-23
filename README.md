# Accelerating Python with Rust (PyO3)

This repository demonstrates how to leverage Rust to significantly enhance the performance of a Python project.

## Why Not Just Use a Compiled Language?

A natural question arises: Why not develop the entire application in a compiled language like Rust, Java, or Go from the start? The reality is that no single language is perfect for every use case. Often, business and technical constraints dictate language choices.

Consider a scenario where a team primarily working with Java needs to implement a solution for generating massive PDF and XLSX reports quickly. Given resource availability, the fastest way to develop the initial solution might be to use Python, a high-level language with extensive libraries. However, after deployment, performance becomes a critical issue. This is where Rust, integrated via PyO3, becomes a game-changer.

## Why Traditional Python Optimization Techniques Fall Short

There are numerous ways to optimize Python, but most are either too restrictive or only effective for isolated cases. Below, we evaluate common Python optimization approaches and their limitations.

### 1. NumPy
**Why it's not suitable:**
- Optimized for array computations, but not general-purpose Python performance enhancements.
- Operates under the Global Interpreter Lock (GIL), limiting true parallelism.
- Ineffective for complex algorithms requiring recursion, branching, or custom logic.

**Best use cases:**
- Numerical computations with arrays, matrices, and tensors.
- Vectorized mathematical operations.

### 2. Numba
**Why it's not suitable:**
- Works best for numerical computations but struggles with complex objects and business logic.
- Just-In-Time (JIT) compilation introduces overhead, making it less efficient for short-lived functions.
- Limited support for Python’s standard library.
- Parallel execution (@njit(parallel=True)) is restrictive compared to Rust’s fine-grained control over multi-threading.

**Best use cases:**
- Optimizing numerical loops over NumPy arrays.
- GPU acceleration (via CUDA) for select workloads.

### 3. MyPyC
**Why it's not suitable:**
- Limited performance improvements compared to Rust or C extensions.
- Only works with fully type-annotated Python code.
- Still constrained by the GIL, limiting true parallelism.

**Best use cases:**
- Speeding up type-annotated Python applications.
- Optimizing Python modules without major refactoring.

### 4. Cython (.py and .pyx)
**Why it's not suitable:**
- Significant performance gains require extensive manual optimization.
- Runs under the GIL unless explicitly disabled, limiting multi-threading benefits.
- Generates Python-specific C extensions, making portability difficult compared to Rust.

**Best use cases:**
- Writing high-performance Python extensions.
- Optimizing existing Python codebases with minimal changes.

### 5. Cython (.pyx) with C or C++
**Why it's not suitable:**
- Manual memory management introduces risks of memory leaks and segmentation faults.
- Multi-threading is error-prone and complex to implement safely.

**Best use cases:**
- Performance-critical Python extensions where C/C++ optimizations are required.
- Interfacing with existing C/C++ libraries.

### 6. Taichi
**Why it's not suitable:**
- Primarily designed for high-performance numerical simulations, not general-purpose optimization.
- Limited scope beyond computational physics and graphics workloads.

**Best use cases:**
- GPU-accelerated simulations in physics and graphics.
- Differentiable programming (e.g., physics-informed machine learning).

## Why PyO3 and Rust Were the Right Choice

1. **Fine-grained control over performance** – Rust provides explicit control over memory, threading, and optimization, avoiding Python’s dynamic overhead.
2. **True multi-threading** – Unlike Numba, MyPyC, and Cython, Rust’s compiled binaries can execute outside the GIL, enabling real parallelism.
3. **Memory safety without garbage collection** – Rust ensures safe memory management without the need for a garbage collector.
4. **General-purpose optimization** – Unlike NumPy and Taichi, which are domain-specific, Rust can optimize arbitrary Python code effectively.
5. **Seamless interoperability with Python** – PyO3 allows Rust to be integrated into Python projects with minimal friction.

## Beyond "Hello World"

Most online tutorials on PyO3 focus on simple use cases like optimizing basic loops or specific computations with native Python libraries. These approaches often assume:
- The optimization applies to isolated, simple functions.
- There are idle execution periods (e.g., I/O operations) that can be leveraged for performance gains.

This repository goes beyond these basic examples by:
- Demonstrating efficient multi-threading and core utilization via Rust.
- Keeping the core application logic and external libraries in Python.
- Using FastAPI for REST API design, ensuring a scalable and practical real-world solution.

By integrating Rust into a Python project strategically, we achieve significant performance gains while retaining Python’s flexibility and ecosystem. 🚀

## Annex: Creating an Image and a Dagger Pipeline

In addition to everything mentioned above, when incorporating Rust into a Python project, you must consider the compilation process. To provide a complete and fully functional example, we also include this section.

In our case, we provide the necessary `Dockerfile` to generate the image, as well as the pipeline (using Dagger) to integrate the project into the CI/CD process.

You will find the pipeline in the `dagger_pipeline` folder, which is written in Python, and a README.md to help you. Later, we will integrate it into our CD process.


