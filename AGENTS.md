# Project working rules

- Use the shared `simulator` engine for new dynamics; add local chemistry hooks
  and JSON scenarios rather than another simulation scheduler.
- Follow `.agents/skills/local-chemistry-research/SKILL.md` for chemistry research.
  Record hypotheses, decisions, failures, configurations and code provenance.
  Update the branch tree, research log, priorities and maturity at each batch.
- Alternate mechanism exploration with unification and simplification. Once
  mechanisms work separately, prioritize transfer and coupling under common laws;
  record a concrete blocker when further isolated exploration is needed.
- Freeze each candidate's elementary alphabet, local laws and parameters during
  comparison campaigns. Track variants, chemical reference cases, regressions
  and added primitive/helper complexity as specified in the research skill.
- Distinguish separate models, common laws tested separately, and coupled
  functions in one bath. A shared engine is not evidence of common chemistry;
  test that a synthesized product works in the next process without changing laws.
- Membrane assembly must be tested from isolated composite molecules. Folding a
  prepared ribbon is a separate control, not proof of molecular self-assembly.
- Keep laws local: no contour, complete sequence, complete genome or biological
  aggregate identity in the dynamics. Observers may identify these afterwards.
- Commit code, laws, configurations, recipes and research documents. Keep raw
  trajectories, checkpoints, full run results and bulk experiment data local,
  excluded by `.gitignore`. Never delete local evidence just to keep Git small.
- Preserve old recipe sources and hashes. Generate new run folders for changes.
- Run checks appropriate to the change. At batch handoff give a very brief,
  honest maturity assessment, distinguishing separate models from common chemistry.
- The user authorizes useful local commits at the end of a batch. Review staged
  paths so experimental data and unrelated user changes are excluded.
- **Never push to the remote repository. The user performs all pushes.**
