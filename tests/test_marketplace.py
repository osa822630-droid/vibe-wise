"""Check the marketplace catalog against the rules claude.ai applies when adding it.

claude.ai clones the repository, reads .claude-plugin/marketplace.json, and
validates each plugin entry before it syncs. Its validator is stricter than
`claude plugin validate`: a plugin source of "." is rejected even though the CLI
accepts it, an entry under the default strict mode needs a .claude-plugin/plugin.json
whose name matches the entry, and a SKILL.md frontmatter field outside the Agent
Skills specification can invalidate the skill. These tests keep the catalog in the
shape claude.ai accepts, so adding the marketplace doesn't fail with a generic
"check the repository URL" message.
"""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"

# Fields the Agent Skills specification defines for SKILL.md frontmatter.
SPEC_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path):
    """Read top-level frontmatter keys from a Markdown file without a YAML parser."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields, text
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return None, text


class MarketplaceCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load(MARKETPLACE)

    def plugin_root(self, entry):
        source = entry["source"]
        self.assertIsInstance(source, str, "claude.ai accepts relative path sources here")
        # claude.ai rejects "." while the CLI accepts it; require "./".
        self.assertTrue(source.startswith("./"), f"{source!r} must start with ./")
        self.assertNotIn("..", Path(source).parts)
        root = (ROOT / source).resolve()
        self.assertTrue(root.is_dir(), f"{source} does not exist")
        self.assertTrue(
            root.is_relative_to(ROOT.resolve()), f"{source} escapes the marketplace root"
        )
        return root

    def test_required_top_level_fields(self):
        self.assertTrue(NAME_PATTERN.match(self.catalog["name"]))
        self.assertTrue(self.catalog["owner"]["name"])
        self.assertTrue(self.catalog["description"])
        self.assertTrue(self.catalog["version"])
        self.assertTrue(self.catalog["plugins"])

    def test_entries_point_at_plugins_with_matching_manifests(self):
        for entry in self.catalog["plugins"]:
            with self.subTest(plugin=entry["name"]):
                self.assertTrue(NAME_PATTERN.match(entry["name"]))
                self.assertTrue(entry["description"])
                root = self.plugin_root(entry)
                manifest = load(root / ".claude-plugin/plugin.json")
                # Under strict mode (the default) claude.ai requires a manifest and
                # installs the plugin under the entry's name.
                self.assertEqual(manifest["name"], entry["name"])
                self.assertEqual(manifest["version"], self.catalog["version"])
                self.assertTrue(manifest["description"])
                self.assertTrue(manifest["license"] or (root / "LICENSE").is_file())

    def test_no_top_level_bin_directory(self):
        # claude.ai and Cowork refuse to install a plugin that ships a bin/ folder.
        for entry in self.catalog["plugins"]:
            self.assertFalse((self.plugin_root(entry) / "bin").exists())

    def test_skills_follow_the_agent_skills_specification(self):
        for entry in self.catalog["plugins"]:
            root = self.plugin_root(entry)
            skill_files = sorted(root.glob("skills/*/SKILL.md"))
            self.assertTrue(skill_files, "the plugin should expose at least one skill")
            for path in skill_files:
                with self.subTest(skill=str(path.relative_to(ROOT))):
                    fields, _ = frontmatter(path)
                    self.assertIsNotNone(fields, "SKILL.md needs YAML frontmatter")
                    unknown = set(fields) - SPEC_FIELDS
                    self.assertFalse(
                        unknown,
                        f"{path.parent.name} uses {sorted(unknown)}, which claude.ai "
                        "can reject when syncing; move extras into metadata:",
                    )
                    self.assertEqual(fields["name"], path.parent.name)
                    self.assertTrue(NAME_PATTERN.match(fields["name"]))
                    self.assertTrue(fields["description"])
                    self.assertLessEqual(len(fields["description"]), 1024)
                    self.assertNotIn(
                        "disable-model-invocation",
                        fields,
                        "chat has no way to invoke a skill that the model can't call",
                    )

    def test_hook_commands_resolve(self):
        for entry in self.catalog["plugins"]:
            root = self.plugin_root(entry)
            config = load(root / "hooks/hooks.json")
            for groups in config["hooks"].values():
                for group in groups:
                    for hook in group["hooks"]:
                        command = hook["command"]
                        match = re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"']+)", command)
                        self.assertIsNotNone(match, command)
                        self.assertTrue((root / match.group(1)).is_file(), command)


class CodexCatalogTests(unittest.TestCase):
    def test_plugin_source_exists(self):
        catalog = load(CODEX_MARKETPLACE)
        self.assertTrue(catalog["plugins"])
        for entry in catalog["plugins"]:
            source = entry["source"]
            self.assertEqual(source["source"], "local")
            root = (ROOT / source["path"]).resolve()
            self.assertTrue(root.is_dir(), source["path"])
            manifest = load(root / ".codex-plugin/plugin.json")
            self.assertEqual(manifest["name"], entry["name"])


class WebSupportTests(unittest.TestCase):
    def test_learn_skill_documents_the_web_surface(self):
        skill = ROOT / "plugins/vibe-wise/skills/learn"
        guide = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Claude on the web", guide)
        self.assertTrue((skill / "web.md").is_file())
        web = (skill / "web.md").read_text(encoding="utf-8")
        self.assertIn("vibe-wise-state.md", web)

    def test_reset_skill_documents_the_web_surface(self):
        guide = (ROOT / "plugins/vibe-wise/skills/reset/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Claude on the web", guide)


if __name__ == "__main__":
    unittest.main()
