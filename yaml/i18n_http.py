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
REVIEW_URL = "http://csbu.ruijie.com.cn/glossary-api/api/v1/glossary/review/en"

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
    product_id: int = 6,
    is_urgent: bool = False,
    expected_translate_at: str = "",
    need_ml_translation: bool = True,
    no_translation: bool = False,
) -> dict:
    return {
        "product_id": product_id,
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
    product_id: int = 6,
    verify: bool = False,
    **payload_overrides,
) -> requests.Response:
    """Submit a glossary entry. Set verify=True to enable SSL verification."""
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}
    payload = build_payload(module_key, entry_key, zh_content, product_id=product_id, **payload_overrides)

    resp = requests.post(BASE_URL, headers=headers, json=payload, verify=verify)
    resp.encoding = "utf-8"
    return resp


def get_entry(
    token: str,
    keyword: str,
    *,
    module_key: str = "",
    product: str = "",
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "",
    sort_order: str = "",
    pipeline_status: str = "",
    created_by: str = "",
    is_urgent: str = "",
    verify: bool = False,
) -> requests.Response:
    """Query glossary review entries by keyword. Set verify=True to enable SSL verification."""
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}
    params = {
        "page": page,
        "pageSize": page_size,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "keyword": keyword,
        "product": product,
        "module_key": module_key,
        "pipeline_status": pipeline_status,
        "created_by": created_by,
        "is_urgent": is_urgent,
    }

    resp = requests.get(REVIEW_URL, headers=headers, params=params, verify=verify)
    resp.encoding = "utf-8"
    return resp


def test_post_entry():
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


def test_get_entry():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTUyNzc3NTEsImlhdCI6MTc5NTE2MjU1MSwiaWQiOjIyOH0.8DM6ozpLSz8ySzxlaElJdQIEwbefawWWPU39n91ywrs"
    keyword = "assetManager.asset.type.firewall"
    product = "安全云后端"
    module_key = "assetMgmt"

    resp = get_entry(token, keyword, product=product, module_key=module_key, page=1, page_size=20)
    print(f"Status: {resp.status_code}")
    try:
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        # 提取 en_lang.content
        items = data.get("data", {}).get("list", [])
        for item in items:
            en_content = item.get("en_lang", {}).get("content", "")
            entry_key = item.get("entry_key", "")
            zh_content = item.get("zh_content", "")
            print(f"\n--- en_lang content ---")
            print(f"entry_key: {entry_key}")
            print(f"zh_content: {zh_content}")
            print(f"en_content: {en_content}")
    except ValueError:
        print(resp.text)


if __name__ == "__main__":
    test_get_entry()