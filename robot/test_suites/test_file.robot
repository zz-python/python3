*** Settings ***
Library    OperatingSystem

*** Test Cases ***
Example Test
    [Documentation]    验证文件是否存在
    File Should Exist    myfile.txt
