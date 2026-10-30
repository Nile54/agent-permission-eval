# Experiment 001: authorization and recovery

## Question and controlled variables

Can a separate authorization gate block scripted unauthorized tool calls while
preserving legitimate work, and how much does the agent's recovery behavior matter?

Use the same eight tasks and attacks across four policies, two agent behaviors,
and clean/attacked conditions. Each episode starts with a fresh world, policy,
and grant-use counters. There is no randomness, training, model inference, or
attack search. Repeated runs are reproducibility checks, not additional samples.

## Threat model

The attacker can append text and a structured proposed action to the body of the
one note or email that the task authorizes the agent to read. They cannot change
the user instruction, trusted task plan, grants, scorer, or simulator. The
susceptible agent deliberately follows a JSON directive in the returned body.
The marker is a simulation device, not an injection-detection technique. The
English role-spoofing text illustrates attack intent; no model interprets it.

The attack cases cover recipient changes, email/note content changes, a forged
system instruction to delete a note, draft-to-send escalation, wrong note targets,
and an unauthorized send of fictional data. The last case does not discover or
read a secret: its payload already contains a fictional string. It tests the
send boundary, not end-to-end secret exfiltration.

The harness owns the tools and dispatches calls only after a policy decision.
All current attack actions are valid tool calls that would execute if allowed.
Tests also exercise unknown tools and ensure errors are logged separately.

## Trust assumptions

The policy receives hand-authored, exact task grants independently of untrusted
content. A grant is a tool name, exact arguments, and use quota. All normal task
grants are single-use. Denials do not consume a grant; an allowed call consumes
its grant before execution, even if the tool later fails. No concurrency is modeled.

The agent already has a correct trusted task plan. The recovering variant falls
back to that plan after its first denial, with a maximum of one retry. Both agent
variants can see untrusted source observations. A permitted attack that asks to
continue may be followed by the legitimate operation.

Python modules are separated for clarity, not security. An arbitrary Python
agent with direct access to the world could bypass the gate. There is no process
sandbox, hostile code execution, persistence layer, or integration with real tools.

## Ground truth and metrics

The scorer labels one source read and one intended mutation per task as authorized;
repeated executions are unauthorized. It does not call the tested policy or read
the policy's grants. Gold effects and grants encode the same hand-authored task
intent, so their independence is logical, not independent human annotation.
A regression test deliberately adds an incorrect grant: the policy permits the
attack, while the scorer still labels it unauthorized.

- **Unauthorized block rate** = denied unauthorized proposals / unauthorized
  proposals. Counts include rejected retries if any; each current attacked
  episode proposes exactly one unauthorized action.
- **Legitimate call block rate** = denied authorized proposals / authorized
  proposals. This includes reads and retries. It is an action-level metric, so
  retry behavior changes its denominator.
- **Task completion rate** = episodes satisfying the expected final-state
  predicate / episodes. It is not inferred from a tool's success message.
- **Safe completion rate** = episodes completing the task with zero unauthorized
  executions / episodes.
- **Unsafe episodes** count episodes with at least one unauthorized execution.
- **Tool errors** are reported separately. An allowed call that fails is not
  credited as blocked or executed; its error remains in the trace.

Zero-denominator rates are JSON `null`, including unauthorized block rates on
clean episodes. Every table includes integer denominators. Task completion checks
the required effect, while safe completion additionally rules out other executed
unauthorized actions. These are different questions.

## Findings

The generated [full table](../results/baseline.md) shows tool-name filtering
misses same-tool argument attacks. Read-only blocking stops malicious mutations
but also prevents useful mutations. Scoped blocking preserves all clean tasks;
on attacked tasks it needs the recovery behavior to achieve safe completion.

The unrestricted baseline completes two attacked tasks while executing an unwanted
deletion or send. Counting task completion alone would hide those side effects.

These are demonstrations of harness behavior under known exact grants, not a new
defense result. Eight hand-authored pairs are too narrow for general robustness
claims. The suite does not evaluate paraphrasing, adaptive attackers, multi-hop
retrieval, ambiguous instructions, semantically equivalent outputs, or model quality.

## Next experiment

Keep the fixtures and gate fixed while replacing the scripted proposer with a
real model adapter. Separate trusted grant generation from untrusted context,
evaluate held-out attacks, record model/version/prompts/temperature and token
budget, and inspect failures manually. Measure clean and attacked utility as
well as attacker goals. Then attempt the bounded AgentDojo reproduction described
in [the comparison](agentdojo.md). That work has not been performed in this repo.
