import ast
import pandas as pd

def parse_path(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            da=line.strip()
        #print(da)
        return da

df2 = pd.read_csv('../List_of_websites/top_200.csv') #For RQ1 and RQ2
# df2 = pd.read_csv('List_of_websites/top_201_5k.csv') For RQ3 and RQ4


print(df2.keys())
url_list=df2["Websites"]

reach=[]
banner=[]
icon=[]
manage=[]
withdraw=[]
reject=[]

for url in url_list:
    
    try:
        file_path = f"/home/usenix/Desktop/dataset_1_2/rev/{url}/path.txt"  # Change this to the actual file path
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

    except Exception as e:
            print(e)
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
