#!/usr/bin/env python3
"""
Entry point — extract key-value pairs from a YAML localization file
and submit each entry to the i18n glossary API.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from properties_extract import extract_key_values, write_key_values
from i18n_http import post_entry, get_entry

# 文件路径
PROP_PATH = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages.properties"
PROP_PATH_EN = "E:/projects/security-operations/platform/soc-common/soc-common-i18n/src/main/resources/messages_en.properties"
# key值头
PROP_TOP_KEY = "assetManager"

# 平台模块名称
MODULE_KEY = "assetMgmt"
# 平台token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTU2MDI1MzcsImlhdCI6MTc5NTQ4NzMzNywiaWQiOjIyOH0.N-Xp9iuKRNntxZjnabRsNUhcwpzRGrysdgjU8zSAdyA"
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

def check_entry_en():
    result = extract_key_values(PROP_PATH_EN, PROP_TOP_KEY)
    print(f"Extracted {len(result)} entries from {PROP_PATH_EN}[{PROP_TOP_KEY}]")
    print(f"Module key: {MODULE_KEY}\n")

    diff_updates: dict[str, str] = {}

    for entry_key, content in result.items():
        try:
            resp = get_entry(TOKEN, entry_key, module_key=MODULE_KEY, product=PRODUCT)
            # 比对entry_key 的 content和resp返回的是否一致
            data = resp.json()
            items = data.get("data", {}).get("list", [])
            # 从返回列表中精确匹配 entry_key
            matched = [it for it in items if it.get("entry_key") == entry_key]
            if not matched:
                print(f"[MISS] {entry_key} | content: {content} | (not found in API response)")
                continue
            api_content = matched[0].get("en_lang", {}).get("content", "")
            if content == api_content:
                print(f"[MATCH] {entry_key} | {content}")
            else:
                print(f"[DIFF] {entry_key} | PROP: {content} | API: {api_content}")
                diff_updates[entry_key] = api_content
        except Exception as exc:
            print(f"[ERR] {entry_key} -> {exc}")
            continue

    if diff_updates:
        print(f"\nUpdating {len(diff_updates)} key(s) with API values...")
        write_key_values(PROP_PATH_EN, diff_updates, PROP_TOP_KEY)
    else:
        print("\nAll entries match — nothing to update.")


if __name__ == "__main__":
    # write_entry()
    check_entry_en()