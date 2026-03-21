import os
import glob

files_to_patch = []
for root, dirs, files in os.walk('.'):
    if 'types.ts' in files:
        if 'engine/types.ts' in os.path.join(root, 'types.ts'):
            files_to_patch.append(os.path.join(root, 'types.ts'))

for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()

    insert_str = "    ccr: { installed: boolean; version?: string; path?: string };\n"
    target_str = "    claude: { installed: boolean; version?: string; path?: string };\n"

    if 'ccr: {' not in content:
        new_content = content.replace(target_str, target_str + insert_str)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
