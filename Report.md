# Say What You Did: Communication-Aware Robot Policies for Accessible Monitoring

Summer research report. Sampurn Bhowmick, Mina Huh, Amy Pavel. UC Berkeley, Pavel lab.

Code-as-Policies robots report failures they can predict and never failures they would have to observe. They have no execution feedback loop, and telling them the user is blind adds unverified claims instead of verification.

## 1. Research questions

RQ1. When a Code-as-Policies robot acts for a user who cannot watch it, does it communicate what actually happened?

RQ2. Does telling the model about the user (blind vs sighted, with or without an instruction to assist in monitoring) change that communication?

RQ3. Can outcome communication be made reliable, either by prompted rules or by communication primitives that carry their own verification? (Experiment generated, analysis pending.)

## 2. Background and motivation

In the lab's formative study, blind and low-vision participants said the hard part of working with a robot is not commanding it. It is knowing what happened after. A sighted user glances over and catches the error, but a BLV user waits for the robot to say something, and if it says nothing, the outcome is unknown. Participants averaged 7.5 errors per task in their own reports of what the robot had done while rating their situational awareness as high. So they were confident but wrong.

Two ways LLM robots are built today:

Code as Policies (CaP): the LLM writes a short Python policy that calls hand-written primitives for perception and action, and the code runs on the arm. 

Vision-language-action models (VLA): one network maps camera frames to motor commands. Neither is built to communicate. A VLA has no language output channel. CaP has exactly one, say(), which is an unchecked print statement. Nothing connects what the robot says to what happened.

We study CaP because the policy is code. We can read it, log every call, and score every claim against simulator ground truth. And because primitives are just functions in one namespace, communication can be added the same way perception and action were: a communication primitive sits next to get_obj_pos and put_first_on_second and gets called the same way.

The argument has three rungs, tested in order:

1. Identity labels alone. Put "the user is blind" in the prompt. Pilot result: near-identical code to the control. Null.
2. Prompted rules. Tell the model to verify after acting and report. Pilot result: verification-shaped code appears, but the model picks its own check, and that choice is a lottery. One cell produced six different strategies across runs, including is_obj_visible, a check that cannot detect a failed placement. Same prompt, different safety, depending on the draw.
3. Primitives. Put the correct check inside the communication function (say_verified). The model decides when to communicate. It never decides how to verify.

The baseline study below measures rung 0, what CaP does with no support at all, and rungs 1 and 2 at scale come next.

## 3. Method

### 3.1 Setup

RoboSuite + MuJoCo, simulated Panda 7-DOF arm, operational space controller. The LLM sees the standard CaP few-shot prompt (cached so it cannot drift mid-experiment), the scene's object list read from the simulator, and one command. It writes a policy. We execute the policy statement by statement on the arm, record every say() with its timing relative to physical actions, and score every claim against ground truth. Model for the run reported here: Claude Opus 4.8, pinned by id in a registry. A parallel Opus 4.5 run is in progress for a version comparison, because the experiment were previously being ran on Opus 4.5 and that produced more communication lines compared to when I updated Opus 4.8.

RoboSuite provides physics and a controller but no pick-and-place, so we wrote the movement layer: waypoint grasp-lift-place with grasp verification, plus per-scene ground-truth checks (is_placed, is_in_bin, is_in_bowl, is_on_plate, is_at, was_lifted). We also implemented the perception vocabulary CaP's own prompt demonstrates (parse_position, parse_obj_name, transform_shape_pts), deterministically. This matters for validity: any demonstrated function we failed to provide made correct policies crash, and the crash scored as a communication failure. Several of the eleven harness bugs we found were exactly this (section 6).

### 3.2 Conditions and profiles

Three policy conditions. Baseline: nothing added to the CaP prompt. Instructions: plain-language rules to verify after acting and report the outcome. Predefined primitives: five communication primitives added to the prompt and namespace, with the check built in.

Five user profiles, crossed with condition: empty (control), "the user is blind", "the user is sighted", and each identity plus "assist them in monitoring the task".

### 3.3 Tasks

All tasks are tabletop tasks pulled or modified from RoboSuite environments or the published CaP demo commands. 

Twenty tasks, ten short and ten long. Long means the goal needs at least two sequential manipulations, where one manipulation is one completed pick-place cycle, counted as the minimum a correct policy needs. 

16 of 20 commands are verbatim from tabletop tasks from RoboSuite environments or the published CaP demo commands, so the task set is not tuned to the hypothesis. RoboSuite ships no bowls and one fruit, so three tasks use procedurally built colored bowls and two shallow plates. The commands stayed verbatim.

Four tasks are modified on purpose, because benchmarks mostly measure success rate, so every benchmark task is solvable and none tests what a robot says about failure:

- S3, impossible task. "Put the red block on the purple block" with no purple block present. Tests whether the robot checks the environment before acting or performs arbitrarily. Purple, not blue, so the command does not prime the prompt's examples.
- S2, missing capability. "Lift the cube above the table." Possible task, but the action vocabulary has no lift-and-hold: placement always ends in a release at table height. Tests whether the robot notices an action constraint.
- L4, narration request. "Put the milk and the cereal each in its bin, telling me as you go." The trailing clause is ours. CaP's demo set has many narration tasks, but they are questions answerable before acting; this one requires communicating during action. It is the only command carrying a communication instruction, so it is reported separately and never pooled into baseline means.
- L9, two commands in one sentence. CaP issues commands turn by turn. L9 composes two consecutive CaP commands ("arrange the blocks in a square around the middle. then, make the square bigger.") into one instruction. Its ground truth is history-dependent: the shim snapshots poses after every placement, and success requires that a square existed mid-run and the final square is at least 1.25x larger.

### 3.4 Metrics

Per run: task success from ground truth, every utterance with its timing bucket (before any action, between actions, after the last action), and a verdict comparing each claim to reality. Failed runs partition into correct report, silent, false confirmation, and split by failure type: no attempt (zero physical actions, so the failure was knowable up front) versus attempted (the robot acted and the task still failed, so the failure only exists after acting). The split is computed per run from the action count, not from a task list, because the same task can be refused on one run and attempted on the next. Success runs partition into correct report, silent, false alarm. Every primitive call is counted by category (perception, verification, action, communication). All means carry sd over profile x task cells.

Separately, we open coded every utterance (section 5.4).

### 3.5 Scale

Baseline: 5 profiles x 20 tasks x 5 runs = 500 generated policies, all executed. 

Three-condition grid: 1,500 cells per model, of which the two new conditions (1,000 generations) are complete and awaiting execution and analysis.

## 4. Results, baseline

### 4.1 Failure reporting depends on when the failure is knowable

Of 500 runs, 309 succeeded and 191 failed. The 191 split into 50 no-attempt failures (all from S2 and S3, the two designed probes) and 141 attempted failures (natural grasp misses, wrong placements, mid-task errors, spread over 16 tasks).

No-attempt failures: 96% ± 8 correctly reported, up front, in plain language. "I don't see a purple block in the workspace." Attempted failures: 0% reported. 98% ± 13 silent, 2% ± 13 false confirmation. The user hears "Putting the cereal in the cereal bin," then nothing, forever.

That contrast, 96 vs 0, is the finding. The robot reports what it can predict before moving and nothing it would have to observe after. There is no execution feedback loop.

### 4.2 Success is also silent

98% ± 11 of successful runs end without any completion message. The only exception is L4, the task whose command asks for narration (33% ± 33 of its successes reported).

### 4.3 Speech volume is flat and timing is front-loaded

say() per run is 1.2 ± 0.8 overall, and exactly 1.0 with zero variance on most tasks in every profile. 93% ± 18 of all utterances happen before the robot has moved at all; under 1% come after the last action.

### 4.4 What the robot actually says: open coding

Of 642 utterances, only 115 distinct strings, which made full manual coding tractable. Four mutually exclusive speech acts:

- announce_intent, 88%. "Putting the red block on the green block." A restatement of the command, spoken before acting.
- claim_completion, 7%. The only speech act that ever occurs after an action.
- report_absence, 4%. All of S3.
- refusal_capability, 1%.

The dimension that matters is verifiability. An intent announcement is true no matter what happens next. 88% of everything the user hears makes no checkable claim. The robot is not silent. It talks constantly and says nothing falsifiable.

The act-by-timing table is nearly deterministic: refusals and absence reports are 100% pre-action, intent is 86% pre-action, and completion claims are the only post-action speech. The discourse structure is announce, act, stop.

### 4.5 Broken sentences can reach the user

8% of utterances end mid-reference: "Putting the red block to the left of the ". All from two tasks, and traced to an f-string whose variable resolved empty when a perception call returned nothing. The message text is assembled beside the check, not from it, so nothing catches a missing referent. This is one evidence for the claim/reference gap that motivates building messages from verified state, and it doubles as a user-facing symptom of a harness gap we then fixed.

### 4.6 A model-version observation

Live demos looked chattier than the grid. The cause was two uncontrolled variables in the demo tool: a hardcoded older model id (Opus 4.5) and a live-fetched prompt. Opus 4.5 narrates loops where 4.8 does not. After unifying both paths we kept the observation as a candidate finding: spontaneous narration is model-version dependent, which can itself be an argument that emergent communication cannot be relied on. A controlled 4.5 vs 4.8 comparison is planned as well.

## 5. Proposed solution

Two ways to add the missing feedback loop, run as prompt conditions against the same 20 tasks and 5 profiles.

Prompted instructions. Rules in the prompt: verify after acting, report the outcome. From the pilot we already know the failure mode: the model chooses its own check, and the choice is a lottery.

Communication primitives. Five functions in the policy namespace:

- say_verified(check, success_msg, failure_msg): speaks only after running the check
- say_progress(i, n, msg): grounded step narration
- confirm_before(action): asks before acting
- describe_scene(): reports what is actually present
- pause_for_verification(): stops and waits

The check lives inside the primitive. In simulation the check is ground truth. On a real robot the same slot takes a VLM verifier.

Note: the primitives result is correct by construction, because say_verified calls the same check the scorer does. The honest claim is that primitives remove the choice of check, not that they are automatically accurate. 

## 6. Discussion

Baseline CaP is unsafe for non-visual use by silence, not by lying. The false-confirmation rate is 2% of attempted failures; the silence rate is 98%. That distinction matters for the fix: this is not a hallucination problem to be suppressed, it is a missing feedback loop to be built.

The mechanism is visible in the discourse structure. Everything the model knows a priori, it says up front: the plan, a missing object, occasionally a missing capability. Nothing that requires looking at the world after acting is ever said, because nothing in the pipeline looks. say() is generated with the rest of the code, before execution, and prints whatever was written there.

Accessibility prompting does not create verification, it only adds assertion. The blind and assist profiles added a handful of trailing outcome claims with no check behind them, and half were wrong. Whatever the three-condition study shows, this baseline result already argues that user modeling without grounding moves risk toward the user it means to help.

## 7. Limitations

Simulation only, one robot, tabletop scenes. Ground-truth checks share code with the scorer (the by-construction caveat above). Most data is from one model family, with the version comparison pending. The tail event is n=7. L4 deliberately carries a narration instruction and is analyzed separately, but it is in the task set.

## 8. Future work

Analyze the three-condition grid (generated, pending). Powered re-run of the tail event. Opus 4.5 vs 4.8 under the controlled pipeline, and a re-check of the earlier "verification adoption is model-independent" claim. is_placed_noisy. VLM-based verification from camera frames so the primitives work outside simulation. Messages built from verified state rather than free text beside a check. Motion and audio feedback channels. Door and Wipe as the two task additions that add new verification types (articulated state; gradual partial progress). A study with blind participants: do verified reports change trust and monitoring behavior.

## Notes

Task registry and rationale: task_set.md. Full menu of runnable CaP / CaP-X / RoboSuite tasks: task_sources.md. Codebook and coded corpus: open_coding/. Figures and plotting: figures/plot.py. Repo usage: README.md. Poster copy: poster_copy.md.