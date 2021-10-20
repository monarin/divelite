AI HW for Machine Learning
- Large memory bandwidth
- Intense computing cycles


Cerebras
Framework -> LAIR(NN 4 Layers) -> Kernel Graph -> Execution Plan -> Executable


Frontier
Orion largest file system
Cray Programming Environment (CPE)
AMD ROCm 


Groq
Dynamic memory (data flow through layers)


SambaNova
Stochastic Nearest Neighbor Rounding - Probablistic rounding
High Resolution Image NN (No image batching/ tiling)
We break a batch into multiple micro batches. Once we get to the granularity of a single image, we feed the image to our HW. The compiler ensures that the activation maps that get generated for a high res image are managed appropriately. In case of high res images, because the activations can become large, the large DRAM memory (1 TB) that we have comes into use. We temporary store these large activations there. To hide the latency of DRAM execution we try to reuse as much of the activation as possible by scheduling multiple layers simultaneously


Perlmutter
CUDA-aware MPI (code may crash on a nod CUDA-aware MPI system)
CUDA Unified Memory


Aurora:
Intel-Cray
Intel Xeon and Intel GPUs (2 cpus/ 6 gpus)




