import requests
import base64
import getReal302
from dateutil import rrule
from dateutil.parser import parse
import click
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import json


def setToUrl(qbase64):
    return "https://fofa.so/api/v1/search/all?email="+username+"&key="+key+"&qbase64={"+qbase64+"}"

def b64(st):
    return str(base64.b64encode(st.encode("utf-8")),"utf-8")
def query(qu,out):
    print("base64:"+b64(qu))
    url=setToUrl(b64(qu))+"&size=10000&fields=ip,port,title,cert&page=1"
    rp=requests.get(url)
    result=rp.json()
    print("query string: "+result["query"])
    print("page: "+str(result['page']))
    # print("save size: "+str(result["size"]))
    click.secho("save size: "+str(result["size"]),fg="yellow")
    if result["size"] ==0:
        return 0
    result=result["results"]
    with open(out,'a+',encoding='utf-8') as w:

        for r in result:
            ssl="http"
            if r[3]:
                ssl="https"
            if r[2]=="":
                w.write(ssl + "://" + r[0] + ":" + r[1] + "|" + "notitle" + "\n")
            else:
                w.write(ssl+"://"+r[0]+":"+r[1]+"|"+r[2]+"\n")

def byPass(qu,ot):

    now = datetime.now()
    start_year = now - relativedelta(years=2)

    mouthList=list(rrule.rrule(rrule.MONTHLY,dtstart=parse(datetime.strftime(start_year,"%Y-%m-%d")),until=parse(datetime.strftime(now,"%Y-%m-%d"))))
    bf=str(datetime.strftime(now, "%Y-%m-%d"))
    mouthList.reverse()
    for m in mouthList:
        af=str(datetime.strftime(m,"%Y-%m-%d"))
        if bf==af:
            continue
        st="Querying after=\"{}\" before=\"{}\"".format(af,bf)
        click.secho(st.center(100, "*"), fg="cyan")
        quer="{} && after=\"{}\" && before=\"{}\"".format(qu,af,bf)
        if query(quer,ot)==0:
            return



        bf=af

@click.group()
def cli():
    """
    python3 fofa.py fofaquery --queryString title="TSCEV4.0" --outPut x.txt
    python3 fofa.py checkurl --input target.txt --output output.txt --code False

    """

    pass


@click.command(options_metavar='<options>')
@click.option("--querystring",help="FOFA query string",metavar="need")
@click.option("--output",help="Output File",metavar="need")
@click.option("--proxy",help="Proxy usag: --proxy http://127.0.0.1:8081",metavar="option")
def fofaquery(querystring,output,proxy=""):
    click.secho("FOFA Query Start".center(100, "*"),fg="green")
    now = datetime.now()
    filename = str(datetime.strftime(now, "%Y%m%d%H%M%S"))+".txt"
    byPass(querystring,filename)
    # print("FOFA Query Stop".center(100,"*"))
    click.secho("FOFA Query Stop".center(100,"*"),fg="green")
    click.secho("URL Check Start".center(100,"*"),fg="green")
    # print("URL Check Start".center(100,"*"))
    try:
        px = {'http': proxy, 'https': proxy}
    except Exception:
        print("proxy ERROR"
              "usage: --proxy http://127.0.0.1:8081")
    "Chick "
    getReal302.URLtest(filename,output,proxy=px)
    click.secho("URL Check Finish".center(100, "*"), fg="green")
    print("Query original file:"+filename)
    print("Url check file out:"+output)


@click.command(options_metavar='<options>')
@click.option("--input",help="Url input file",metavar="need")
@click.option("--output",help="Check output file",metavar="need")
@click.option("--type",help="Input file type xlsx or urllist(default)",metavar="option",default="url")
@click.option("--code",help="Output httpcode(default False) usage: --code True",metavar="option",type=bool)
@click.option("--proxy",help="Proxy usag: --proxy http://127.0.0.1:8081",metavar="option")
def checkurl(input,output,type,code,proxy=""):

    try:
        px = {'http': proxy, 'https': proxy}
    except Exception:
        print("proxy ERROR"
              "usage: --proxy http://127.0.0.1:8081")
    click.secho("URL Check Start".center(100, "*"), fg="green")
    getReal302.URLtest(input,output,type,code,proxy=px)
    click.secho("URL Check Finish".center(100, "*"), fg="green")

if __name__ == '__main__':

    p="""
    ____      ____                                __  
   / __/___  / __/___ _________  ____ ___________/ /_ 
  / /_/ __ \/ /_/ __ `/ ___/ _ \/ __ `/ ___/ ___/ __ \\
 / __/ /_/ / __/ /_/ (__  )  __/ /_/ / /  / /__/ / / /
/_/  \____/_/  \__,_/____/\___/\__,_/_/   \___/_/ /_/ 
                                                      
                                    -- Whit
    """
    with open('config.json','r',encoding='utf-8') as r:
        config=json.load(r)
        username = config["username"]
        key = config["key"]
    click.secho(p,fg="green")
    cli.add_command(fofaquery)
    cli.add_command(checkurl)
    cli()
