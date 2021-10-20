MPI

The threshold of “small message” depends on network and low-level library used. For most cases, message smaller than 8KB-16KB are considered as small.


Non-blocking Commuication


One-sided Communication
- Window concept
- RMA (Remote Memory Access)
- Passive Synchronization with Lock/Unlock

Exercises 
rma
From derived_type/stencil.c, replace send/recv with Fence and Put
solution:
The differences start in rma/stencil_fence_put.c line 132


Hyprid MPI (MPI+X)
MPI + Threads
Need to use TAG to make sure t_n matches with t_n on another process
See good example in slide for MPI Wait All

Exercises
Start from derived_datatype/stencil.c
Solution in threads/stencil_funneled.c

MPI + Gpu
Remote Direct Memory Access with UVA


MPI4
Session
- Less overhead for repetitive collective ops


