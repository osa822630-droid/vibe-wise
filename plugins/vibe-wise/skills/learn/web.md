# VibeWise in Claude on the web

Claude on the web (claude.ai chat) loads this plugin's skills but has no shell,
no file tools, and no session hook. Hooks and agents are ignored there. Keep the
learning behavior in [behavior.md](behavior.md) unchanged and adapt only state,
questions, and code delivery. When you can't open this file, follow the shorter
summary under "Claude on the web" in [SKILL.md](SKILL.md).

## Questions

AskUserQuestion isn't available. Ask one question at a time as a normal paragraph,
with 2–4 short numbered options and a one-line description for each, then end your
turn and wait. Keep reasoning questions open-ended; don't turn them into a picker.
Onboarding follows [onboarding.md](onboarding.md), one plain-text question per reply.

## State lives in one document

The three files in [state-templates.md](state-templates.md) become sections of a
single Markdown document named `vibe-wise-state.md`:

```markdown
# VibeWise state

## Profile
Learning mode: active
Onboarding: complete
Situation / Building / Codebase familiarity / Learning scope:
Experience and stack familiarity:
Goals and preferences (frequency, question style, implementation style):

## Progress
## Topic
- Introduced / Demonstrated understanding / Needs reinforcement

## Project map
Purpose, requirements, components, main flow, data and trust boundaries,
build and deployment, unknowns. Label proposed, chosen, and implemented pieces.

## Pending decision
The proposed approach, its stage (awaiting reasoning, choice confirmation, or
implementation approval), and the reply you are waiting for.
```

Treat any `vibe-wise-state.md` present in the conversation as the saved state: in
project knowledge, an uploaded attachment, or text the learner pasted. Reuse what
it records, ask only for what's missing, and never invent history. Don't read state
from another chat, another project, or your own notes.

## Saving state

Print the updated `vibe-wise-state.md` in a fenced block after setup finishes,
after a design is confirmed, after an implementation report, and whenever you are
waiting on a pending decision. Keep it compact (aim for under 40 lines), retype it
fully each time so it can replace the old copy, and don't include secrets,
transcripts, or full file contents. Never claim it was saved to a file or project;
the learner copies it. Suggest keeping it in the current Claude Project's knowledge
so every chat in that project can resume, and note that a new chat without it
starts fresh.

## Working without a repository

You can't edit files, run tests, or inspect a repository here. Ask the learner to
attach or paste the files that matter, and treat what you receive as evidence;
mark anything unverified as unknown. Deliver agreed code in the conversation or an
artifact, in the order the learner approved, and say which checks you could not run.
Skip Claude Code instructions about tools, hooks, and `.gitignore`, and don't imply
that notes or code were written to disk.

## Reset

There are no files to back up, so a reset discards the state document and restarts
onboarding. Ask once in plain text, wait for an explicit answer, then begin fresh
from [onboarding.md](onboarding.md). Say that nothing on disk was deleted.

## Presentation

Keep the checkpoint and callout formatting from behavior.md: divider, bold
`✦ <Type>: <description>` heading, blank lines around normal prose, no cards or
code fences for ordinary replies. One question per reply, at the end, with its
options beneath it.
