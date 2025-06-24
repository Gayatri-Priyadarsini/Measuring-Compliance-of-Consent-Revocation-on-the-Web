import json
import numpy as np
import difflib
from nltk.metrics.distance import *
import pandas as pd
import csv 
websites={}
websites2={}
def parse_json_file(url,file_path):
    with open(file_path,encoding='utf-8', errors='ignore') as json_file:
        data = json.load(json_file, strict=False)
        cookies = data.get('cookiesCB', [])
        list_cookies = data.get('cookies', [])
        nec=[]
        fun=[]
        adv=[]
        ana=[]
        udef=[]
        ad=0
        n=0
        f=0
        an=0
        un=0
        dad=str(cookies)
        for k in cookies:
            if k['level']=="INFO": 
                #print(dad) 
                c=k['message'].split()
                c=c[3][:len(c[3])-1]
                #print(k['message'])
                start_idx=dad.find('"IDB:"')
                end_idx=len(dad)-53
                #print(start_idx,end_idx)
                data=dad[start_idx+8:end_idx-4]
                #print(data)
                #p=JSON.parse(data)
                #dad=data.split()
                #data = data.replace("\\","")
                #data = data.replace('""',"")
                dad = data.replace("\\","")
                dad = dad.replace(':"",',':" ",')
                dad = dad.replace('""','"')
                print()
                #cb=None
                #print(c)
                #try:
                #c_json=json.loads(c[3])
                #cb=json.loads(c_json)
                #print(len(cb))
                #print(data)
                cb=json.loads(dad)
                for b in cb:
                    #print(b)
                    if b['current_label']==0:
                        n=n+1
                        nec.append(b['name'])
                    elif b['current_label']==1:
                        f=f+1
                        fun.append(b['name'])
                    elif b['current_label']==2:
                        an=an+1
                        ana.append(b['name'])
                    elif b['current_label']==3:
                        ad=ad+1
                        adv.append(b['name'])
                    else:
                        un=un+1
                        udef.appedn(b['name'])

        #print("---------------",list_cookies)
        nec1=[]
        fun1=[]
        adv1=[]
        ana1=[]
        udef1=[]
        ad1=0
        n1=0
        f1=0
        an1=0
        un1=0
        for c in list_cookies:            
            value=c['value']
            name=c['name']
            do=c['domain']

            if name in nec:
                n1=n1+1
                nec1.append([name,do])
            
            elif name in fun:
                f1=f1+1
                fun1.append([name,do])
            
            elif name in ana:
                an1=an1+1
                ana1.append([name,do])

            elif name in adv:
                ad1=ad1+1
                adv1.append([name,do])
            else:
                un1=un1+1
                udef1.append([name,do])
    cookie_block=n+f+an+ad+un
    selenium_c=len(list_cookies)
    print(cookie_block,selenium_c)
    websites[url]=[[n,nec],[f,fun],[an,ana],[ad,adv],[un,udef]]
    websites2[url]=[[n1,nec1],[f1,fun1],[an1,ana1],[ad1,adv1],[un1,udef1]]
    writer.writerow([df2['Rank'][id],df2['Websites'][id],n1,nec1,f1,fun1,an1,ana1,ad1,adv1,un1,udef1,cookie_block,selenium_c])
    #writer.writerow([df2['Rank'][id],df2['Websites'][id],n,nec,f,fun,an,ana,ad,adv,un,udef,cookie_block,selenium_c])
df2 = pd.read_csv('../List_of_websites/top_200.csv')

print(df2.keys())


fieldnames=['Rank','Website','Count-N','N','Count-F','F','Count-Ana','Ana','Count-Ad','Ad','Undefined','Un']  
with open('jj.csv',mode='w',newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    id=-1
    for url in df2['Websites']:
        print(url)
        id=id+1
        file_path = f"dataset_1/{url}/browsing_data3.json"
        try:
            cookies=parse_json_file(url,file_path)
        except Exception as e:
            print(url,e)
            websites[url]=[[],[],[],[],[]]
            writer.writerow([df2['Rank'][id],df2['Websites'][id],'',[],'',[],'',[],'',[],'',[],'',''])

    #writer.writerow([df2['Rank'][id],df2['Website'][id],n,nec,f,fun,an,ana,ad,adv])

#print(websites)
#print(websites2)
