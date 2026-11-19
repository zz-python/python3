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


def main(properties_path: str, prefix: str):
    result = extract_key_values(properties_path, prefix)
    print(f"Extracted {len(result)} entries with prefix '{prefix}':\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    props_path = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages.properties"
    main(props_path, "assetManager")