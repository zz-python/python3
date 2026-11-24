#!/usr/bin/env python3
"""
YAML key-value extractor for localization files.

Usage:
    python yaml_extract.py <yaml_file_path> <top_level_key>

Example:
    python yaml_extract.py "C:/project/ui_remote_module/locales/zh-CN.yaml" socAlert

Outputs a JSON map of key -> value for all entries under the specified top-level key.
Keys are flattened with dot notation (e.g., socAlert.allAlerts -> 全部告警).
"""

import sys
import json

import yaml


def extract_key_values(file_path: str, prefix: str) -> dict[str, str]:
    """
    Parse a YAML file and return a flat key->value map for all entries
    under the given top-level key prefix.

    Nested keys are joined with dots. Only leaf (string) values are included.
    Keys that lead to nested dicts are skipped — only their leaves appear.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if prefix not in data:
        print(f"Warning: key '{prefix}' not found in YAML file", file=sys.stderr)
        return {}

    subtree = data[prefix]

    result: dict[str, str] = {}

    def _flatten(node, parent_key: str):
        if isinstance(node, dict):
            for k, v in node.items():
                full_key = f"{parent_key}.{k}"
                if isinstance(v, str):
                    result[full_key] = v
                elif isinstance(v, dict):
                    _flatten(v, full_key)
                # skip non-string leaf values (lists, numbers, etc.)
        # skip non-dict top-level

    _flatten(subtree, prefix)
    return result


def write_key_values(file_path: str, updates: dict[str, str], prefix: str):
    """
    Update values in a YAML file by walking lines — only lines under
    the given *prefix* subtree are touched; every other line is kept as-is.

    :param file_path:  path to the YAML file
    :param updates:     dict of {full_dotted_key: new_value}
    :param prefix:      top-level key, e.g. "socAlert"
    """
    if not updates:
        print("No changes to write.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    path_stack: list[tuple[int, str]] = []  # [(indent, key_name), ...]
    new_lines: list[str] = []
    updated = 0

    for line in lines:
        stripped = line.rstrip('\n\r')
        content = stripped.lstrip(' ')

        # blank line
        if not content:
            new_lines.append(line)
            continue

        indent = len(line) - len(line.lstrip(' '))

        # pop siblings / ancestors when indent decreases or stays the same
        while path_stack and indent <= path_stack[-1][0]:
            path_stack.pop()

        # comment / non-key line
        if content.startswith('#') or ':' not in content:
            new_lines.append(line)
            continue

        # split on first colon only (values may contain ':')
        colon_idx = content.index(':')
        key_part = content[:colon_idx].rstrip()
        value_part = content[colon_idx + 1:].strip()

        # build full dotted key from stack + current key
        full_key = '.'.join([p[1] for p in path_stack] + [key_part])

        if value_part:
            # leaf node — check if this key should be updated
            if full_key in updates and full_key.startswith(prefix):
                new_value = updates[full_key]
                # preserve quoting style of the original value
                if value_part.startswith('"') and value_part.endswith('"'):
                    new_val_str = f'"{new_value}"'
                elif value_part.startswith("'") and value_part.endswith("'"):
                    new_val_str = f"'{new_value}'"
                else:
                    new_val_str = new_value

                new_line = ' ' * indent + f'{key_part}: {new_val_str}\n'
                new_lines.append(new_line)
                path_stack.append((indent, key_part))
                print(f"[UPD ] {full_key}: {value_part!r} -> {new_value!r}")
                updated += 1
            else:
                new_lines.append(line)
                path_stack.append((indent, key_part))
        else:
            # nested key (no value) — push to stack, keep line as-is
            new_lines.append(line)
            path_stack.append((indent, key_part))

    if updated == 0:
        print("No changes to write.")
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Wrote {updated} update(s) to {file_path}")


def main(yaml_path: str, top_key: str):
    result = extract_key_values(yaml_path, top_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main("C:/project/ui_remote_module/locales/zh-CN.yaml", "socAlert")