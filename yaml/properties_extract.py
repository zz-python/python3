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
    """
    Compare the given input_map against the .properties file.
    Returns a dict with:
        matched   — key 和 value 完全一致
        mismatched — key 存在但 value 不同
        extra     — 	input_map 中有但文件中没有的 key
        missing   — 文件中有但 input_map 中缺少的 key
    """
    file_map = extract_key_values(file_path, prefix)

    matched: dict[str, str] = {}
    mismatched: dict[str, dict] = {}
    extra: dict[str, str] = {}
    missing: dict[str, str] = {}

    # check input_map against file
    for key, val in input_map.items():
        if key in file_map:
            if val == file_map[key]:
                matched[key] = val
            else:
                mismatched[key] = {"expected": file_map[key], "got": val}
        else:
            extra[key] = val

    # check file keys not in input_map
    for key, val in file_map.items():
        if key not in input_map:
            missing[key] = val

    return {
        "matched": matched,
        "mismatched": mismatched,
        "extra": extra,
        "missing": missing,
    }


def test_extract_key_values(properties_path: str, prefix: str):
    result = extract_key_values(properties_path, prefix)
    print(f"Extracted {len(result)} entries with prefix '{prefix}':\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def test_check_key_values():
    props_path = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages.properties"
    prefix = "assetManager"

    # 构造一个测试 map：故意有匹配、不匹配、多余、缺少
    test_map = {
        "assetManager.module": "资产管理",          # matched
        "assetManager.asset.type.PC": "错误的值",                     # mismatched
        "assetManager.not.exist.key": "不存在的key",                              # extra
        # "assetManager.assetGroup.defaultName" 故意不传，验证 missing
    }

    result = check_key_values(props_path, prefix, test_map)

    print("=== matched ===")
    print(json.dumps(result["matched"], ensure_ascii=False, indent=2))
    print("\n=== mismatched ===")
    print(json.dumps(result["mismatched"], ensure_ascii=False, indent=2))
    print("\n=== extra ===")
    print(json.dumps(result["extra"], ensure_ascii=False, indent=2))
    print(f"\n=== missing ({len(result['missing'])} keys) ===")
    print(json.dumps(result["missing"], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    # test_check_key_values()
    test_check_key_values()