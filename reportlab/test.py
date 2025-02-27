data = [{'logType': 0, 'attackType': 19, 'attackTypeString': '攻击类型2', 'max': 23}, {'logType': 0, 'attackType': 5, 'attackTypeString': '攻击类型1', 'max': 10}]
categoryNames = [entry['attackTypeString'] for entry in data]
print(categoryNames)