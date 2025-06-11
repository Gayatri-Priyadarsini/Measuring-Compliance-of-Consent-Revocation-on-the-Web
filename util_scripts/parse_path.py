import ast
import pandas as pd

def parse_path(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            da=line.strip()
        #print(da)
        return da

#with open("parse_consent.txt",'r') as file:
url_list_600 =['yahoo.com', 'spotify.com', 'msn.com', 'tumblr.com', 'nytimes.com', 'flickr.com', 'forbes.com', 'soundcloud.com', 'cnn.com', 'theguardian.com', 'bbc.co.uk', 'bbc.com', 'sourceforge.net', 'researchgate.net', 'twitch.tv', 'issuu.com', 'tinyurl.com', 'reuters.com', 'dailymail.co.uk', 'washingtonpost.com', 'slideshare.net', 'bloomberg.com', 'nature.com', 'wsj.com', 'businessinsider.com', 'springer.com', 'dailymotion.com', 'stackoverflow.com', 'quora.com', 'cnbc.com', 'dotomi.com', 'tripadvisor.com', 'weather.com', 'statista.com', 'npr.org', 'time.com', 'independent.co.uk', 'espn.com', 'usatoday.com', 'giphy.com', 'wired.com', 'scribd.com', 'cnet.com', 'speedtest.net', 'ted.com', 'webmd.com', 'cbsnews.com', 'ft.com', 'buzzfeed.com', 'aol.com', 'corriere.it', 'elmundo.es', 'francetvinfo.fr', 'fortune.com', 'asos.com', 'quizlet.com', 'wp.pl', 'apnews.com', 'marca.com', 'n-tv.de', 'onet.pl', 'adroll.com', 'screenrant.com', 'gsmarena.com', 'chess.com', 'bfmtv.com', 'caixa.gov.br', 'goal.com', 'ecosia.org', 'idnes.cz', 'sharethis.com', 'otto.de', 'vice.com', 'chegg.com', 'biomedcentral.com', 'nu.nl', 'nexusmods.com', 'marketwatch.com', 'newyorker.com', 'digicert.com', 'netflix.com', 'ui.com', 'adobe.com', 'vimeo.com', 'cloudflare.com', 'bit.ly', 'zoom.us', 'fastly.net', 'criteo.com', 'unity3d.com', 'applovin.com', 'sciencedirect.com', 'weebly.com', 'hp.com', 'linktr.ee', 'slack.com', 'go.com', 'media.net', 'cisco.com', 'booking.com', 'outbrain.com', 'grammarly.com', 'appsflyer.com', 'branch.io', 'avast.com', 'indeed.com', 'trendmicro.com', 'surveymonkey.com', 'pixabay.com', 'opendns.com', 'behance.net', 'salesforce.com', 'viber.com', 'mailchimp.com', 'intel.com', 'yelp.com', 'tandfonline.com', 'calendly.com', 'verisign.com', 'webex.com', 'nvidia.com', 'life360.com', 'pexels.com', 'deloitte.com', 'umich.edu', 'redfin.com', 'typeform.com', 'macys.com', 'costco.com', 'intercom.io', 'schwab.com', 'atlassian.com', 'force.com', 'kohls.com', 'paloaltonetworks.com', 'bitdefender.com', 'vmware.com']
url_list_1100=['brainly.in', 'azet.sk', '1mg.com', 'njuskalo.hr', 'livescore.in', 'publi24.ro', 'diretta.it']
url_list_2600=['venturebeat.com', 'slashdot.org', 'spot.im', 'hollywoodreporter.com', 'ilmessaggero.it', 'icespay.com', 'gamespot.com', 'esquire.com', 'boredpanda.com', 'thefreedictionary.com', 'bostonglobe.com', 'fifa.com', 'billboard.com', 'jpost.com', 'softonic.com', 'tamilyogi.plus', 'deadline.com', 'yumpu.com', 'lonelyplanet.com', 'patch.com', 'irishtimes.com', 'thingiverse.com', 'timeout.com', 'over-blog.com', 'wired.co.uk', 'derstandard.at', 'techrepublic.com', 'csmonitor.com', 'illinois.edu', 'mimecast.com', 'klarna.com', 'adswizz.com', 'acronis.com', 'mparticle.com', 'last.fm', 'bazaarvoice.com', 'statuspage.io', 'ask.com', 'uisp.com', 'sketchfab.com', 'thomsonreuters.com', 'kpmg.com', 'ow.ly', 'mcdonalds.com', 'nobelprize.org', 'blackberry.com']
url_list_3600=['20minutes.fr', 'elespanol.com', 'denverpost.com', 'nbcsports.com', 'elconfidencial.com', 'mediaset.it', 'ibtimes.com', 'liveabout.com', 'radiofrance.fr', 'eatingwell.com', '247sports.com', 'freep.com', 'france.tv', 'pagesix.com', 'health.com', 'gameloft.com', 'lesechos.fr', '20min.ch', 'quantcast.com', 'gazeta.pl', 'baltimoresun.com', 'kotaku.com', 'francebleu.fr', 'cadenaser.com', 'blick.ch', 'thetrainline.com', 'worldtimeserver.com', 'ilfattoquotidiano.it', 'sky.it', 'tim.it', 'spiceworks.com', 'jigsawplanet.com', 'chefkoch.de', 'amazon.se', 'manchestereveningnews.co.uk', 'lavozdegalicia.es', 'sport1.de', 'cio.com', 'loom.com', 'bigcommerce.com', 'premierleague.com', 'coca-cola.com', 'celtra.com', 'arkoselabs.com', 'binance.info', 'gmu.edu', 'oregonlive.com', 'elementor.com', 'paycomonline.net', 'sketchup.com', 'semana.com', 'postman.com', 'comodo.com', 'al.com', 'thenationalnews.com', 'swagbucks.com', 'tanium.com', 'nuance.com']
url_list_4600=['ilsole24ore.com', 'heute.at', 'newsday.com', 'windguru.cz', 'marvel.com', 'money.pl', 'springeropen.com', 'nzz.ch', 'walesonline.co.uk', 'thespruceeats.com', 'novosti.rs', 'viki.com', '15min.lt', 'bling.com.br', 'megaphone.fm', 'symbolab.com', 'gala.fr', 'purepeople.com', 'lrytas.lt', 'auchan.fr', 'klix.ba', 'orlandosentinel.com', 'record.pt', 'epicurious.com', 'chess-results.com', 'portfolio.hu', 'ml.com', 'carrefour.es', 'brightspace.com', 'grubhub.com', 'nrdc.org', 'gitlab.io', 'telemundo.com', 'mheducation.com', 'canon.com', 'boeing.com', 'dotloop.com', 'netlify.com', 'intimissimi.com', 'corel.com', 'avaaz.org', 'winzip.com', 'paylocity.com']

url_list=url_list_600+url_list_1100+url_list_2600+url_list_3600+url_list_4600

print(len(url_list))

reach=[]
banner=[]
icon=[]
manage=[]
withdraw=[]
reject=[]

for url in url_list:
    
    try:
        file_path = f"{url}/path.txt"  # Change this to the actual file path
        path=parse_path(file_path)
        p=ast.literal_eval(path)

        if p[0]=='r1':
            reach.append("True")
        
        #print(type(p))
        if p[1]=='b1':
            banner.append("Banner")
        elif p[1]=='b2':
            banner.append("No Banner")
        elif p[1] == 'b3':
            banner.append("No Option")
        else:
            print(url)    


        if p[2]=='i1':
            icon.append("Icon")
        elif p[2]=='i2':
            icon.append("Footer")
        elif p[2] == 'i3':
            icon.append("Nav/ Side bar")
        elif p[2] =='i4':
            icon.append("Persistent banner")
        else:
            print(url)    
        
        if p[3]=='s1':
            manage.append("Direct manage options")
        elif p[3]=='s2':
            manage.append("Indirect manage options")
            
        else:
            print(url)    
        
        if p[4]=='w1':
            withdraw.append("Withdrawal possible")
        elif p[4]=='w2':
            withdraw.append("Withdrawal not possible")
        else:
            print(url)    

        if p[5]=='j1':
            reject.append("Direct reject option")
        elif p[5]=='j2':
            reject.append("Indirect reject option")
        elif p[5]=='j3':
            reject.append("No Banner")
        else:
            print(url)            

    except:
            reach.append("")
            banner.append("")
            icon.append("")
            manage.append("")
            withdraw.append("")
            reject.append("")
            continue

print(len(reach))
print(len(banner))
print(len(icon))
print(len(manage))
print(len(withdraw))
print(len(reject))

df={"Website":url_list}
df2 = pd.DataFrame(df)
df2.insert(1,"Proper data collected",reach)
df2.insert(2,"Banner",banner)
df2.insert(3,"Icon?",icon)
df2.insert(4,"Manage",manage)
df2.insert(5,"Withdrawal Possible",withdraw)
df2.insert(6,"Rejection Direct",reject)
df2.to_csv('path-decoded_latest.csv')
print(df2.keys())
