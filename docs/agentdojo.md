# Relationship to AgentDojo

This project is a small original simulation experiment, not an AgentDojo
reproduction, integration, or comparable benchmark score. No AgentDojo code or
datasets were copied, and no AgentDojo run has been performed.

[AgentDojo's paper](https://arxiv.org/abs/2406.13352) studies tool-using LLM agents
exposed to untrusted data and provides an extensible environment for tasks,
attacks, and defenses. The paper describes 97 realistic tasks and 629 security
test cases; those are paper-version figures, not a verified count of the current
repository. The [official repository](https://github.com/ethz-spylab/agentdojo)
and [documentation](https://agentdojo.spylab.ai/) provide benchmark usage and
extension instructions. Sources consulted October 29, 2026 (America/Los_Angeles).

| Aspect | This experiment | AgentDojo reference |
|---|---|---|
| Proposer | Deterministic scripted agent | LLM agent evaluation framework |
| Environment | In-memory notes and email | Realistic tasks with tool-using agents |
| Attacks | Eight fixed structured directives | Extensible attack evaluation |
| Defense under study | Tool-name versus exact argument authorization | Extensible agent pipelines and defenses |
| Utility measurement | Required final-state effect, clean and attacked | User task evaluation |
| Security measurement | Unauthorized proposals and executions | Attacker objectives/security tests |
| Interpretation | Harness sanity checks and controlled recovery ablation | Established benchmark for broader experiments |

The distinction between an unauthorized-action label and an attacker-goal success
predicate matters: an attacker may need several calls, and one blocked call does
not automatically prove that the entire attacker goal failed. This simulation
has single malicious calls; it does not supply AgentDojo-equivalent attack success.

## Bounded reproduction plan

1. Pin an AgentDojo commit and its dependencies in a separate environment. Record
   the exact model, prompts, defense settings, task IDs, and run budget. Its
   documentation warns that the package API may change.
2. Start with workspace user tasks 0 and 1, first without an attack. Verify the
   task predicates and traces by hand before interpreting aggregate utility.
3. Repeat with the documented `tool_knowledge` attack and `tool_filter` defense,
   plus an undefended comparison. Confirm flags against the pinned version's
   `--help`; the repository README provides an example for these task IDs.
4. Add a custom policy-gate pipeline only after understanding the baseline.
   State exactly how grants are obtained without reading attacker-controlled
   instructions. Treat manual exact grants as an explicitly privileged condition.
5. Report per-task user success and attacker success alongside action decisions,
   repeat stochastic trials, publish configurations and sanitized traces, and
   investigate discrepancies before increasing the task set.

Do not compare this repo's 8/8 counts numerically with published AgentDojo
percentages: the agents, attack construction, permissions, and tasks differ.

## Reference

Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer,
and Florian Tramèr. *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection
Attacks and Defenses for LLM Agents*. NeurIPS Datasets and Benchmarks, 2024.
[Paper](https://arxiv.org/abs/2406.13352) ·
[Code](https://github.com/ethz-spylab/agentdojo).
