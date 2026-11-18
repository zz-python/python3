#!/usr/bin/env python3
"""
HTTP client for the i18n glossary API.

Usage as module:
    from i18n_http import post_entry
    resp = post_entry(token="<token>", module_key="socAlert", entry_key="allAlerts", zh_content="全部告警")

Usage as script:
    python i18n_http.py <token> <module_key> <entry_key> <zh_content>
"""

import json
import sys

import requests


BASE_URL = "http://csbu.ruijie.com.cn/glossary-api/api/v1/glossary/entries"
PRODUCT_ID = 6

HEADERS_TEMPLATE = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://csbu.ruijie.com.cn",
    "Referer": "http://csbu.ruijie.com.cn/glossary/review-cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
}


def build_payload(
    module_key: str,
    entry_key: str,
    zh_content: str,
    *,
    is_urgent: bool = False,
    expected_translate_at: str = "",
    need_ml_translation: bool = True,
    no_translation: bool = False,
) -> dict:
    return {
        "product_id": PRODUCT_ID,
        "module_key": module_key,
        "zh_content": zh_content,
        "is_urgent": is_urgent,
        "expected_translate_at": expected_translate_at,
        "need_ml_translation": need_ml_translation,
        "no_translation": no_translation,
        "entry_key": entry_key,
    }


def post_entry(
    token: str,
    module_key: str,
    entry_key: str,
    zh_content: str,
    *,
    verify: bool = False,
    **payload_overrides,
) -> requests.Response:
    """Submit a glossary entry. Set verify=True to enable SSL verification."""
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}
    payload = build_payload(module_key, entry_key, zh_content, **payload_overrides)

    resp = requests.post(BASE_URL, headers=headers, json=payload, verify=verify)
    resp.encoding = "utf-8"
    return resp


def main():
    token = "xxxx"
    module_key = "secAlert"
    entry_key = "secAlert.test"
    zh_content = "测试"

    resp = post_entry(token, module_key, entry_key, zh_content)
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print(resp.text)


if __name__ == "__main__":
    main()