#from browsermobproxy import Server

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





indexeddb_script="""

var request = window.indexedDB.open("CookieBlockHistory", 1);

request.onsuccess = function(event) {

    var db = event.target.result;

    var transaction = db.transaction(["cookies"], "readonly");

    var objectStore = transaction.objectStore("cookies");

    var data = [];

    objectStore.openCursor().onsuccess = function(event) {

        var cursor = event.target.result;

        if (cursor) {

            data.push(cursor.value);

            cursor.continue();

        }

    };

    transaction.oncomplete = function() {

        console.log("IDB:",JSON.stringify(data));

    };

};

"""



delete_idb_script="""

var request = window.indexedDB.open("CookieBlockHistory", 1);

request.onsuccess = function(event) {

    var db = event.target.result;

    var transaction = db.transaction(["cookies"], "readwrite");

    var objectStore = transaction.objectStore("cookies");

    var deleteRequest = objectStore.clear();

};

"""



ot_script = """

    var originalValue = window.OnetrustActiveGroups;

    Object.defineProperty(window, 'OnetrustActiveGroups', {

    get: function() {

        if (document.currentScript) {

            console.log('***********Access to OneTrustActiveGroups:', originalValue,document.currentScript.src);

        }

        else{

            //console.log('***********Access to OneTrustActiveGroups:', originalValue,"");

            try{

                document.currentScript.src

            }catch(e){

                console.log('EERRROOOOORRRA', originalValue,e.stack)

            }

        }

        return originalValue;

    },

    set: function(value) {

        if (document.currentScript) {

            console.log('++++++++++++Assignment to OneTrustActiveGroups:', value,document.currentScript.src);

        }

        else{

            //console.log('++++++++++++Assignment to OneTrustActiveGroups:', value,"");

            try{

                document.currentScript.src

            }catch(e){

                console.log('EERRROOOOORRRW', value,e.stack)

            }

        }

        

        originalValue=value;

    }

    });

    """



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

tcf_intercept="""

        var originalTCFApi = window.__tcfapi;

        window.__tcfapi = function(command, version, callback, parameter) {

            try{

                throw new Error();

            }catch(e){

                console.log('__tcfapi call intercepted:', command,e.stack);

            }

            

            // You can log or manipulate the command here as needed

            return originalTCFApi.apply(this, arguments);

        };

        """



def get_selenium_driver():

    desired_capabilities = DesiredCapabilities.CHROME 

    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL","browser": "ALL"}

    options = webdriver.ChromeOptions()

    options.add_argument(r"--user-data-dir=/home/usenix/.config/google-chrome")

    #options.add_argument(r"--user-data-dir=/opt/google/chrome/google-chrome")

    #provide the profile name with which we want to open browser

    options.add_argument(r'--profile-directory=Default')

    options.add_extension('CookieBlock 1.1.0.0.crx')

    #options.set_capability("goog:loggingPrefs", {  # old: loggingPrefs

    #"browser": "ALL"})

    #specify where your chrome driver present in your pc

    #driver = webdriver.Chrome(executable_path='/home/usenix/Downloads/chromedriver/chromedriver',options=options)

    driver = webdriver.Chrome(executable_path='/home/usenix/Downloads/chromedriver/chromedriver',options=options,desired_capabilities=desired_capabilities)

    return driver



def delete_cookieblock_history(driver):

    driver.get('chrome-extension://fbhiolckidkciamgcobkokpelckgnnol/options/cookieblock_options.html')

    time.sleep(5)

    driver.execute_script(delete_idb_script)



def get_cookie_data(driver):

    consolemsgs=[]

    try:

        driver.execute_script("window.open('');")

        driver.switch_to.window(driver.window_handles[1])



        driver.get('chrome-extension://fbhiolckidkciamgcobkokpelckgnnol/options/cookieblock_options.html')

        #print("Current Page Title is : %s" %driver.title)

        indexeddb_data = driver.execute_script(indexeddb_script)

        time.sleep(2)

        consolemsgs = get_browser_log_entries(driver)

        #print(consolemsgs[-1])

    

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        # Switch back to the first tab with URL A

    except Exception as e:

        print("*****************",e)

        print(consolemsgs)

    

    

    print("=========================")

    return consolemsgs

        



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

            continue



    #and return logs incase you want them

    return slurped_logs



def collect_data(driver):

    indexed_db_data = driver.execute_script("return window.indexedDB")

    local_storage_data = driver.execute_script("return window.localStorage")

    cookies = driver.get_cookies()

    

    try:

        res_entries = driver.execute_script("""

                    var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};

                    var network = performance.getEntries() || [];

                    return network;

                """)

        for res in res_entries:

            for key in res.keys():

                if type(res[key])!=str:

                    res[key]=str(res[key])

    except Exception as e:

        print(e)



    driver.execute_script(postmessage_script)

    

    time.sleep(5)



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

    except:

        pass

    

    try:

        # res = driver.execute_script('if (window.__tcfapi) return "ok";', None)

        otvar=driver.execute_script('return window.OnetrustActiveGroups;', None)

    except:

        otvar="error"

        pass



    

    logs = get_browser_log_entries(driver)



    print(logs)



    post_method=[]

    for log in logs:

        if "sc-postMessage" in log['message']:

            # print(log)

            post_method=logs

        # print(consolemsgs)

    

    tcstring=""

    for msg in logs:

        if "sc-TCData" in msg['message']:

            tcstring=msg['message']



    web_ot_access=[]

    web_tcf_access=[]

    for log in logs:

        if "********" in log['message']:

            l=log['message'].split()

            ls=[]

            for e in l:

                if "js" in e:

                    if "error" not in e:

                        if e[0] =="(":

                            e=e[1:]

                            if e[-1]=="n":

                                e=e[:-4]

                            else:

                                e=e[:-2]

                        else:

                            if e[-1]=="n":

                                e=e[:-3]

                            else:

                                e=e[:-1]



                        ls.append(e)

            # print(ls)

            if ls==[]:

                web_ot_access.append([url,"[+]Script which accessed:",l[3],l])

            else:

                web_ot_access.append([url,"[+]Script which accessed:",l[3],ls])



        if "+++++++++" in log['message']:

            l=log['message'].split()

            ls=[]

            for e in l:

                if "js" in e:

                    if "error" not in e:

                        if e[0] =="(":

                            e=e[1:]

                            if e[-1]=="n":

                                e=e[:-4]

                            else:

                                e=e[:-2]

                        else:

                            if e[-1]=="n":

                                e=e[:-3]

                            else:

                                e=e[:-1]



                        ls.append(e)

            # print(ls)

            if ls==[]:

                web_ot_access.append([url,"[+]Script which wrote:",l[3],l])

            else:

                web_ot_access.append([url,"[+]Script which wrote:",l[3],ls])



            # print("[+]Script which wrote:",l[3],ls)

        if "EERRROOOOORRRA" in log['message']:

            # print(log)

            l=log['message'].split()

            # print(log)

            ls=[]

            for e in l:

                if "js" in e:

                    if "error" not in e:

                        if e[0] =="(":

                            e=e[1:]

                            if e[-1]=="n":

                                e=e[:-4]

                            else:

                                e=e[:-2]

                        else:

                            if e[-1]=="n":

                                e=e[:-3]

                            else:

                                e=e[:-1]



                        ls.append(e)

            # print(ls)

            if ls ==[]:

                web_ot_access.append([url,"[+]Script which accessed:",l[3],l])

            else:

                web_ot_access.append([url,"[+]Script which accessed:",l[3],ls])



            # print("[+]Script which accessed:",l[3],ls)

        if "EERRROOOOORRRW" in log['message']:

            # print(log)

            l=log['message'].split()

            # print(log)

            ls=[]

            for e in l:

                if "js" in e:

                    if "error" not in e:

                        if e[0] =="(":

                            e=e[1:]

                            if e[-1]=="n":

                                e=e[:-4]

                            else:

                                e=e[:-2]

                        else:

                            if e[-1]=="n":

                                e=e[:-3]

                            else:

                                e=e[:-1]



                        ls.append(e)

            # print(ls)

            if ls==[]:

                web_ot_access.append([url,"[+]Script which wrote:",l[3],l])

            else:

                web_ot_access.append([url,"[+]Script which wrote:",l[3],ls])



            # print("[+]Script which wrote:",l[3],ls)

        if "__tcfapi" in log['message']:

            # print(log)

            l=log['message'].split()

            ls=[]

            for e in l:

                if "js" in e:

                    if "error" not in e:

                        if e[0] =="(":

                            e=e[1:]

                            if e[-1]=="n":

                                e=e[:-4]

                            else:

                                e=e[:-2]

                        else:

                            if e[-1]=="n":

                                e=e[:-3]

                            else:

                                e=e[:-1]



                        ls.append(e)

            if ls==[]:

                web_tcf_access.append([url,"[*]Script which accessed tcfAPI:",l[5],l])

            else:

                web_tcf_access.append([url,"[*]Script which accessed tcfAPI:",l[5],ls])



    cookies_data = get_cookie_data(driver)



    data = {

        "indexedDB": indexed_db_data,

        "localStorage": local_storage_data,

        "cookies": cookies,

        "cookiesCB": cookies_data,

        "res_entries": res_entries,

        "post_method_present":post_method,

        "console_msgs":consolemsgs,

        "tcstring":tcstring,

        "iframe":frame,

        "access_to_tcstring":web_tcf_access,

        "access_to_otag":web_ot_access,

        "otvar":otvar

    }







    return data



def network_capture(driver,domain,i):

    logs = driver.get_log("performance") 



    # Opens a writable JSON file and writes the logs in it 

    with open(f"{domain}/res{i}.json", "w", encoding="utf-8") as f: 

        f.write("[") 



        # Iterates every logs and parses it using JSON 

        for log in logs: 

            network_log = json.loads(log["message"])["message"] 



            # Checks if the current 'method' key has any 

            # Network related value. 

            if("Network.response" in network_log["method"] 

                    or "Network.request" in network_log["method"] 

                    or "Network.webSocket" in network_log["method"]):



                if network_log["method"] == "Network.responseReceived":

                    request_id = network_log["params"]["requestId"]

                    try:

                        body_data = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})

                        network_log["params"]["response"]["body"] = body_data['body']

                    except Exception as e:

                        network_log["params"]["response"]["body"] = None



                # Writes the network log to a JSON file by 

                # converting the dictionary to a JSON string 

                # using json.dumps(). 

                f.write(json.dumps(network_log)+",") 

        f.write("{}]")



def network_capture2(driver,domain):

    logs = driver.get_log("performance") 



    # Opens a writable JSON file and writes the logs in it 





    # Iterates every logs and parses it using JSON 

    for log in logs: 

        network_log = json.loads(log["message"])["message"] 



        # Checks if the current 'method' key has any 

        # Network related value. 

        if("Network.response" in network_log["method"] 

                or "Network.request" in network_log["method"] 

                or "Network.webSocket" in network_log["method"]):



            if network_log["method"] == "Network.responseReceived":

                request_id = network_log["params"]["requestId"]

                try:

                    body_data = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})

                    network_log["params"]["response"]["body"] = body_data['body']

                except Exception as e:

                    network_log["params"]["response"]["body"] = None





def export_indexeddb_localstorage_cookies(url,path):

    # Set up browsermob-proxy server

    #server = Server(r'C:\Users\kkpg2\Downloads\browsermob-proxy-2.1.4-bin\browsermob-proxy-2.1.4\bin\browsermob-proxy')

    # Path to the browsermob-proxy executable

    #server.start()

    #proxy = server.create_proxy()

    

    driver= get_selenium_driver()



    domain=url

    url="http://"+url

    delete_cookieblock_history(driver)



    driver.get('chrome://settings/clearBrowserData')

    time.sleep(5)



    driver.get(url)

    driver.execute_script(ot_script)

    driver.execute_script(tcf_intercept)

    for i in range(4):



        if i==0:



            #Requests collection

            #input(f"Download/export HAR files from network tab and name req{i}:")

            



            #Screenshot collection

            driver.save_screenshot(f'{domain}/screenshot0.png')

            

            # Data collection

            data=collect_data(driver)



    

            try:

                with open(f"{domain}/browsing_data0.json", "w") as json_file:

                    json.dump(data, json_file, indent=4)

            except:

                with open(f"{domain}/browsing_data0.txt", "w") as file:

                    file.write(str(data))

            network_capture(driver,domain,i)

        elif i==1:



            #Requests collection

            #input("Open the network tab")

            b=input("Accept on banner/if present, scroll down then enter b1/b2:")

            path.append(b)

            #input(f"Download/export HAR files from network tab and name req{i}:")

            

            driver.save_screenshot(f'{domain}/screenshot1.png')



            # Data collection

            data=collect_data(driver)



    

            try:

                with open(f"{domain}/browsing_data1.json", "w") as json_file:

                    json.dump(data, json_file, indent=4)

            except Exception as ex:

                print(ex)

                with open(f"{domain}/browsing_data1.txt", "w") as file:

                    file.write(str(data))

            network_capture(driver,domain,i)

        elif i==2:

            icon=input("Click on icon /link on footer then enter i1/i2:")

            path.append(icon)



            driver.save_screenshot(f'{domain}/screenshot2.png')



            #input("Navigate to revocation option, then open network tab")

            network_capture2(driver,domain)

            s=input("Revoke consent and based on popup(1 step) or multiple steps enter s1/s2:")

            w=input("Could withdraw or not w1/w2:")

            path.append(s)

            path.append(w)      

            

            #input(f"Download/export HAR files from network tab and name req{i}:")   

            

            # Data collection

            data=collect_data(driver)

    

            try:

                with open(f"{domain}/browsing_data2.json", "w") as json_file:

                    json.dump(data, json_file, indent=4)

            except:

                with open(f"{domain}/browsing_data2.txt", "w") as file:

                    file.write(str(data))  

            network_capture(driver,domain,i)

        elif i==3:

            

            driver.get('chrome://settings/clearBrowserData')

            time.sleep(5)

            delete_cookieblock_history(driver)

            driver.get(url)

            driver.save_screenshot(f'{domain}/screenshot3.png')

            network_capture2(driver,domain)

            #input("Open network tab")

            jt=input("Reject on banner then based on direct option enter j1/j2:")

            path.append(jt)



            #input(f"Download/export HAR files from network tab and name req{i}:")

            

            # Data collection

            data=collect_data(driver)



            try:

                with open(f"{domain}/browsing_data3.json", "w") as json_file:

                    json.dump(data, json_file, indent=4)

            except:

                with open(f"{domain}/browsing_data3.txt", "w") as file:

                    file.write(str(data))

            network_capture(driver,domain,i)

            return path





if __name__ == "__main__":

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)7s:%(message)s')

    logging.info("start")

    url = input("Enter the URL to extract data from: ")

    os.mkdir(url)



    try:

        path=[]

        path.append("r1")

        path=export_indexeddb_localstorage_cookies(url,path)



        with open(f"{url}/path.txt","w") as file:

            file.write(str(path))

    except:

        path=[]

        path.append("r2")

    logging.info("end")