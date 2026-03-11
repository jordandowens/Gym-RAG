FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    git build-essential cmake curl && \
    rm -rf /var/lib/apt/lists/*

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp
WORKDIR /llama.cpp

# Build with CUDA support
# Use CUDA stub libs for link-time inside the image; real libcuda comes from the host at runtime.
RUN set -eux; \
    export CUDA_HOME=/usr/local/cuda; \
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs; \
    export LIBRARY_PATH=/usr/local/cuda/lib64/stubs; \
    # Ensure libcuda.so.1 resolves during link against stub libs
    if [ ! -e /usr/local/cuda/lib64/stubs/libcuda.so.1 ]; then \
      ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1; \
    fi; \
    cmake -B build \
      -DGGML_CUDA=ON \
      -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
      -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
      -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath,/usr/local/cuda/lib64/stubs" \
      -DBUILD_SHARED_LIBS=ON \
      -DGGML_BUILD_TESTS=OFF \
      -DGGML_BUILD_EXAMPLES=OFF \
      -DLLAMA_BUILD_TESTS=OFF \
      -DLLAMA_BUILD_EXAMPLES=OFF \
      -DLLAMA_BUILD_SERVER=ON \
      .; \
    cmake --build build --config Release -j $(nproc)

# Expose the HTTP server port
EXPOSE 8080

# Prefer real CUDA libs at runtime (provided by NVIDIA runtime on the host)
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64

# Run the server with GPU acceleration
CMD ["./build/bin/llama-server", \
     "--model", "/models/llama-3.1-8b-instruct-q4_k_m.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--n-gpu-layers", "999"]
