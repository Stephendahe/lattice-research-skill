# Installation

## Install All Lattice Skills

```bash
git clone https://github.com/Stephendahe/lattice-research-skill.git
cd lattice-research-skill
```

Copy the skill folders into the skill directory used by your agent.

## Cursor

```bash
mkdir -p ~/.cursor/skills
cp -R skills/lattice-* ~/.cursor/skills/
```

For a project-local install:

```bash
mkdir -p .cursor/skills
cp -R skills/lattice-* .cursor/skills/
```

Restart Cursor or open a new Agent chat after installation.

## Claude

```bash
mkdir -p ~/.claude/skills
cp -R skills/lattice-* ~/.claude/skills/
```

Restart Claude Code or open a new Claude session after installation. For Claude.ai or API workflows, upload or register the same skill folders according to Anthropic's custom-skill workflow.

## Other Agent Skills-Compatible Tools

Copy `skills/lattice-*` into the directory your tool uses for `SKILL.md` skills. The package follows the Agent Skills directory pattern:

```text
skill-name/
  SKILL.md
  scripts/
  references/
  assets/
```

More details:

[Agent Installation Guide](docs/agent-installation.md)

## Install A Subset

```bash
cp -R skills/lattice-research-skill <your-agent-skills-dir>/
cp -R skills/lattice-find-papers <your-agent-skills-dir>/
cp -R skills/lattice-gaps <your-agent-skills-dir>/
```

`lattice-wording` and `lattice-honesty` can be installed separately if needed.

## Zotero Notes

For DOI import and local-library evidence checks, keep Zotero Desktop running and make sure the Zotero local API / connector is available to your agent.

If Zotero is unavailable, Lattice Find Papers can still prepare Request PDF lists, but Lattice Gaps should not treat abstracts or metadata as full-text evidence.

Detailed setup instructions are here:

[Zotero Configuration for Lattice](docs/zotero-configuration.md)
