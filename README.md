<img src="plugins/vibe-wise/.claude-plugin/icon.svg" alt="VibeWise brain with code brackets" width="96" height="96">

# VibeWise

**You build. AI writes.**

A plugin for **Claude Code**, **Claude on the web** (claude.ai chat and Cowork), and **Codex** that puts learning first and keeps you in control while AI writes the code you designed. The AI **asks for your approach first**, helps you examine tradeoffs, and explains unfamiliar concepts. You shape the design and decide when it's ready to implement. The AI writes the code, then explains what it changed and why.

For anyone who wants to learn as they build—whether you're an aspiring engineer, a junior developer, or an experienced engineer exploring an unfamiliar stack. Practice planning how the pieces fit together, anticipating failures, and checking the result while keeping ownership of the decisions.

## Table of Contents

- [Get started](#get-started)
  - [Claude on the web](#claude-on-the-web)
  - [Claude Code](#claude-code)
  - [Codex](#codex)
- [This fork](#this-fork)
- [Troubleshooting the web marketplace](#troubleshooting-the-web-marketplace)
- [What it feels like](#what-it-feels-like)
- [Make it yours](#make-it-yours)
- [Updating](#updating)
- [License](#license)

## Get started

The plugin is the same on every surface. Pick where you use it; the install steps
differ because only Claude Code and Codex can run terminal commands.

You need an up-to-date [Claude](https://claude.ai), [Claude
Code](https://code.claude.com/docs/en/setup), or
[Codex](https://developers.openai.com/codex). Claude Code and Codex also need
[Python 3](https://www.python.org/downloads/); Claude on the web needs nothing
installed. In Claude Code, VibeWise uses Python to restore learning context and
reset learning notes. In Codex, only reset needs it. No extra Python packages are
needed.

### Claude on the web

Works in claude.ai chat, the Claude desktop app, and Cowork. No terminal, no
download, and no Python.

1. Open [Customize → Plugins](https://claude.ai/customize/plugins).
2. Select **Add**, then **Add marketplace**, then **Add from a repository**.
3. Enter `osa822630-droid/vibe-wise` (the full
   `https://github.com/osa822630-droid/vibe-wise` URL works too) and select **Sync**.
4. Open the **Personal** tab, select **VibeWise**, and add it to your account.
5. Start a chat and ask for **VibeWise** or **learn mode**; typing `/` also lists
   the plugin's skills.

Setup asks one question at a time. Answer in plain text, because the choice picker
from Claude Code isn't available in chat. Then ask for what you want to build.

On the web the plugin has no file access, so your notes travel inside the
conversation instead of a `.vibe-wise/` folder. After setup, and again after each
confirmed design, VibeWise prints a compact `vibe-wise-state.md` block. Keep it in
your Claude Project's knowledge to resume in another chat; a new chat without it
starts fresh.

What loads on the web: the Learn and Reset skills and the learning behavior. What
doesn't: session hooks, automatic restoration, and running your repository's code or
tests. Claude writes the agreed code in the chat or an artifact, as you approved it,
and says which checks it couldn't run.

If the marketplace won't add, see
[Troubleshooting the web marketplace](#troubleshooting-the-web-marketplace).

### Claude Code

This repository is its own marketplace. Run these commands **one at a time** in
Claude Code. First, add the marketplace:

```text
/plugin marketplace add osa822630-droid/vibe-wise
```

After it finishes, install the plugin:

```text
/plugin install vibe-wise@vibe-wise
```

Enable automatic updates through `/plugin` → **Marketplaces** → **vibe-wise** →
**Enable auto-update**. This is off by default for third-party marketplaces.
Restart Claude Code in the project you want to work on, then run:

```text
/vibe-wise:learn
```

Setup asks one question at a time. Use the arrow keys and Enter for choices; pick
**Use defaults** to skip preference setup. Then ask Claude to build something.
Starting fresh or joining an unfamiliar repository both work. For an existing
repository, Claude first inspects the code and sketches a small system map.

<details>
<summary>Alternative: install the upstream plugin from Anthropic's Directory</summary>

The original project is also published in the built-in **Anthropic Directory**. If
you don't need this fork's changes, run:

```text
/plugin install vibe-wise@anthropic-plugin-directory
```

Choose an installation scope and confirm. No marketplace setup is needed. Choose
one installation method; you don't need both.

</details>

### Codex

In a terminal, run these commands **one at a time**. First, add the marketplace:

```sh
codex plugin marketplace add osa822630-droid/vibe-wise
```

After it finishes, install the plugin:

```sh
codex plugin add vibe-wise@vibe-wise
```

Start Codex in your project and run `$vibe-wise:learn`. Run it again at the start
of each Codex session, and whenever Codex seems to have lost track of learning
mode. It resumes from your saved notes without repeating setup. To reset, run
`$vibe-wise:reset`. Claude Code and Codex share the same `.vibe-wise/` notes.

In Codex, the commands in this guide use `$` instead of `/`: `/vibe-wise:learn`
becomes `$vibe-wise:learn`.

## This fork

This is [nykooi1/vibe-wise](https://github.com/nykooi1/vibe-wise) laid out so the
same repository can be added as a marketplace in Claude Code, Codex, and claude.ai.
The catalog sits at the repository root and the plugin lives in `plugins/vibe-wise/`.
Claude Code and Codex keep their `.vibe-wise/` notes and session hook; Claude on the
web gets a file-free mode that keeps the same notes in the conversation. The only
behavior change for existing users is that the Learn and Reset skills are now
model-invocable, because claude.ai rejects Claude Code-only `SKILL.md` frontmatter.

## Troubleshooting the web marketplace

The claude.ai dialog says only "Failed to add marketplace" or "Marketplace sync
failed. Check the repository URL and try again." even when the real cause is
something else. Check these in order.

- **A marketplace named `vibe-wise` already exists.** claude.ai names a marketplace
  after the repository, not after the catalog's `name` field, and it enforces that
  name before it reads the repository. If you ever added `nykooi1/vibe-wise` (or
  tried this fork before), remove the old one first: **Customize → Plugins →
  Marketplaces**, select `vibe-wise`, remove it, then add this repository again and
  reinstall the plugin. Renaming your fork also gives the marketplace a new name.
- **The repository is private or the default branch isn't `main`.** Make it public,
  or connect GitHub when the dialog asks and grant the Claude GitHub App access.
  claude.ai reads the repository's default branch.
- **The repository predates this fork's layout.** Here the catalog is
  `.claude-plugin/marketplace.json` and the plugin itself is `plugins/vibe-wise/`,
  with `"source": "./plugins/vibe-wise"`. Older copies put the plugin at the
  repository root (`"source": "./"`), the same folder as the catalog; claude.ai
  validates that shape more strictly and can fail the sync. Sync your fork with
  `main` and add the marketplace again.
- **Plugins aren't available on your account or organization.** If **Plugins**
  never appears under **Customize**, your plan or organization doesn't offer plugin
  marketplaces here. Use [Claude Code](#claude-code) instead.
- **The marketplace adds but the skill doesn't answer.** Open a new chat after
  installing, then ask "which skills do you have from plugins?" and mention
  VibeWise or learn mode explicitly.

## What it feels like

You're building a Notion-style notes app: users sign in, create and edit private
notes, and organize them into folders. Here, you're working through how notes and
folders relate—and what should happen when someone deletes a folder.

This condensed example is adapted from a real learning session. Later implementation
steps are illustrative; intervening design discussions are omitted.

**You:**

```text
A note can be in several folders. Deleting a folder should delete its notes.
```

**Claude / Codex:**

```text
✦ Build checkpoint: Deleting a shared note

"Trip ideas" is in both Travel and Summer. Deleting it removes it from both.

When someone deletes Travel, what should happen to that note in Summer?
```

**You:**

```text
Keep it in Summer. If it has no folders left, keep the note outside any folder.
```

**Claude / Codex:**

```text
That separates deleting a folder from deleting a note.

✦ Build checkpoint: Connecting notes and folders

How would you represent which folders a note belongs to, without copying the note?
```

**You:**

```text
A links table with note_id and folder_id. Deleting a folder removes its links,
not the notes.
```

**Claude / Codex:**

```text
Each link records one membership. Several links can point to the same note;
a note with no links is unfiled.

notes ← folder links → folders

✦ Design checkpoint: Folder membership

Proposed: store notes once and track folder membership in a links table.
Deleting a folder removes its links and keeps the notes. This supports multiple
folders per note; loading a folder's notes needs a lookup through those links.

Confirming records this design. We still need to work through access rules
and technology choices before writing code.

❯ 1. Confirm and continue
     This approach makes sense to me; move to the next piece.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Confirm and continue.
```

*Later, after the remaining choices for this step are worked through...*

**Claude / Codex:**

```text
✦ Implementation checkpoint: Folder membership

I'll add the agreed tables and folder-deletion operation, then test that deleting
a folder preserves its notes and their membership in other folders.
This step builds storage behavior; the UI comes later.

❯ 1. Implement this step
     This approach makes sense to me; write the code for this step.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Implement this step.
```

*Claude or Codex writes the code and runs the tests.*

**Claude / Codex:**

```text
✦ Implementation report: Folder membership

- Added the schema migration: each membership references one note and one folder.
- Added folder deletion: removes the folder and its links, preserving note content.
- Added and ran tests for shared notes and notes left without a folder; both passed.
```

You don't need to know the answer already. The AI can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

Describing what you want sets the requirements. Build Checkpoints ask you to work
out how it should function; a feature preference doesn't approve an architecture.

| Checkpoint | What happens |
| --- | --- |
| **Build** | You reason through how to approach the problem with the AI. |
| **Design** | Review the design. **Confirm and continue** records it and continues planning; no code yet. |
| **Implementation** | Review the specific code changes. **Implement this step** authorizes the AI to make them. |

These aren't three mandatory stops. When ready to code, the Implementation
checkpoint also confirms the design, skipping a separate Design checkpoint.
Both confirmations offer **Discuss** to ask questions, clarify anything confusing,
or explore alternatives before deciding.

When the AI proposes additional implementation details, it separates them from your
decisions in a short list or table explaining each addition and why it matters.
You can question or change any item before proceeding.

After implementation, the AI briefly explains what changed, how the key code works,
why it fits your decision, any tests it added or updated and what they cover, and
which checks ran with their results. Ask to dig deeper anywhere it's unclear.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

## Make it yours

Experience changes the support you get, not your ownership of decisions:

| Level | Teaching approach |
| --- | --- |
| Beginner | Explain unfamiliar pieces, use diagrams, ask smaller reasoning questions. |
| Intermediate | Less introductory context; explore interactions and tradeoffs. |
| Advanced | Probe difficult constraints, failure modes, and design assumptions. |

Everyone reasons first. The AI adapts to what you demonstrate and how familiar you
are with the stack. Checkpoint frequency—Light, Normal, or Frequent—is separate.

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this one.”
- “Pause learning.” Resume with `/vibe-wise:learn`.

Preferences, learning notes, and a project map live in `.vibe-wise/` in your project. In a Git repository, that's the repository root, and VibeWise finds it from any subfolder. Without Git, it's the folder you start in, so always start from your project's top folder. Learning mode resumes in future sessions and after compaction. Add `.vibe-wise/` to your `.gitignore` to keep your notes out of Git; the plugin won't change it silently.

No extra account, backend, or telemetry. Saved notes are included in the AI's context, so your normal Claude, Claude Code, or Codex data settings still apply. On Claude on the web there is no project folder: the same notes stay in the conversation as a `vibe-wise-state.md` block that you choose where to keep.

To start learning this project from scratch, run `/vibe-wise:reset` (on the web,
ask VibeWise to reset learning). It shows the project and asks **Cancel / Reset
learning**. After confirmation, it backs up your
profile, progress, and project map inside the notes directory's `backups/` folder,
then restarts onboarding. Source code and other projects stay untouched. To change
your experience level or preferences, just tell the AI; no reset is needed.

## Updating

On Claude on the web, open **Customize → Plugins**, select **Marketplaces**, and
choose **Check for updates** on `vibe-wise`. If the update doesn't reach a
conversation, start a new chat. Plans and organization settings can delay or block
updates.

In Claude Code, open `/plugin` → **Installed**, select VibeWise, and choose **Update now**.
For automatic updates, open **Marketplaces**, select the source you installed from,
and enable auto-update if it's off.

To update from your terminal:

```sh
claude plugin marketplace update vibe-wise
```

```sh
claude plugin update vibe-wise@vibe-wise
```

If you installed the upstream plugin from Anthropic's Directory instead:

```sh
claude plugin update vibe-wise@anthropic-plugin-directory
```

Then restart Claude Code. Your project learning notes stay intact; no reset is needed.
Run `claude plugin list` to check the installed version.
[More about plugin updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

For Codex, refresh the marketplace, then install the latest version:

```sh
codex plugin marketplace upgrade vibe-wise
```

```sh
codex plugin add vibe-wise@vibe-wise
```

Then start a new Codex session.

## License

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
