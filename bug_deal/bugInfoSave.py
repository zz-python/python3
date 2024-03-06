from urllib import parse
import requests
import csv
import json
import datetime
import os
import shutil

BUG_SAVE_URL = 'http://bugs.ruijie.com.cn/bug_switch/bug/bug_add_save'
BUG_RESOLVED_URL = 'http://bugs.ruijie.com.cn/bug_switch/bug/bug_info_save'


def cbd(config, wbsId, line, row):
    params = config.get("cbd", {})
    bugId = row['BUGID']
    if not bugId:
        print('ERROR: 第{}行BUGID未定义'.format(line))
        return

    wbsName = '【{}】'.format(config.get('wbs').get(str(wbsId)))
    summary = row.get('BUG简介')
    if not summary:
        print('ERROR: {}行"BUG简介"为空'.format(line))
        return
    else: 
        summary = wbsName + summary

    repairInfluence = row.get('修订影响面')
    testVerification = row.get('测试验证点')
    locationResult = row.get('根因定位结论')

    if not repairInfluence:
        repairInfluence = "NA"
    if not testVerification:
        testVerification = "NA"
    if not locationResult:
        locationResult = "NA"

    params['id'] = bugId
    params['wbs'] = wbsId
    params['summary'] = summary
    params['repairInfluence'] = repairInfluence
    params['testVerification'] = testVerification
    params['locationResult'] = locationResult

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "bugs.ruijie.com.cn",
        "Origin": "http://bugs.ruijie.com.cn",
        "Referer": "http://bugs.ruijie.com.cn/bug_switch/bug/bug_add",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
	} 
    cookies = {
        "JSESSIONID": config.get("JSESSIONID", ""),
        "bug-cookie": config.get("bug-cookie", "")
    }
    data = parse.urlencode(params)
    res = requests.post(url=BUG_RESOLVED_URL, data=data, headers=headers, cookies=cookies, timeout=30)
    if res.status_code != 200:
        print('ERROR: 第{}行提交出错了!'.format(line))
        return False
    print('INFO: 第{}行请求响应：{}'.format(line, res.text))
    result = json.loads(res.text)
    if 'success' == result.get('type'):
        print('SUCCESS: 第{}行提交出成功，result：{}'.format(line, result))

def resolved(config, wbsId, line, row):
    params = config.get("resolved", {})
    bugId = row['BUGID']
    if not bugId:
        print('ERROR: 第{}行BUGID未定义'.format(line))
        return

    wbsName = '【{}】'.format(config.get('wbs').get(str(wbsId)))
    summary = row.get('BUG简介')
    if not summary:
        print('ERROR: {}行"BUG简介"为空'.format(line))
        return
    else: 
        summary = wbsName + summary

    resolvedAnalyse = row.get('分析过程')
    resolvedSolution = row.get('解决方案')
    resolvedVerification = row.get('验证解决方案')
    resolvedModuleAffect = row.get('对其他模块影响')
    resolvedProductAffect = row.get('对其他产品影响')
    repairInfluence = row.get('修订影响面')
    testVerification = row.get('测试验证点')
    locationResult = row.get('根因定位结论')

    if not resolvedAnalyse:
        resolvedAnalyse = "NA"
    if not resolvedSolution:
        resolvedSolution = "NA"
    if not resolvedVerification:
        resolvedVerification = "NA"
    if not resolvedModuleAffect:
        resolvedModuleAffect = "NA"
    if not resolvedProductAffect:
        resolvedProductAffect = "NA"
    if not repairInfluence:
        repairInfluence = "NA"
    if not testVerification:
        testVerification = "NA"
    if not locationResult:
        locationResult = "NA"

    params['id'] = bugId
    params['wbs'] = wbsId
    params['summary'] = summary
    params['resolvedAnalyse'] = resolvedAnalyse
    params['resolvedSolution'] = resolvedSolution
    params['resolvedVerification'] = resolvedVerification
    params['resolvedModuleAffect'] = resolvedModuleAffect
    params['resolvedProductAffect'] = resolvedProductAffect
    params['repairInfluence'] = repairInfluence
    params['testVerification'] = testVerification
    params['locationResult'] = locationResult

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "bugs.ruijie.com.cn",
        "Origin": "http://bugs.ruijie.com.cn",
        "Referer": "http://bugs.ruijie.com.cn/bug_switch/bug/bug_add",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
	} 
    cookies = {
        "JSESSIONID": config.get("JSESSIONID", ""),
        "bug-cookie": config.get("bug-cookie", "")
    }
    data = parse.urlencode(params)
    res = requests.post(url=BUG_RESOLVED_URL, data=data, headers=headers, cookies=cookies, timeout=30)
    if res.status_code != 200:
        print('ERROR: 第{}行提交出错了!'.format(line))
        return False
    print('INFO: 第{}行请求响应：{}'.format(line, res.text))
    result = json.loads(res.text)
    if 'success' == result.get('type'):
        print('SUCCESS: 第{}行提交出成功，result：{}'.format(line, result))


def add_save(config, wbsId, line, row):
    params = config.get("baseInfo", {})
    if row['BUGID']:
        print('ERROR: 第{}行BUG已存在'.format(line))
        return

    wbsName = '【{}】'.format(config.get('wbs').get(str(wbsId)))
    summary = row.get('BUG简介')
    description = row.get('BUG描述')
    testtopo = row.get('测试拓扑')
    topodesc = row.get('拓扑描述')

    if not summary:
        print('ERROR: {}行"BUG简介"为空'.format(line))
        return
    else: 
        summary = wbsName + summary

    params['wbs'] = wbsId
    params['summary'] = summary
    if not description:
        params['description'] = summary
    else:
        params['description'] = description
    if testtopo:
        params['testtopo'] = testtopo
    if topodesc:
        params['topodesc'] = topodesc

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "bugs.ruijie.com.cn",
        "Origin": "http://bugs.ruijie.com.cn",
        "Referer": "http://bugs.ruijie.com.cn/bug_switch/bug/bug_add",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
	} 
    cookies = {
        "JSESSIONID": config.get("JSESSIONID", ""),
        "bug-cookie": config.get("bug-cookie", "")
    }
    data = parse.urlencode(params)
    res = requests.post(url=BUG_SAVE_URL, data=data, headers=headers, cookies=cookies, timeout=30)
    if res.status_code != 200:
        print('ERROR: 第{}行提交出错了!'.format(line))
        return False
    print('INFO: 第{}行请求响应：{}'.format(line, res.text))
    result = json.loads(res.text)
    if 'success' == result.get('type') and 'id' in result:
        print('SUCCESS: 第{}行提交出成功，result：{}'.format(line, result))
        row['BUGID'] = result.get('id')

def get_config():
    config = {}
    with open('config.json', 'r', encoding='utf-8') as file:  
        config = json.load(file)  
    return config

def add_save_by_csv(wbsId, **setting):
    print('------ 提交新BUG. {} 工作包 ------ '.format(wbsId))
    config = get_config()
    start = setting.get('start', None)
    end = setting.get('end', None)
    if str(wbsId) not in config.get('wbs', {}):
        print('------ {} 工作包不存在，忽略 ------ '.format(wbsId))
    reader = None
    data = []
    fileName = '{}.csv'.format(wbsId)
    with open(fileName, 'r', encoding='utf-8-sig') as file:  
        reader = csv.DictReader(file) 
        reader.line_num
        for index, row in enumerate(reader):
            line = index + 2
            data.append(row)
            if start and line < start:
                continue
            elif end and line > end:
                continue
            add_save(config, wbsId, line, row)
    backup(fileName)
    update_file(fileName, reader, data)

def resolved_save_by_csv(wbsId, **setting):
    print('------ 解决BUG. {} 工作包 ------ '.format(wbsId))
    config = get_config()
    start = setting.get('start', None)
    end = setting.get('end', None)
    if str(wbsId) not in config.get('wbs', {}):
        print('------ {} 工作包不存在，忽略 ------ '.format(wbsId))
    reader = None
    data = []
    fileName = '{}.csv'.format(wbsId)
    with open(fileName, 'r', encoding='utf-8-sig') as file:  
        reader = csv.DictReader(file) 
        reader.line_num
        for index, row in enumerate(reader):
            line = index + 2
            data.append(row)
            if start and line < start:
                continue
            elif end and line > end:
                continue
            resolved(config, wbsId, line, row)

def cbd_by_csv(wbsId, **setting):
    print('------ CBD. {} 工作包 ------ '.format(wbsId))
    config = get_config()
    start = setting.get('start', None)
    end = setting.get('end', None)
    if str(wbsId) not in config.get('wbs', {}):
        print('------ {} 工作包不存在，忽略 ------ '.format(wbsId))
    reader = None
    data = []
    fileName = '{}.csv'.format(wbsId)
    with open(fileName, 'r', encoding='utf-8-sig') as file:  
        reader = csv.DictReader(file) 
        reader.line_num
        for index, row in enumerate(reader):
            line = index + 2
            data.append(row)
            if start and line < start:
                continue
            elif end and line > end:
                continue
            cbd(config, wbsId, line, row)

def backup(fileName):
    now = datetime.datetime.now()  
    timeStr = now.strftime("%Y%m%d%H%M%S") 
    targetFile = '{}.{}'.format(fileName, timeStr) 
    shutil.copy2(fileName, targetFile)
    print('备份文件：{} -> {}'.format(fileName, targetFile))


def update_file(fileName, reader, data):
    if not reader:
        return
    with open(fileName, 'w', newline='', encoding='utf-8-sig') as file:  
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)  
        writer.writeheader() 
        writer.writerows(data)

if __name__ == '__main__':
    # "71223": "酒店投屏-web",
    # "71073": "替换信息-web"
    # wbs: 72136
    # add_save_by_csv(71073, start=29)
    resolved_save_by_csv(72136)
    # cbd_by_csv(71073, start=22)
    # cbd_by_csv(72136)