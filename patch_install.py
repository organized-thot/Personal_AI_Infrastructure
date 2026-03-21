import os
import glob

files_to_patch = []
for root, dirs, files in os.walk('.'):
    if 'install.sh' in files:
        if '.claude/install.sh' in os.path.join(root, 'install.sh'):
            files_to_patch.append(os.path.join(root, 'install.sh'))

for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to insert the ccr check after claude check
    insert_str = """
# ─── Check Claude Code Router ────────────────────────────
if command -v ccr &>/dev/null; then
  success "Claude Code Router found"
else
  warn "Claude Code Router not found — will install during setup"
fi
"""

    if 'Check Claude Code Router' not in content:
        target_str = """# ─── Check Claude Code ───────────────────────────────────
if command -v claude &>/dev/null; then
  success "Claude Code found"
else
  warn "Claude Code not found — will install during setup"
fi
"""
        new_content = content.replace(target_str, target_str + insert_str)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
