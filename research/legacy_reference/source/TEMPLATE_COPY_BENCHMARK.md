# Template-copy benchmark notes

The tuned default uses the exact-copy sequence `011010`, 48 free monomers of each symbol, a 100 x 60 periodic world, a 12-second capture phase, and a 4-second release phase.

The success criterion is deliberately stronger than the first smoke test: at least four exact six-bit chains must be fully detached from template bonds. The original seed chain counts as one of the four chains.

A native optimized headless build was run for deterministic seeds 1 through 500. Every run reached the criterion within 2,225 simulation steps, corresponding to at most 44.5 simulated seconds with `dt = 0.02`. The median and 90th-percentile success time were both 28.5 simulated seconds.

The CTest smoke test uses 16 fixed seeds and requires every seed to reach four detached exact chains within 2,500 steps. This is intended as a regression test, not as a claim that every possible parameter setting or random seed will replicate successfully.
