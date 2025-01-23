*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    OperatingSystem

*** Variables ***
# API的基础URL
${BASE_URL}    https://172.27.55.53
# 认证信息
${AUTH_TOKEN}  Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMzAyMjkxMzMxMjUwNDI5OTUzIiwicm9sZSI6InRlbmFudEFkbWluIiwiaXNGaXJzdExvZ2luIjpmYWxzZSwidXNlcl9uYW1lIjoiTVNQIiwidGltZXpvbmUiOm51bGwsImlzcyI6IjEiLCJ1c2VySWQiOiIyNTA0Mjk5NTM5IiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9BRE1JTiJdLCJjbGllbnRfaWQiOiJ3ZWJfYXBwIiwidGVuYW50TmFtZSI6Ium7mOiupOenn-aItyIsInNjb3BlIjpbIm9wZW5pZCJdLCJuYW1lIjoiTVNQIiwibmlja25hbWUiOiJNU1AiLCJleHAiOjE3MzgyMDAyMTQsImlhdCI6MTczNzU5NTQxNCwianRpIjoiZzRzWGtzNzc0ZTFrbTRkTlpVcXo3OXF4M2l3IiwiZ3VpZGUiOmZhbHNlfQ.TOr_ZPKruktNyk9yBGIV4Ku9SNbOib6OoiC8FoSjuLS4CM7FAbEH744-q2SSRIqi-25iUw3qH1Q4FCe6SyEnadVp1lW3sqVjmASm_5RmDP1dBlDf0cydMeHplaY3sSkH1hkj6KH3FR-MC1jbi-2q0wKnRBU4xsuOr0XGA8bXUR-LptSyuX6KRpEjY9NNo4Jze5dEIv0gZ0LxOeWeetAC8SWt2PnrKz7Rep7CeFFBeHAbtdct4UMPylkBUlAByYKWYyjQOeOnshk9RmI_KNaFTCTO5DCJgvs5HSz6mXKCt0-PpuHewwliDE9wzqGTCu-zAISR5qHiTFZSNjsyEfFkxA

*** Test Cases ***
Test GET API
    [Documentation]    验证GET接口是否返回正确的状态码和数据

    # 0. 定义头部信息查询参数
    ${headers}    Create Dictionary    Authorization=${AUTH_TOKEN}
    ${query_params}    Create Dictionary    page=0    size=10    ipType=0    allowType=0    deviceKey=device-abc

    # 1. 创建会话和headers
    Create Session    my_test_session    ${BASE_URL}    headers=${headers}

    # 2. 发送GET请求到指定的路径和参数
    ${response}    GET On Session    my_test_session    /api/ne-base-cfg/black-white/black-whites    params=${query_params}

    # 3. 验证状态码
    Should Be Equal As Integers    ${response.status_code}    200

    # 4. 验证返回的数据
    ${response_body}    To Dictionary    ${response.json()}
    Log    返回的数据：${response_body}

*** Keywords ***
# 简单返回值
To Dictionary
    [Arguments]    ${response}
    RETURN    ${response}
