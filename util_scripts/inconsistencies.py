import urllib
import json
from urllib.parse import urlparse
import pandas as pd
import csv
from iab_tcf import decode_v2
import ast
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
import sys, os

def parse_html(html_source):
    # Parse HTML
    soup = BeautifulSoup(html_source, 'html.parser')

    # Find src attributes from iframe tags
    iframe_src_list = [iframe['src'] for iframe in soup.find_all('iframe')]
    #print("SRC attributes from iframe tags:", iframe_src_list)

    # Find src attributes from img tags
    img_src_list = [img['src'] for img in soup.find_all('img')]
    #print("SRC attributes from img tags:", img_src_list)

    return iframe_src_list,img_src_list


def get_cmp_name(cid):
    with open("cmp-list.json", 'r') as json_file:
        data = json.load(json_file)
        cmps_list = data.get("cmps",{})
        cid=str(cid)
        #print(cid)
        #print(cmps_list[cid])
        try:
            #print(cmps_list[cid]['name'])
            return cmps_list[cid]['name']
        except Exception as e:
            return None
        
def parse_url(url):
    #print("PPPPAAARRRSSEEEE",url)
    l=[]
    url = urllib.parse.unquote(url)
    parse_result=urlparse(url)
    if parse_result.query!="":

        #print("query:",parse_result.query)
        query=parse_result.query
        query=query.split("&")
        for params in query:
            try:
                pair=params.split("=")
                k=pair[0]
                v=pair[1]
                #print(v)
                CMP_name=None
                if v[0]=="C" and v[-1]=="A":
                    consent=decode_v2(v)
                    CMP_ID=consent.cmp_id
                    CMP_name=get_cmp_name(CMP_ID)
                    CMP_purposes=[consent.purposes_consent,consent.purposes_legitimate_interests,consent.special_features_optin]
                    if CMP_name==None:
                        continue
                    else:
                        #print(k,CMP_name)
                        #l.append([parse_result.hostname,k,CMP_ID,CMP_name,CMP_purposes])
                        l.append([parse_result.hostname,k,v])
            except:
                pass
    #print(l)
    return l


    # print("fragment",parse_result.fragment)

def parse_stack(stack,urls):
    if stack:
        # Get the callFrames from the current stack
        call_frames = stack.get('callFrames', [])
        
        # Iterate through each call frame
        for frame in call_frames:
            # Get the url from the current call frame
            url = frame.get('url')
            if url:
                urls.append(url)
            
            # Recursively call collect_urls on the parent stack
            parent_stack = stack.get('parent')
            parse_stack(parent_stack, urls)



def parse_json_file(file_path):
    entry_obj={}
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for each_entry in data:
            try:
                #print(each_entry['params']['requestId'])

                if each_entry['params']['requestId'] in entry_obj.keys():
                    entry_obj[each_entry['params']['requestId']].append(each_entry)
                else:
                    entry_obj[each_entry['params']['requestId']]=[each_entry]

            except:
                pass

    return entry_obj

def parse_loop(data):
    result = []
    #print(type(data))
    #print("AAAHHHHH",data)
    for key, value in data.items():
        try:
            value=json.loads(value)
        except:
            pass
        if isinstance(value, dict):
            # If the value is a dictionary, recursively parse it
            result.extend(parse_loop(value))
        elif isinstance(value, list):
            # If the value is a list, iterate through it
            for item in value:
                if isinstance(item, dict):
                    # If the item in the list is a dictionary, recursively parse it
                    result.extend(parse_loop(item))
                elif isinstance(item, str):
                    #print(item)
                    #print("strinnggggg",type(value),value)
                    # If the item is a string, add it to the result
                    try:
                        cmp_id=decode_v2(value).cmp_id
                        cmp_name=get_cmp_name(cmp_id)
                        if cmp_name!=None:
                            if value[0]=="C"and value[-1]=="A":
                                #print(value)
                                #print(key)
                                #l.append([key,value])
                                result.append([key,item])
                    except:
                        pass
                else:
                    # Handle other types of items as needed
                    pass
        elif isinstance(value, str):
            # If the value is a string, add it to the result
            #result.append(value)
            #print("strinnggggg",type(value),value)
            try:
                cmp_id=decode_v2(value).cmp_id
                cmp_name=get_cmp_name(cmp_id)
                if cmp_name!=None:
                    if value[0]=="C"and value[-1]=="A":
                        #print(value)
                        #print(key)
                        result.append([key,value])
            except:
                pass
        else:
            # Handle other types of values as needed
            pass
    #print(result)
    return result


def parse_postdata(postdata):
    l=[]
    postdata=json.loads(postdata)
    l=parse_loop(postdata)
    #print(l)
    return l

def extract_html_from_string(mixed_string):
    #print(mixed_string)
    l=[]
    soup = BeautifulSoup(mixed_string, 'html.parser')
    
    # Extract the script tags separately
    script_tags = soup.find_all('script')
    scripts_content = []
    for script in script_tags:
        script_content = str(script)
        script_string=script_content.replace("\\\"", "\"").replace("\\\\", "\\")
        #print(script_string)
        #print()
        url_pattern = re.compile(r'src=["\'](.*?)["\']')

        # Extract URLs from script tags
        urls = []
        for script in script_tags:
            if script.get('src'):
                urls.append(script['src'])
            else:
                # If script tag does not have src attribute, try extracting URLs from its content
                script_content = script.string
                if script_content:
                    extracted_urls = re.findall(url_pattern, script_content)
                    urls.extend(extracted_urls)

        # Print the extracted URLs
        #print("Extracted URLs:", len(urls))
        for url in urls:
            #print(url)
            #print("*************************************************************",url)
            url_tcstring=parse_url(url)
            if url_tcstring !=[]:
                l.append(url_tcstring)

    
    # Use regex to extract all remaining HTML parts
    html_pattern = re.compile(r'(<[^>]+>[^<]*<\/[^>]+>|<[^>]+>)')
    
    html_parts = html_pattern.findall(str(soup))

    # Join the HTML parts to form a complete HTML string
    html_content = ''.join(html_parts)
    
    # Append the script contents back to the final HTML content
    full_content = html_content + ''.join(scripts_content)
    
    img_src,iframe_src=parse_html(full_content)
    #print(img_src,iframe_src)
    for src in img_src:
        #print(src)
        src=src.replace("\\","")
        #print("*************************************************************",src[1:-1])
        url_tcstring=parse_url(src[1:-1])
        #print(url_tcstring)
        if url_tcstring !=[]:
            l.append(url_tcstring)
    for src in iframe_src:
        #print(src)
        src=src.replace("\\","")
        url_tcstring=parse_url(src[1:-1])
        #print("*************************************************************",src[1:-1])
        #print(url_tcstring)
        if url_tcstring !=[]:
            l.append(url_tcstring)

    return l


def tcstring(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        tcs_access = data.get('tcstring', "")
        if tcs_access!="":
            idx=tcs_access.find("sc-TCData")
            #print(tcs_access[idx+13:-1])
            return tcs_access[idx+13:-1]
        else:
            return tcs_access

def get_tccookie(url):
    l=[]
    try:
        file_path = f"/home/usenix/Desktop/dataset_3/{url}/browsing_data1.json"  # Change this to the actual file path
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            list_cookies = data.get('cookies', [])
            #print("---------------",list_cookies)
            for c in list_cookies:
                
                v=c['value']
                n=c['name']
                #print(n,v)
                if v[0]=="C" and v[-1]=="A":
                    consent=decode_v2(v)
                    CMP_ID=consent.cmp_id
                    CMP_name=get_cmp_name(CMP_ID)
                    CMP_purposes=[consent.purposes_consent,consent.purposes_legitimate_interests,consent.special_features_optin]
                    if CMP_name==None:
                        continue
                    else:
                        l.append([n,v])
            #print("COOOOOOKIIIIIEEESSSSS",l)
            return l
    except Exception as ex:
        #print("aaaahhhhhhh",ex)
        return l

def get_tcstring(url):
    try:
        file_path = f"/home/usenix/Desktop/dataset_3/{url}/browsing_data1.json"  # Change this to the actual file path
        tcs=tcstring(file_path)
        #print(tcs)
        return tcs
    except Exception as e:
        #print(e)
        return ""
        pass

def get_tcls(url):
    l=[]
    try:
        file_path = f"/home/usenix/Desktop/dataset_3/{url}/browsing_data1.json"
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            #indexeddb = data.get('indexeddb', {})
            level1 = data.get('localStorage', {})
            #cookies = data.get('cookies', [])
            #res_entries = data.get('res_entries', [])


            l=[]
            # Process localstorage
            #print("\nLocalStorage:")
            # print(level1)
            for k1, v1 in level1.items():
                try:
                    level2=json.loads(v1)
                    for k2, v2 in level2.items():
                        # print(k2,type(v2))
                        if type(v2) == dict:
                            level3=v2
                            for k3, v3 in level3.items():
                                if type(v3) == dict:
                                    level4=v3
                                    for k4, v4 in level4.items():
                                        if type(v4) == str:
                                            #print("string4",k4)
                                            l.append([k4,v4])
                                elif type(v3) ==str:
                                    #print("string3",k3)
                                    l.append([k3,v3])

                        elif type(v2) ==str:
                            #print("string2",k2)
                            l.append([k2,v2])
                except:
                    #if type(v1) !=str:
                            #print("list",k1,v1)
                    continue
        #return l
        l2=[]
        for ll in l:
            #print(ll,type(ll))
            v=ll[1]
            n=ll[0]
            #print(n,v)
            if len(v)>0:
                if v[0]=="C" and v[-1]=="A":
                    consent=decode_v2(v)
                    CMP_ID=consent.cmp_id
                    CMP_name=get_cmp_name(CMP_ID)
                    CMP_purposes=[consent.purposes_consent,consent.purposes_legitimate_interests,consent.special_features_optin]
                    if CMP_name==None:
                        continue
                    else:
                        l2.append([n,v]) 
        return l2
    except Exception as e:
        #print(e)
        return l
        pass



def cookie_dict(cookie_str):
    #cookie_string = "__adroll=7720d37b1dbb63bd11862e471d957ab7-a_1719256360; Version=1; Expires=Thu, 24-Jul-2025 19:12:40 GMT; Max-Age=34128000; Path=/; HttpOnly; SameSite=None; Secure; Domain=d.adroll.com"
    cookie_string = cookie_str
    # Split the string by ';' to separate the attributes
    attributes = cookie_string.split(';')

    # Extract the name and value from the first part
    name_value = attributes[0].split('=')
    name = name_value[0].strip()
    value = name_value[1].strip()

    # Create the dictionary with 'name' and 'value' keys
    cookie_dict = {
        "name": name,
        "value": value
    }

    # Iterate over the remaining attributes and add them to the dictionary
    for attribute in attributes[1:]:
        # Split attribute into key and value
        key_value = attribute.split('=')
        if len(key_value) == 2:
            key = key_value[0].strip()
            attr_value = key_value[1].strip()
        else:
            # Handle attributes without a value (e.g., HttpOnly, Secure)
            key = key_value[0].strip()
            attr_value = True
        cookie_dict[key] = attr_value

    # Print the resulting dictionary
    return cookie_dict

def flatten_dict(data):
    flattened_data = {}
    for key, list_of_dicts in data.items():
        flat_row = {}
        for i, d in enumerate(list_of_dicts):
            for k, v in d.items():
                flat_row[f"{k}_{i}"] = v
        flattened_data[key] = flat_row
    return flattened_data



df2 = pd.read_csv('../List_of_websites/top_200.csv')

df3 = pd.read_csv('withdrawal_not_possible.csv')

ll= list(df3['Website'])

print(df2.keys())

fieldnames = ['Rank','Website','curr_cookies','curr_ls','curr_tcs','ano','unique','req_cookies','res_cookies','tp']

print(fieldnames)

with open('anomalies_after_acceptance.csv',mode='w',newline='') as csv_file: # Creates a csv which has network data, cookies, localstorage, and tcfstring returned by tcfapi to find inconsistencies discussed in RQ3 and RQ4. 
# with open('anomalies_after_revocation.csv',mode='w',newline='') as csv_file: # Creates similar csv, but for "after revocation stage"
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    #blah=["forbes.com","aol.com","newsday"]
    websites={}
    id=-1
    for url in df2['Websites']:
        
    #for url in url_list:
        if url not in ll:
            id=id+1
            #if url in blah:
            #    continue
            print("==============",url,"==============")
            
            try:
                file_path = f"/home/usenix/Desktop/dataset_3/{url}/res1.json"  # Change this to the actual file path
                return_obj1=parse_json_file(file_path)
                print(len(return_obj1.keys()))
                entries={}
                
                curr_tcstring=get_tcstring(url)
                
                if len(curr_tcstring)>1 and (curr_tcstring in str(return_obj1)):
                    flag =0
                    for k,v in return_obj1.items():

                        if curr_tcstring in str(v):
                            #print("YAAAYYYYYY")
                            flag =1

                        entries[k]={}
                        #print(k,v)
                        entries[k]['req']=[]
                        entries[k]['res']=[]
                        entries[k]['ini']=[]
                        entries[k]['url']=""
                        
                        for entry in v:
                            #print("INI")
                            try:
                                l=[]
                                parse_stack(entry['params']['initiator']['stack'],l)
                                #print(l)
                                if flag ==1:
                                    entries[k]['ini'].append(l)

                            except:
                                pass
                            #print("REQUEST")
                            try:
                                entries[k]['url']=entry['params']['request']['url']
                                req=entry['params']['request']
                                if entry['params']['request']['method']=="POST":
                                    postdata_tcstring=parse_postdata(entry['params']['request']['postData'])
                                    #print(postdata_tcstring)
                                    if curr_tcstring in postdata_tcstring:
                                        flag = 1
                                    if flag ==1:
                                        entries[k]['req'].append([urlparse(entry['params']['request']['url']).hostname,entry['params']['request']['method'],postdata_tcstring])
                                    """
                                    if postdata_tcstring !=[]:
                                        print(entry['params']['requestId'])
                                        print("--------------",entry['params']['request']['method'],"--------------")
                                        print(entry['params']['request']['url'])
                                        #print("POSTDATA:",entry['params']['request']['postData'])
                                        print(postdata_tcstring)
                                    """
                                else:
                                    url_tcstring=parse_url(entry['params']['request']['url'])
                                    #print(url_tcstring)
                                    if flag ==1:
                                        entries[k]['req'].append([urlparse(entry['params']['request']['url']).hostname,entry['params']['request']['method'],url_tcstring])

                                    """
                                    if url_tcstring != []:
                                        print(entry['params']['requestId'])
                                        print("--------------",entry['params']['request']['method'],"--------------")
                                        print(urlparse(entry['params']['request']['url']).hostname)
                                        print(url_tcstring)
                                    """
                                    
                            except Exception as e:
                                #print(e)
                                pass
                            
                            #print("RESPONSE")
                            try:
                                response_body=entry['params']['response']['body']
                                #print(url_tcstring[0][1])
                                #print(type(entry['params']['response']['body']))
                                """
                                if url_tcstring[0][1] in response_body:
                                    #print(response_body)
                                    print("*****************************************",url)
                                    print(entry['params']['requestId'])
                                """
                                try:
                                    if entry['params']['response']['mimeType']=="application/json":
                                        #print("AAHHH",response_body)
                                        body_tcstring=parse_loop(json.loads(response_body))
                                        #print("JSON",body_tcstring)
                                        if flag ==1:
                                            entries[k]['res'].append(["JSON",body_tcstring])
                                except Exception as e:
                                    #print(e)
                                    pass
                                
                                try:
                                    if entry['params']['response']['mimeType']=="application/json":
                                        response_body=entry['params']['response']['body']
                                        html_tcstring=extract_html_from_string(response_body)
                                        #print("HTML",html_tcstring)
                                        if flag ==1:
                                            entries[k]['res'].append(["HTML",html_tcstring])
                                except:
                                    pass

                            except:
                                pass
                            
                            ## Collecting cookies in requests
                            try:
                                cookie_list=entry['params']['associatedCookies']
                                #print(url)
                                #print(entries[k]['url'])
                                #print("cookkiiieessss",urlparse(entries[k]['url']).hostname,url)
                                if urlparse(entries[k]['url']).hostname != url: 
                                    #print("cookkiiieessss",urlparse(entries[k]['url']).hostname,url)
                                    temp_c=[]
                                    for c in cookie_list:
                                        value=c["cookie"]["value"]
                                        cmp_id=decode_v2(value).cmp_id
                                        cmp_name=get_cmp_name(cmp_id)
                                        if cmp_name!=None:
                                            if value[0]=="C"and value[-1]=="A":
                                                if flag ==1:
                                                    temp_c.append([c["cookie"]["name"],c["cookie"]["value"],c["cookie"]["domain"],entries[k]['url']])
                                    if temp_c!=[]:
                                        if flag ==1:    
                                            entries[k]['req'].append(["Cookies in request",temp_c])
                                    #print(temp_c)
                            except Exception as e:
                                #print(e)
                                pass
                            
                            ## Collecting cookies in responses set-header:

                            try:
                                setcookie_entry=entry['params']['headers']['set-cookie']
                                setcookie_list=setcookie_entry.split('\n')
                                #print("SETCOOOOOKIIIEEEE",setcookie_list)
                                temp_c=[]
                                #print(setcookie_list)
                                for cc in setcookie_list:
                                    c_dict=cookie_dict(cc)
                                    #print(c_dict,type(c_dict))
                                    
                                    value=c_dict['value']
                                    #print("aa",value)
                                    temp_c=[c_dict["name"],c_dict["value"],c_dict["Domain"],entries[k]['url']]
                                if temp_c!=[]:    
                                    if flag ==1:
                                        entries[k]['res'].append(["Cookies in response",temp_c])
                                
                                #print("",temp_c)
                                #entries[k]['res'].append(["Cookies in response",setcookie_list])

                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                #print(exc_type, fname, exc_tb.tb_lineno)
                                #print(e)
                                pass

                    anomalies_list={}
                    request_cookies={}
                    response_cookies={}
                    tp_sites={}
                    all_tcstring_in_websites=[]

                    curr_tcstring=get_tcstring(url)
                    curr_cookies=get_tccookie(url)
                    curr_ls=get_tcls(url)
                    final_tcs=[]

                    print("curr:",curr_tcstring)

                    for r_id,e in entries.items():

                        #print("----------------------")
                        #print()
                        #print("CUUURRRRR:",curr_tcstring)
                        #print("REQUEST ID=",r_id)
                        
                        req=e['req']
                        res=e['res']
                        ini=e['ini']
                        req_url=e['url']
                        recievers_list=[]
                        req_tcs_list=[]
                        res_tcs_list=[]
                        req_cookies=[]
                        res_cookies=[]
                        req_url=""

                        for q in req:
                            #print(q)
                            if q[-1] !=[]:
                                if q[0]=="Cookies in request":
                                    req_cookies.append(q[-1])
                                else:
                                    #print("aaaaaaaaaaaaaaaaaaah",q[0])
                                    recievers_list.append(q[0])
                                    for qq in q[-1]:
                                        if len(qq)==3:
                                            req_tcs_list.append(qq[-1])
                                            req_url=q[0]
                                        else:
                                            req_tcs_list.append(qq[-1])
                        #print("------------------------------------")
                        for q in res:
                            #print("YYYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYYYYYYYYYYYYYYYYYYYYYYY")
                            #print(q[-1])
                            if q[-1] !=[]:
                                if q[0]=="Cookies in response":
                                    res_cookies.append(q[-1])
                                else:
                                    for qq in q[-1]:
                                        print("aaahhh:",qq)
                                        try:
                                            if q[0]=="JSON":
                                                #print("MMMMMMMMMMMMMMMMMMMMMMMAAAAHHH",qq[-1])
                                                if len(qq[-1])==3:
                                                    res_tcs_list.append(qq[-1][-1])
                                                    recievers_list.append(qq[-1][0])
                                                else:
                                                    res_tcs_list.append(qq[-1])
                                            else:
                                                if len(qq[-1])==3:
                                                    res_tcs_list.append(qq[-1][-1])
                                                    recievers_list.append(qq[-1][0])
                                                else:
                                                    res_tcs_list.append(qq[-1])
                                        except Exception as ex:
                                            print(ex)
                                            pass


                        #recievers_list=[]
                        #req_tcs_list=[]
                        #res_tcs_list=[]
                        #req_cookies=[]
                        #res_cookies=[]


                        print(req_tcs_list)
                        print(res_tcs_list)
                        
                        unique_list = list(dict.fromkeys(req_tcs_list))

                        if len(unique_list)!=0:
                            #print("------------------------------",unique_list)
                            for k in range(len(unique_list)):    
                                if curr_tcstring != unique_list[k]:
                                    anomalies_list[r_id]=[e,unique_list[k],"REQ"]


                        try:
                            unique_list = list(dict.fromkeys(res_tcs_list))
                            if len(unique_list)!=0:
                                #print("------------------------------",unique_list)
                                for k in range(len(unique_list)):    
                                    if curr_tcstring != unique_list[k]:
                                        anomalies_list[r_id]=[e,unique_list[k],"RES"]
                        except:
                            pass
                        
                        total_list=req_tcs_list+res_tcs_list
                        for p in total_list:
                            final_tcs.append(p)

                        if len(req_cookies)>0:
                            request_cookies[r_id]=req_cookies
                        
                        if len(res_cookies)>0:
                            response_cookies[r_id]=res_cookies
                        
                        temp=[]
                        #print("liisssttt:",recievers_list)
                        for r in recievers_list:
                            try:
                                if str(url) not in str(urlparse(r).hostname):
                                    temp.append(r)
                            except Exception as e:
                                print(e)
                                pass
                        
                        if temp!=[]:
                            tp_sites[r_id]=temp
                    

                    try:
                        #print("pehle:",final_tcs)
                        unique_list=[]
                        
                        unique_list = list(dict.fromkeys(final_tcs))
                        
                    except Exception as ex:
                        #print("baad",final_tcs)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        #print(exc_type, fname, exc_tb.tb_lineno)
                        #print(ex)
                        pass
                    #if len(unique_list)>1:
                    #    print(unique_list)

                    tt=[]
                    #print(type(tp_sites))
                    for k,t in tp_sites.items():
                        for j in t:
                            tt.append(j)
                    #print(len(tt))

                    unique_list2 = list(dict.fromkeys(tt))
                    try:
                        unique_list3=[]
                        unique_list3 = list(dict.fromkeys(final_tcs))
                    except:
                        pass
                        #unique_list3 = [item for sublist in final_tcs for item in sublist]
                        #unique_list3=[]

                    #websites[url]=[curr_cookies,curr_ls,curr_tcstring,anomalies_list,len(unique_list),request_cookies,response_cookies,[len(tp_sites.keys()),unique_list2]]
                    websites[url]=[df2['Rank'][id],df2['Website'][id],curr_cookies,curr_ls,curr_tcstring,json.dumps(anomalies_list),len(unique_list),json.dumps(request_cookies),json.dumps(response_cookies),[len(tt),len(unique_list2),unique_list2],[len(final_tcs),len(unique_list3),unique_list3]]
                    writer.writerow([df2['Rank'][id],df2['Website'][id],curr_cookies,curr_ls,curr_tcstring,json.dumps(anomalies_list),len(unique_list),json.dumps(request_cookies),json.dumps(response_cookies),[len(tt),len(unique_list2),unique_list2],[len(final_tcs),len(unique_list3),unique_list3]])
                else:
                    print("YAHHAAA")
                    flag =1
                    for k,v in return_obj1.items():

                        if curr_tcstring in str(v):
                            #print("YAAAYYYYYY")
                            flag =1

                        entries[k]={}
                        #print(k,v)
                        entries[k]['req']=[]
                        entries[k]['res']=[]
                        entries[k]['ini']=[]
                        entries[k]['url']=""
                        
                        for entry in v:
                            #print("INI")
                            try:
                                l=[]
                                parse_stack(entry['params']['initiator']['stack'],l)
                                #print(l)
                                if flag ==1:
                                    entries[k]['ini'].append(l)

                            except:
                                pass
                            #print("REQUEST")
                            try:
                                entries[k]['url']=entry['params']['request']['url']
                                req=entry['params']['request']
                                if entry['params']['request']['method']=="POST":
                                    postdata_tcstring=parse_postdata(entry['params']['request']['postData'])
                                    #print(postdata_tcstring)
                                    if flag ==1:
                                        entries[k]['req'].append([urlparse(entry['params']['request']['url']).hostname,entry['params']['request']['method'],postdata_tcstring])
                                    """
                                    if postdata_tcstring !=[]:
                                        print(entry['params']['requestId'])
                                        print("--------------",entry['params']['request']['method'],"--------------")
                                        print(entry['params']['request']['url'])
                                        #print("POSTDATA:",entry['params']['request']['postData'])
                                        print(postdata_tcstring)
                                    """
                                else:
                                    url_tcstring=parse_url(entry['params']['request']['url'])
                                    #print(url_tcstring)
                                    if flag ==1:
                                        entries[k]['req'].append([urlparse(entry['params']['request']['url']).hostname,entry['params']['request']['method'],url_tcstring])

                                    """
                                    if url_tcstring != []:
                                        print(entry['params']['requestId'])
                                        print("--------------",entry['params']['request']['method'],"--------------")
                                        print(urlparse(entry['params']['request']['url']).hostname)
                                        print(url_tcstring)
                                    """
                                    
                            except Exception as e:
                                #print(e)
                                pass
                            
                            #print("RESPONSE")
                            try:
                                #print("RESPONSE")
                                response_body=entry['params']['response']['body']
                                #print(url_tcstring[0][1])
                                #print(entry['params']['response']['body'])
                                
                                """
                                if url_tcstring[0][1] in response_body:
                                    print(response_body)
                                    print("*****************************************",url)
                                    print(entry['params']['requestId'])
                                """
                                
                                try:
                                    if entry['params']['response']['mimeType']=="application/json":
                                        #print("AAHHH",response_body)
                                        body_tcstring=parse_loop(json.loads(response_body))
                                        #print("JSON",body_tcstring)
                                        if flag ==1:
                                            entries[k]['res'].append(["JSON",body_tcstring])
                                except Exception as e:
                                    #print(e)
                                    pass
                                
                                try:
                                    if entry['params']['response']['mimeType']=="application/json":
                                        response_body=entry['params']['response']['body']
                                        html_tcstring=extract_html_from_string(response_body)
                                        #print("HTML",html_tcstring)
                                        if flag ==1:
                                            entries[k]['res'].append(["HTML",html_tcstring])
                                except:
                                    pass

                            except:
                                pass
                            
                            ## Collecting cookies in requests
                            try:
                                cookie_list=entry['params']['associatedCookies']
                                #print(url)
                                #print(entries[k]['url'])
                                #print("cookkiiieessss",urlparse(entries[k]['url']).hostname,url)
                                if urlparse(entries[k]['url']).hostname != url: 
                                    #print("cookkiiieessss",urlparse(entries[k]['url']).hostname,url)
                                    temp_c=[]
                                    for c in cookie_list:
                                        value=c["cookie"]["value"]
                                        cmp_id=decode_v2(value).cmp_id
                                        cmp_name=get_cmp_name(cmp_id)
                                        if cmp_name!=None:
                                            if value[0]=="C"and value[-1]=="A":
                                                if flag ==1:
                                                    temp_c.append([c["cookie"]["name"],c["cookie"]["value"],c["cookie"]["domain"],entries[k]['url']])
                                    if temp_c!=[]:
                                        if flag ==1:    
                                            entries[k]['req'].append(["Cookies in request",temp_c])
                                    #print(temp_c)
                            except Exception as e:
                                #print(e)
                                pass
                            
                            ## Collecting cookies in responses set-header:

                            try:
                                setcookie_entry=entry['params']['headers']['set-cookie']
                                setcookie_list=setcookie_entry.split('\n')
                                #print("SETCOOOOOKIIIEEEE",setcookie_list)
                                temp_c=[]
                                #print(setcookie_list)
                                for cc in setcookie_list:
                                    c_dict=cookie_dict(cc)
                                    #print(c_dict,type(c_dict))
                                    
                                    value=c_dict['value']
                                    #print("aa",value)
                                    temp_c=[c_dict["name"],c_dict["value"],c_dict["Domain"],entries[k]['url']]
                                if temp_c!=[]:    
                                    if flag ==1:
                                        entries[k]['res'].append(["Cookies in response",temp_c])
                                
                                #print("",temp_c)
                                #entries[k]['res'].append(["Cookies in response",setcookie_list])

                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                #print(exc_type, fname, exc_tb.tb_lineno)
                                #print(e)
                                pass

                    anomalies_list={}
                    request_cookies={}
                    response_cookies={}
                    tp_sites={}
                    all_tcstring_in_websites=[]

                    curr_tcstring=get_tcstring(url)
                    curr_cookies=get_tccookie(url)
                    curr_ls=get_tcls(url)
                    final_tcs=[]

                    print("curr:",curr_tcstring)

                    for r_id,e in entries.items():

                        #print("----------------------")
                        #print()
                        #print("CUUURRRRR:",curr_tcstring)
                        #print("REQUEST ID=",r_id)
                        
                        req=e['req']
                        res=e['res']
                        ini=e['ini']
                        req_url=e['url']
                        recievers_list=[]
                        req_tcs_list=[]
                        res_tcs_list=[]
                        req_cookies=[]
                        res_cookies=[]
                        req_url=""

                        for q in req:
                            #print(q)
                            if q[-1] !=[]:
                                if q[0]=="Cookies in request":
                                    req_cookies.append(q[-1])
                                else:
                                    #print("aaaaaaaaaaaaaaaaaaah",q[0])
                                    recievers_list.append(q[0])
                                    for qq in q[-1]:
                                        if len(qq)==3:
                                            req_tcs_list.append(qq[-1])
                                            req_url=q[0]
                                        else:
                                            req_tcs_list.append(qq[-1])

                        for q in res:
                            #print("YYYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYYYYYYYYYYYYYYYYYYYYYYY")
                            print(q[-1])
                            if q[-1] !=[]:
                                if q[0]=="Cookies in response":
                                    res_cookies.append(q[-1])
                                else:
                                    for qq in q[-1]:
                                        if q[0]=="JSON":
                                            #print("JSSSONNNN")
                                            if len(qq[-1])==3:
                                                res_tcs_list.append(qq[-1][-1])
                                                recievers_list.append(qq[-1][0])
                                            else:
                                                res_tcs_list.append(qq[-1])
                                        else:
                                            if len(qq[-1])==3:
                                                res_tcs_list.append(qq[-1][-1])
                                                recievers_list.append(qq[-1][0])
                                            else:
                                                res_tcs_list.append(qq[-1])

                        #recievers_list=[]
                        #req_tcs_list=[]
                        #res_tcs_list=[]
                        #req_cookies=[]
                        #res_cookies=[]


                        #print(req_tcs_list)
                        #print(res_tcs_list)
                        
                        unique_list = list(dict.fromkeys(req_tcs_list))

                        if len(unique_list)!=0:
                            #print("------------------------------",unique_list)
                            for k in range(len(unique_list)):    
                                if curr_tcstring != unique_list[k]:
                                    anomalies_list[r_id]=[e,unique_list[k],"REQ"]


                        
                        unique_list = list(dict.fromkeys(res_tcs_list))

                        if len(unique_list)!=0:
                            #print("------------------------------",unique_list)
                            for k in range(len(unique_list)):    
                                if curr_tcstring != unique_list[k]:
                                    anomalies_list[r_id]=[e,unique_list[k],"RES"]
                        
                        total_list=req_tcs_list+res_tcs_list
                        for p in total_list:
                            final_tcs.append(p)

                        if len(req_cookies)>0:
                            request_cookies[r_id]=req_cookies
                        
                        if len(res_cookies)>0:
                            response_cookies[r_id]=res_cookies
                        
                        temp=[]
                        #print("liisssttt:",recievers_list)
                        for r in recievers_list:
                            try:
                                if str(url) not in str(urlparse(r).hostname):
                                    temp.append(r)
                            except Exception as e:
                                print(e)
                                pass
                        
                        if temp!=[]:
                            tp_sites[r_id]=temp
                    

                    unique_list = list(dict.fromkeys(final_tcs))
                    #if len(unique_list)>1:
                    #    print(unique_list)

                    tt=[]
                    #print(type(tp_sites))
                    for k,t in tp_sites.items():
                        for j in t:
                            tt.append(j)
                    #print(len(tt))

                    unique_list2 = list(dict.fromkeys(tt))

                    unique_list3 = list(dict.fromkeys(final_tcs))

                    #websites[url]=[curr_cookies,curr_ls,curr_tcstring,anomalies_list,len(unique_list),request_cookies,response_cookies,[len(tp_sites.keys()),unique_list2]]
                    websites[url]=[df2['Rank'][id],df2['Website'][id],curr_cookies,curr_ls,curr_tcstring,json.dumps(anomalies_list),len(unique_list),json.dumps(request_cookies),json.dumps(response_cookies),[len(tt),len(unique_list2),unique_list2],[len(final_tcs),len(unique_list3),unique_list3]]
                    writer.writerow([df2['Rank'][id],df2['Website'][id],curr_cookies,curr_ls,curr_tcstring,json.dumps(anomalies_list),len(unique_list),json.dumps(request_cookies),json.dumps(response_cookies),[len(tt),len(unique_list2),unique_list2],[len(final_tcs),len(unique_list3),unique_list3]])


            except Exception as e:
                #print("Error:",ex)

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                pass

            
            print("----------------------------------------------------")
            for web,data in websites.items():
                #print(len(data))
                for d in data:
                    print(d)
            print("----------------------------------------------------")
            

