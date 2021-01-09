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
    parser.add_argument('-r', '--read', dest='read', help='input whois file path')
    parse_args = parser.parse_args()

    # 参数为空 输出--help命令
    if parse_args.read is None:
        parser.print_help()
        os._exit(0)

    return parse_args.read


def domain(host):
    """
     从站长之家api获取到公司数据
     """
    url = "http://apidata.chinaz.com/CallAPI/Whois?key=" + key + "&domainName=" + host
    print(url)
    rqs = requests.get(url)
    test = json.loads(rqs.text)
    # StateCode = test['StateCode']
    # Reason = test['Reason']
    # # print(StateCode)
    # # print(Reason)

    lists = []
    if test['Result'] != None:
        Result = test['Result']
        Host = Result['Host']
        ContactPerson = Result['ContactPerson']
        Registrar = Result['Registrar']
        Email = Result['Email']
        Phone = str(Result['Phone'])
        CreationDate = str(Result['CreationDate'])
        ExpirationDate = str(Result['ExpirationDate'])
        WhoisServer = str(Result['WhoisServer'])
        DnsServer = str(Result['DnsServer'])
        DomainStatus = str(Result['DomainStatus'])
        lists = [host, Host, ContactPerson, Registrar, Email, Phone, CreationDate, ExpirationDate, WhoisServer,
                 DnsServer, DomainStatus]
    else:
        print(host + " 没有查到备案信息！")

    print("当前网站查询到的信息如下：")
    print(lists)
    return lists


def main():
    file_path = args()
    time_new = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    outfile = str(time_new) + ".csv"
    out = open(outfile, 'w+', encoding='utf-8', newline='')
    csv_writer = csv.writer(out)
    csv_writer.writerow(['域名', '网站域名', ' 联系人', '注册商', '联系邮箱', ' 联系电话', '创建时间', '过期时间', '域名服务器', 'DNS', '状态'])
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f.readlines():
                lists = domain(line.replace('\n', ''))
                print(lists)
                csv_writer.writerow(lists)
        f.close()
    except Exception as e:
        print("文件读取出错")
        print(e)
    out.close()


if __name__ == '__main__':
    main()
