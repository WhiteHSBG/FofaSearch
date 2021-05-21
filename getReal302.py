import requests
import click
from multiprocessing.dummy import Pool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hp=False
ot=""
#输出httpcode 开关
codeSw=True
proxies={}
def curl(url):

    if ("http" not in url):
        url = "http://" + url

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
    try:
        with open(ot,'a+',encoding='utf-8') as output:

            r = requests.get(url, verify=False, timeout=10, headers=headers, allow_redirects=False,proxies=proxies)
            click.secho("[*] " + url, fg='green')
            if codeSw:
                output.write(url + "|" + str(r.status_code) + "\n")
            else:
                output.write(url+"\n")

    except Exception as e:
        click.secho("[-] " + url.strip(),fg='red')


def URLtest(input,out,fileType="url",code=False,proxy={},thread=50):
    global proxies
    proxies=proxy
    global ot
    ot=out
    global codeSw
    codeSw=code
    global hp

    if fileType=="url":

        pool = Pool(thread)
        # 此处填写输入文件名输出文件名称
        linelist = []
        with open(input, 'r', encoding='utf-8') as f:
            # with open(output,'a+',encoding='utf-8') as o:
            targetList=list(set(f.readlines()))
            for each in targetList:
                each=each.split("|")[0]
                linelist.append(each.strip())

            pool.map(curl, linelist)
    elif fileType=="xlsx":
        pool = Pool(thread)
        # 此处填写输入文件名输出文件名称
        linelist = []
        with open(input, 'r', encoding='utf-8') as f:
            # with open(output,'a+',encoding='utf-8') as o:
            for each in f.readlines():
                ip=each.split()[0]
                port=each.split()[1]
                xy=each.split()[2]
                u="http://"+ip+":"+port
                if "ssl" in xy:
                    u="https://"+ip+":"+port
                linelist.append(u)

            pool.map(curl, linelist)

if __name__ == "__main__":
    URLtest("4.txt", "output9.txt", "xlsx")


