#!/usr/bin/env python3
"""
Entry point — extract key-value pairs from a YAML localization file
and submit each entry to the i18n glossary API.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from properties_extract import extract_key_values, check_key_values
from i18n_http import post_entry, get_entry

# 文件路径
PROP_PATH = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages.properties"
PROP_PATH_EN = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages_en.properties"
# key值头
PROP_TOP_KEY = "assetManager"

# 平台模块名称
MODULE_KEY = "assetMgmt"
# 平台token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTUyNzc3NTEsImlhdCI6MTc5NTE2MjU1MSwiaWQiOjIyOH0.8DM6ozpLSz8ySzxlaElJdQIEwbefawWWPU39n91ywrs"
# 产品
PRODUCT = "安全云后端"
PRODUCT_ID = 7


def write_entry():
    result = extract_key_values(PROP_PATH, PROP_TOP_KEY)
    print(f"Extracted {len(result)} entries from {PROP_PATH}[{PROP_TOP_KEY}]")
    print(f"Posting to glossary with module_key={MODULE_KEY} ...\n")

    success = 0
    fail = 0

    for entry_key, zh_content in result.items():
        try:
            resp = post_entry(TOKEN, MODULE_KEY, entry_key, zh_content, product_id=PRODUCT_ID)
        except Exception as exc:
            print(f"[FAIL] {entry_key} -> {zh_content}  |  {exc}")
            fail += 1
            continue

        if resp.status_code in (200, 201):
            print(f"[ OK ] {resp.status_code} | {entry_key} | {zh_content} | {resp.text[:500]}")
            success += 1
        else:
            print(f"[{resp.status_code}] {entry_key} | {zh_content} | {resp.text[:500]}")
            fail += 1

    print(f"\nDone.  success={success}  fail={fail}")

def check_entry():
    result = extract_key_values(PROP_PATH, PROP_TOP_KEY)
    print(f"Extracted {len(result)} entries from {PROP_PATH}[{PROP_TOP_KEY}]")
    print(f"Module key: {MODULE_KEY}\n")

    en_map: dict[str, str] = {}
    found = 0
    missing = 0

    for entry_key, zh_content in result.items():
        try:
            resp = get_entry(TOKEN, entry_key, module_key=MODULE_KEY, product=PRODUCT)
        except Exception as exc:
            print(f"[ERR] {entry_key} -> {exc}")
            missing += 1
            continue

        print(f"[{resp.status_code}] {entry_key} | {resp.text[:300]}")
        if resp.status_code != 200:
            print(f"[{resp.status_code}] {entry_key}")
            missing += 1
            continue

        data = resp.json()
        if not data:
            print(f"[EMPTY] {entry_key}")
            missing += 1
            continue

        items = data.get("data", {}).get("list", [])
        if items:
            en_content = items[0].get("en_lang", {}).get("content", "")
            en_map[entry_key] = en_content
            print(f"{entry_key} = {zh_content}  |  en: {en_content}")
            found += 1
        else:
            print(f"[NO RESULT] {entry_key}")
            missing += 1

    print(f"\nTotal: found={found}  missing={missing}")

    # 核对企业微信翻译 en_map 与 English properties 文件
    check_result = check_key_values(PROP_PATH_EN, PROP_TOP_KEY, en_map)
    print(f"\n--- check_key_values against {PROP_PATH_EN} ---")
    print(f"matched:   {len(check_result['matched'])}")
    print(f"mismatched: {len(check_result['mismatched'])}")
    print(f"extra:      {len(check_result['extra'])}")
    print(f"missing:    {len(check_result['missing'])}")

    if check_result["mismatched"]:
        print("\n=== mismatched ===")
        for key, diff in check_result["mismatched"].items():
            print(f"  {key}")
            print(f"    expected: {diff['expected']}")
            print(f"    got:      {diff['got']}")
    if check_result["extra"]:
        print("\n=== extra (in en_map but not in file) ===")
        for key, val in check_result["extra"].items():
            print(f"  {key} = {val}")
    if check_result["missing"]:
        print("\n=== missing (in file but not in en_map) ===")
        for key, val in check_result["missing"].items():
            print(f"  {key} = {val}")

    return en_map

if __name__ == "__main__":
    check_entry()