#!/usr/bin/env bash
# Package the runtime artifact for installation and validate it.
#
# The repository directory and the skill's `name` match. This script still
# produces an isolated installable layout whose runtime artifact is exactly the
# root SKILL.md, byte for byte.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(sed -n 's/^name:[[:space:]]*//p' "$ROOT/SKILL.md" | head -1)"
DIST="$ROOT/dist/$NAME"

rm -rf "$ROOT/dist"
mkdir -p "$DIST"
cp "$ROOT/SKILL.md" "$DIST/SKILL.md"

echo "packaged $NAME -> dist/$NAME/SKILL.md"
python3 "$ROOT/tools/check_skill.py" "$DIST/SKILL.md"
pnpm dlx skills-ref validate "$DIST"
