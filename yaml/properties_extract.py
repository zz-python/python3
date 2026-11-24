#!/usr/bin/env python3
"""
Properties file key-value extractor — reads a Java .properties file
and returns all entries whose key starts with the given prefix.

Usage:
    python properties_extract.py <properties_file_path> <prefix>

Example:
    python properties_extract.py "E:/projects/.../messages.properties" assetManager

Outputs a JSON map of key -> value.
"""

import re
import sys
import json


def _unescape_java_unicode(s: str) -> str:
    """Decode Java-style \\uXXXX escapes in a string to real Unicode characters."""
    def _replace(m: re.Match) -> str:
        return chr(int(m.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', _replace, s)


def extract_key_values(file_path: str, prefix: str) -> dict[str, str]:
    """
    Parse a .properties file and return a flat key->value map
    for all entries whose key starts with the given prefix.
    """
    result: dict[str, str] = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()

            # skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('!'):
                continue

            # split on first '=' or ':'
            sep_pos = -1
            for i, ch in enumerate(line):
                if ch in ('=', ':'):
                    sep_pos = i
                    break

            if sep_pos == -1:
                continue

            key = line[:sep_pos].strip()
            value = line[sep_pos + 1:].strip()

            if key.startswith(prefix):
                result[key] = _unescape_java_unicode(value)

    return result


def check_key_values(file_path: str, prefix: str, input_map: dict[str, str]) -> dict:
    pass


def write_key_values(file_path: str, updates: dict[str, str], prefix: str):
    """
    Update values in a .properties file by walking lines — only lines
    whose key starts with *prefix* and in *updates* are touched.
    """
    if not updates:
        print("No changes to write.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines: list[str] = []
    updated = 0

    for line in lines:
        raw = line.rstrip('\n\r')
        stripped = raw.strip()

        # blank / comment / no separator — keep as-is
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            new_lines.append(line)
            continue

        sep_pos = -1
        for i, ch in enumerate(stripped):
            if ch in ('=', ':'):
                sep_pos = i
                break

        if sep_pos == -1:
            new_lines.append(line)
            continue

        key = stripped[:sep_pos].rstrip()
        sep_char = stripped[sep_pos]
        old_value = stripped[sep_pos + 1:].lstrip()

        if key in updates and key.startswith(prefix):
            new_value = updates[key]
            # preserve leading whitespace
            leading = line[:len(line) - len(line.lstrip())]
            new_lines.append(f'{leading}{key}{sep_char} {new_value}\n')
            print(f"[UPD ] {key}: {old_value!r} -> {new_value!r}")
            updated += 1
        else:
            new_lines.append(line)

    if updated == 0:
        print("No changes to write.")
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Wrote {updated} update(s) to {file_path}")
    


def test_extract_key_values(properties_path: str, prefix: str):
    result = extract_key_values(properties_path, prefix)
    print(f"Extracted {len(result)} entries with prefix '{prefix}':\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    test_extract_key_values()