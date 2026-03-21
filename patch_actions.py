import os

files_to_patch = []
for root, dirs, files in os.walk('.'):
    if 'actions.ts' in files:
        if 'engine/actions.ts' in os.path.join(root, 'actions.ts'):
            files_to_patch.append(os.path.join(root, 'actions.ts'))

for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()

    insert_str = """
  // Install Claude Code Router if missing
  if (!det.tools.ccr.installed) {
    await emit({ event: "progress", step: "prerequisites", percent: 90, detail: "Installing Claude Code Router..." });

    // Try npm first (most common), then bun
    const npmCcrResult = tryExec("npm install -g @musistudio/claude-code-router", 120000);
    if (npmCcrResult !== null) {
      await emit({ event: "message", content: "Claude Code Router installed via npm." });
    } else {
      // Try with bun
      const bunCcrResult = tryExec("bun install -g @musistudio/claude-code-router", 120000);
      if (bunCcrResult !== null) {
        await emit({ event: "message", content: "Claude Code Router installed via bun." });
      } else {
        await emit({
          event: "message",
          content: "Could not install Claude Code Router automatically. Please install manually: npm install -g @musistudio/claude-code-router",
        });
      }
    }
  } else {
    await emit({ event: "progress", step: "prerequisites", percent: 95, detail: `Claude Code Router found: v${det.tools.ccr.version}` });
  }
"""

    target_pattern = """  } else {
    await emit({ event: "progress", step: "prerequisites", percent: 80, detail: `Claude Code found: v${det.tools.claude.version}` });
  }"""

    if 'Install Claude Code Router if missing' not in content:
        new_content = content.replace(target_pattern, target_pattern + insert_str)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
