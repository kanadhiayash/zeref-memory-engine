#!/bin/bash
# zeref-install.sh — One-Command Zeref Install
# Version: 3.0.0
# Usage: bash scripts/zeref-install.sh [--runtime claude|gemini|codex|all]

RUNTIME="${1:-claude}"
FLEET_ROOT="$(pwd)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════"
echo "  ZEREF v3.0.0 INSTALL"
echo "  Runtime: $RUNTIME"
echo "════════════════════════════════════════"

# Step 1: Verify directory structure
echo ""
echo "Step 1: Verifying fleet structure..."
REQUIRED_DIRS=("skills" "agents" "commands" "references" "wiki" "registry" "scripts" "docs")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✅${NC} $dir/"
    else
        mkdir -p "$dir"
        echo -e "  ${YELLOW}📁${NC} Created $dir/"
    fi
done

# Step 2: Copy ZEREF identity file
echo ""
echo "Step 2: Setting up harness identity files..."
if [ -f "ZEREF.md" ]; then
    echo -e "  ${GREEN}✅${NC} ZEREF.md exists"
else
    echo -e "  ${RED}❌${NC} ZEREF.md missing — copy from 06_NEW_FILES/"
fi

# Step 3: Runtime-specific setup
echo ""
echo "Step 3: Runtime-specific setup..."
if [[ "$RUNTIME" == "claude" || "$RUNTIME" == "all" ]]; then
    if command -v claude &> /dev/null; then
        echo "  Configuring Claude Code..."
        echo -e "  ${GREEN}✅${NC} Claude Code detected"
    else
        echo -e "  ${YELLOW}⚠️${NC}  Claude Code not found — install from https://claude.ai/code"
    fi
fi

if [[ "$RUNTIME" == "gemini" || "$RUNTIME" == "all" ]]; then
    GEMINI_SKILLS_DIR="$HOME/.gemini/skills"
    mkdir -p "$GEMINI_SKILLS_DIR"
    if [ -f "GEMINI.md" ]; then
        cp GEMINI.md "$GEMINI_SKILLS_DIR/ZEREF.md"
        echo -e "  ${GREEN}✅${NC} Gemini CLI: ZEREF.md installed to ~/.gemini/skills/"
    else
        echo -e "  ${YELLOW}⚠️${NC}  GEMINI.md not found — copy from 06_NEW_FILES/"
    fi
fi

if [[ "$RUNTIME" == "codex" || "$RUNTIME" == "all" ]]; then
    if [ -f "AGENTS.md" ]; then
        echo -e "  ${GREEN}✅${NC} Codex: AGENTS.md ready"
    else
        echo -e "  ${YELLOW}⚠️${NC}  AGENTS.md not found — copy from 06_NEW_FILES/"
    fi
fi

# Step 4: Run validation
echo ""
echo "Step 4: Running fleet validation..."
if [ -f "scripts/zeref-validate.py" ]; then
    python3 scripts/zeref-validate.py
else
    echo -e "  ${YELLOW}⚠️${NC}  zeref-validate.py not found — validation skipped"
fi

# Step 5: Final summary
echo ""
echo "════════════════════════════════════════"
echo "  INSTALL COMPLETE"
echo ""
echo "  Next steps:"
echo "  1. Open Claude Code and point at this directory"
echo "  2. Say: 'Read ZEREF.md and activate the Zeref fleet'"
echo "  3. Run /zeref-welcome to begin your first session"
echo "════════════════════════════════════════"
echo ""
