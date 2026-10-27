---
name: learn
description: Start or resume VibeWise learning-first development, where the person designs and Claude writes the agreed code. Use when someone explicitly asks for VibeWise, learn mode, or learning-first development, in Claude Code, Codex, or Claude on the web.
compatibility: Claude Code and Codex keep notes in .vibe-wise/ in the project; Claude on the web keeps the same notes in the conversation.
---

# VibeWise Learn mode

Activate learning mode in the main conversation. Read [behavior.md](behavior.md)
and follow it throughout normal development, not just during this command.
The learner owns the design. Ask for their approach and wait. Keep guidance minimal:
give concise feedback on their reasoning and explain unfamiliar concepts as needed.
Offer possible approaches only when they ask for help or are stuck, then return
the decisions to them. Learning and learner control take priority over build speed.
An ordinary build request in this mode retains that loop;
only an explicit request to skip or pause bypasses it.
Do not switch to a subagent or require manual coding by default.

## Pick the surface first

- **Claude on the web (claude.ai chat):** no shell, no file tools, no session
  hook. Read [Claude on the web](#claude-on-the-web) below, and [web.md](web.md)
  when you can open it. Skip the Claude Code steps that follow.
- **Codex:** read [codex.md](codex.md) first, then use the Claude Code steps.
- **Claude Code:** use the steps below as written.

Use the Read tool for plugin guides instead of printing them with Bash `cat`.
Use Glob to discover optional learner-state files before reading them. A missing
`.vibe-wise/` directory is normal first-time setup, not an error. If a shell
check is necessary, handle absence with an explicit conditional that succeeds;
don't run `ls` on a possibly missing directory or hide actual read failures.
Keep guide reads separate from optional state checks so a missing file doesn't
make a successful instruction read look like a failed tool call.

## Locate state

Starting at the current working directory, look upward for `.vibe-wise/` or legacy
`.sensible-vibes/`, preferring `.vibe-wise/` when both exist at the same level,
stopping at the nearest `.git` directory or file (including a worktree root).
Use the nearest existing state directory within that boundary. Without Git, check
only the current directory; don't search its parents. Keep using legacy
notes in place; never merge, move, or reset them automatically. If there is none,
create `.vibe-wise/` at the Git root, or current directory without Git. Do not use
state from a parent repository, another worktree, or the installed plugin folder.
Do not follow symlinked state directories or files; explain the issue instead.

If `profile.md` exists, read it and `project-map.md`. Search the entire `progress.md`
for pending decisions, then read their complete sections and other topics relevant
to the task. An initial excerpt is not evidence that nothing is pending.
Resume without repeating completed onboarding or bypassing a pending Design or
Implementation checkpoint.
Set `Learning mode: active` if the user is resuming paused learning. If onboarding
is incomplete, ask only the unanswered questions. Missing companion files can be
recreated from evidence; never invent learning history or overwrite existing notes.

If no profile exists, read [onboarding.md](onboarding.md) and run onboarding.
Use [state-templates.md](state-templates.md) when creating state. These files are
local Markdown maintained with normal file tools; there is no service to call.

After setup, continue the user's build task. If none was provided, ask what they
want to build or change. Invoking this skill again should not reset anything.

## Claude on the web

In claude.ai chat there is no shell, no file tools, and no session hook, so
`.vibe-wise/` cannot be read or written. Keep the learning behavior in
behavior.md unchanged and change only where notes and questions live.

- **Questions:** AskUserQuestion doesn't exist here. Ask one plain-text question
  at a time, list 2–4 short options with brief descriptions, end your turn, and
  wait. Reasoning questions stay open-ended.
- **State:** treat a `vibe-wise-state.md` file in this conversation (project
  knowledge, an uploaded file, or text the learner pasted) as the profile,
  progress, and map. Reuse what it records and never invent history it doesn't.
- **No state yet:** run onboarding from onboarding.md, then keep the state in the
  conversation.
- **Saving state:** after setup, and after each confirmed or implemented design,
  print a compact fenced block labeled `vibe-wise-state.md` holding the profile,
  the current project map, learned concepts, and any pending decision. Keep it
  short enough to paste into a new chat or a project's knowledge.
- **Code:** you can't edit a repository or run tests here. Explain what you would
  change, or write the code in the conversation or an artifact, and say plainly
  which checks you couldn't run.
- **Reset:** there are no saved notes, so backing up and deleting files doesn't
  apply. Confirm with the learner, then discard the state block and start
  onboarding again.
- **Limits:** hooks, agents, and automatic restoration are ignored on the web.
  A new chat starts fresh unless the state block or project knowledge is present.

[web.md](web.md) has the full adaptation. Read it when you can open files.
