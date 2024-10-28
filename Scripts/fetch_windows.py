from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

def get_browser_log_entries(driver):
    """get log entreies from selenium and add to python logger before returning"""
    loglevels = { 'NOTSET':0 , 'DEBUG':10 ,'INFO': 20 , 'WARNING':30, 'ERROR':40, 'SEVERE':40, 'CRITICAL':50}

    #initialise a logger
    browserlog = logging.getLogger("chrome")
    #get browser logs
    slurped_logs = driver.get_log('browser')
    for entry in slurped_logs:
        #convert broswer log to python log format
        rec = browserlog.makeRecord("%s.%s"%(browserlog.name,entry['source']),loglevels.get(entry['level']),'.',0,entry['message'],None,None)
        rec.created = entry['timestamp'] /1000 # log using original timestamp.. us -> ms
        try:
            #add browser log to python log
            browserlog.handle(rec)
        except:
            print(entry)
    #and return logs incase you want them
    return slurped_logs

def export_indexeddb_localstorage_cookies(url,flag,path):
    # Set up browsermob-proxy server
    server = Server(r'C:\Users\kkpg2\Downloads\browsermob-proxy-2.1.4-bin\browsermob-proxy-2.1.4\bin\browsermob-proxy')
    # Path to the browsermob-proxy executable
    server.start()
    proxy = server.create_proxy()

    postmessage_script = """
    window.addEventListener("message", function(e) {
        var callid = "";
        var version;
        var debug = false;
        if (e.data.__cmpCall) {
        callid = e.data.__cmpCall.callId;
            version = 1;
        } else if (debug && e.data.__cmpReturn) {
        callid = e.data.__cmpReturn.callId;
            version = 1;
        } else if (e.data.__tcfapiCall) {
        callid = e.data.__tcfapiCall.callId;
            version = 2;
        } else if (debug && e.data.__tcfapiReturn) {
        callid = e.data.__tcfapiReturn.callId;
            version = 2;
        } else {
        return;
        }
        var re = /^uCookie_/;
        if (!re.test(callid) || debug) {
            if (version == 1) {
            console.log("sc-postMessage: " + e.origin, callid, e.source, e.data, e);
            } else {
                if (debug) {
                    var callid = "";
                    if (e.data.__tcfapiCall) {
                        callid = e.data.__tcfapiCall.callId;
                    }
                    if (e.data.__tcfapiReturn) {
                        callid = e.data.__tcfapiReturn.callId;
                    }
                    console.log(e.data, callid);
                }
            console.log("sc-postMessage_v2: " + e.origin, callid, e.source, e.data, e);
            }
        }
    });
    """
	
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['goog:loggingPrefs'] = { 'browser':'ALL' }
    service = Service(executable_path=r'C:\Users\kkpg2\.wdm\drivers\chromedriver\win64\124.0.6367.60\chromedriver-win32\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('ignore-certificate-errors')
    # options.add_extension('C:\Users\kkpg2\OneDrive\Desktop\consent_withdrawal\Cookinspect\extensions\get_euconsent.crx')
    options.set_capability("goog:loggingPrefs", {  # old: loggingPrefs
    "browser": "ALL"})
	# options.add_argument("--proxy-server={0}".format(proxy.proxy))
    driver = webdriver.Chrome(service=service, options=options)
    domain=url
    url="http://"+url
    proxy.new_har("google")
    driver.get(url)
    if flag==0:
        r=3
    else:
        r=1
    for i in range(r):
        indexed_db_data = driver.execute_script("return window.indexedDB")
        local_storage_data = driver.execute_script("return window.localStorage")
        cookies_data = driver.get_cookies()
        driver.execute_script(postmessage_script)
        time.sleep(5)
        print("---------------------------------------------------")
        res_entries = proxy.har
        # for entry in res_entries['log']['entries']:
        #     print(entry['request'])
        try:
            res = driver.execute_script('return document.getElementsByName("__tcfapiLocator").length;')
        finally:
            frame=0
            if int(res) > 0:
                frame=res
        
        consolemsgs=[]
        try:
            # res = driver.execute_script('if (window.__tcfapi) return "ok";', None)
            driver.execute_script('if (__tcfapi("getTCData", 2, function(val, success) { console.log("sc-TCData=",val.tcString)})) return "ok";', None)
            consolemsgs = get_browser_log_entries(driver)
        except:
            consolemsgs=[]

        logs=get_browser_log_entries(driver)
        post_method=[]
        for log in logs:
            if "sc-postMessage" in log['message']:
                # print(log)
                post_method=logs
            # print(consolemsgs)
        
        tcstring=""
        for msg in consolemsgs:
            if "sc-TCData" in msg['message']:
                tcstring=msg['message']
        data = {
            "indexedDB": indexed_db_data,
            "localStorage": local_storage_data,
            "cookies": cookies_data,
            "res_entries": res_entries,
            "post_method_present":post_method,
            "console_msgs":consolemsgs,
            "tcstring":tcstring,
            "iframe":frame
        }
        if flag==0 and i==0:
            driver.save_screenshot(f'../latest/{domain}/screenshot{i}.png')
            with open(f"../latest/{domain}/browsing_data{i}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

        elif flag==0 and i==1:
            b=input("Accept on banner/if present, scroll down then enter b1/b2:")
            path.append(b)
            driver.save_screenshot(f'../latest/{domain}/screenshot{i}.png')
            with open(f"{domain}/browsing_data{i}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
        
        elif flag==0 and i==2:
            icon=input("Click on icon /link on footer then enter i1/i2:")
            path.append(icon)
            driver.save_screenshot(f'../latest/{domain}/screenshot{i}.png')
        
        elif flag==0 and i==2:
            s=input("Revoke consent and based on popup(1 step) or multiple steps enter s1/s2:")
            w=input("Could withdraw or not w1/w2:")
            path.append(s)
            path.append(w)
            with open(f"../latest/{domain}/browsing_data{i}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

        elif flag==1:
            driver.save_screenshot(f'../latest/{domain}/screenshot3.png')
            jt=input("Reject on banner then based on direct option enter j1/j2:")
            with open(f"{domain}/browsing_data3.json", "w") as json_file:
                json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)7s:%(message)s')
    logging.info("start")
    url = input("Enter the URL to extract data from: ")
    flag=0
    os.mkdir(url)
    path=[]
    try:
        path.append("r1")
        export_indexeddb_localstorage_cookies(url,flag,path)
        flag=1
        export_indexeddb_localstorage_cookies(url,flag,path)
    except:
        print("Failed:",url)
        path.append("r2")
        with open('failed_websites.txt','a') as file:
            file.write(url+"\n")

    # demo(url)
    logging.info("end")