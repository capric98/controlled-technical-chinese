#!/usr/bin/env bash
# Package the runtime artifact for installation and validate it.
#
# The Agent Skills specification requires the skill's directory name to match the
# skill's `name`. This repository is a development repository named ctc-skill, so
# the installable layout is produced here rather than imposed on the repo root.
# The released artifact is still exactly the root SKILL.md, byte for byte.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(sed -n 's/^name:[[:space:]]*//p' "$ROOT/SKILL.md" | head -1)"
DIST="$ROOT/dist/$NAME"

rm -rf "$ROOT/dist"
mkdir -p "$DIST"
cp "$ROOT/SKILL.md" "$DIST/SKILL.md"

echo "packaged $NAME -> dist/$NAME/SKILL.md"
python3 "$ROOT/tools/check_skill.py" "$DIST/SKILL.md"
npx --yes skills-ref validate "$DIST"
