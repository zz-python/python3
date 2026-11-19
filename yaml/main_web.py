#!/usr/bin/env python3
"""
Entry point — extract key-value pairs from a YAML localization file
and submit each entry to the i18n glossary API.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yaml_extract import extract_key_values
from i18n_http import post_entry

# 文件路径
YAML_PATH = "C:/project/ui_remote_module/locales/zh-CN.yaml"
# key值头
YAML_TOP_KEY = "socAlert"

# 平台模块名称
MODULE_KEY = "secAlert"
# 平台token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTUxNjk1MDksImlhdCI6MTc5NTA1NDMwOSwiaWQiOjIyOH0.UllfInK9DnWKhz7wHJEK_yXxuUDTtt1hcJWlvM-zQT4"
# 产品ID
PRODUCT_ID = 6


def main():
    result = extract_key_values(YAML_PATH, YAML_TOP_KEY)
    print(f"Extracted {len(result)} entries from {YAML_PATH}[{YAML_TOP_KEY}]")
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
            print(f"[ OK ] {resp.status_code} | {entry_key} | {zh_content} | {resp.text[:200]}")
            success += 1
        else:
            print(f"[{resp.status_code}] {entry_key} | {zh_content} | {resp.text[:200]}")
            fail += 1

    print(f"\nDone.  success={success}  fail={fail}")


if __name__ == "__main__":
    main()