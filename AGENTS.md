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
- Apply `research/LOCALITY_AUDIT.md`: state each rule's bounded neighborhood and
  helper cost; keep initialization/measurement labels out of reactions. Test no
  observer feedback and declare external forcing. Do not encode a whole biological
  function in a primitive type or count prepared structures as emergent results.
- Commit code, laws, configurations, recipes and research documents. Keep raw
  trajectories, checkpoints, full run results and bulk experiment data local,
  excluded by `.gitignore`. Never delete local evidence just to keep Git small.
- Preserve old recipe sources and hashes. Generate new run folders for changes.
- At research handoff assess project health, future blockers and design effort
  in `research/PROJECT_HEALTH.md`. Distinguish automatic trials from conceptual
  changes; set decisive milestones and revisit a candidate that stops converging.
- Keep the causal architecture, interaction/noninteraction contracts and particle
  budget current. Include imports, waste, membrane insertion, every added tool's
  gene and renewal, off-target reactions and mixed-environment controls. A closed
  dependency graph is a conditional specification, not evidence of viability.
- Run checks appropriate to the change. At batch handoff give a very brief,
  honest maturity assessment, distinguishing separate models from common chemistry.
- Follow `research/KINETICS_AND_PERFORMANCE.md`: distinguish no encounters,
  ineligible contacts, reaction waiting and product instability. Keep no-event
  runs right-censored; freeze horizons and report selected follow-ups as selected.
  Long campaigns must expose status, checkpoints and source-frozen recipes.
- The user authorizes useful local commits at the end of a batch. Review staged
  paths so experimental data and unrelated user changes are excluded.
- **Never push to the remote repository. The user performs all pushes.**
