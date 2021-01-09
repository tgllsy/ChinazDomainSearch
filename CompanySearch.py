# coding = utf8
___author___ = 'tgllsy'

import argparse
import os
import requests
import json
import csv
import time

key = ""  # 请输入你的key


def args():
    """
    命令行参数以及说明
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--read', dest='read', help='input conpany file path')
    parse_args = parser.parse_args()

    # 参数为空 输出--help命令
    if parse_args.read is None:
        parser.print_help()
        os._exit(0)

    return parse_args.read


def domain(conpany):
    '''
    从站长之家api获取到公司数据
    :param conpany:
    :return:
    '''
    url = "http://apidata.chinaz.com/CallAPI/SponsorUnit?key=" + key + "&companyName=" + str(conpany)
    print(url)
    rqs = requests.get(url)
    test = json.loads(rqs.text)
    # StateCode= test['StateCode']
    # Reason= test['Reason']
    lists = []
    if test['Result'] != None:
        Result = test['Result']
        for domain in Result:
            siteDomain = domain['SiteDomain']
            siteName = domain['SiteName']
            siteLicense = domain['SiteLicense']
            companyType = domain['CompanyType']
            owner = domain['Owner']
            verifyTime = domain['VerifyTime']
            list = [conpany, siteDomain, siteName, siteLicense, companyType, owner, verifyTime]
            lists.append(list)
    else:
        print(conpany + " 没有查到备案信息！")
        print(test['Result'])

    print("当前网站查询到的信息如下：")
    for list in lists:
        print(list)
    return lists


def main():
    file_path = args()
    # file_path = "1.txt"
    time_new = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    outfile = str(time_new) + ".csv"
    print(outfile)
    out = open(outfile, 'w+', encoding='utf-8', newline='')
    csv_writer = csv.writer(out)
    csv_writer.writerow(['公司名称', '网站域名', '网站名称', '许可证', '公司类型', '负责人', '验证时间'])
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f.readlines():
                lists = domain(line.replace('\n', ''))
                for x in lists:
                    csv_writer.writerow(x)
        f.close()
    except Exception as e:
        print("文件读取出错")
        print(e)
    out.close()


if __name__ == '__main__':
    main()
