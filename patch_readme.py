import os

files_to_patch = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f in ['README.md', 'INSTALL.md']:
            files_to_patch.append(os.path.join(root, f))

for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to insert mention of claude-code-router where claude-code is mentioned

    # Find places that list prerequisites
    if 'Bun, Git, Claude Code' in content:
        new_content = content.replace('Bun, Git, Claude Code', 'Bun, Git, Claude Code, Claude Code Router')
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
    elif 'npm install -g @anthropic-ai/claude-code' in content:
        if '@musistudio/claude-code-router' not in content:
            new_content = content.replace('npm install -g @anthropic-ai/claude-code\n', 'npm install -g @anthropic-ai/claude-code\n   npm install -g @musistudio/claude-code-router\n')
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Patched {filepath}")
