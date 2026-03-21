import os

files_to_patch = []
for root, dirs, files in os.walk('.'):
    if 'detect.ts' in files:
        if 'engine/detect.ts' in os.path.join(root, 'detect.ts'):
            files_to_patch.append(os.path.join(root, 'detect.ts'))

for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()

    insert_str = '      ccr: detectTool("ccr", "ccr --version"),\n'
    target_str = '      claude: detectTool("claude", "claude --version 2>&1"),\n'

    if 'ccr:' not in content:
        new_content = content.replace(target_str, target_str + insert_str)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
