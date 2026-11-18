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


def main(yaml_path: str, top_key: str):
    result = extract_key_values(yaml_path, top_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main("C:/project/ui_remote_module/locales/zh-CN.yaml", "socAlert")