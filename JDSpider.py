import requests
import json
import threading
import time

def printUI():
    print(" "*20,"*"*50)
    print(" "*20,"*"," "*15,"欢迎来到京东抢券软件","          *")
    print(" "*20,"*"," "*38,"作者:HN","*")
    print(" "*20,"*"," "*46,"*")
    print(" "*20,"*"*50)

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.    3497.100 Mobile Safari/537.36"}

class JDSpider(object):
    def __init__(self,account_filename,ticket_filename):
        self.account_filename = account_filename
        self.ticket_filename = ticket_filename
        self.act_url = "https://act-jshop.jd.com/couponSend.html?"
        self.wap_url = None
        self.api_url = None
        self.ticket_name = None
        self.ticket_key = None
        self.ticket_id = None
        self.ticket_starttime = None
        self.ticket_sub_cnt = None
        self.ticket_sub_interval = None
        self.ZH_list = list()


    
    def read_ZH_list(self):
        with open(self.account_filename,"r") as f:
            account_info_str = f.read()
        acc_list = account_info_str.split("\n")
        acc_list.pop()      #去除最后一个
        for i in acc_list:
           tmp_list = i.split("|") 
           acc_dict = {"zh":tmp_list[0],"cookies":tmp_list[2]}
           self.ZH_list.append(acc_dict)

    def read_ticket_info(self):
        with open(self.ticket_filename,"r") as f:
            json_str = f.read()
        json_dict = json.loads(json_str)
        self.ticket_name = json_dict["name"]
        self.ticket_ket = json_dict["key"]
        self.ticket_id = json_dict["id"]
        self.ticket_starttime = json_dict["starttime"]
        self.ticket_sub_cnt = json_dict["submitcnt"]
        self.ticket_sub_interval = json_dict["submitinterval"]


    def parse_act(self,zh_name,cookies):
        act_headers = headers
        act_headers["Referer"] = "https://sale.jd.com/mall/wuCablg37JKMB.html?cpdad=1DLSUE"
        act_headers["Cookie"] = cookies
        act_params = {"callback":"jQuery802602",\
                "ruleId" :self.ticket_id,\
                "key":self.ticket_key,\
                "eid":"QE6JL65DIYMEY5YEA3BMGBN5KAUQXSUZI5ELJY3ALNMSLQSG2BJWV5KXCDHC4DPRTOMKDYXLSKJ3BTFR4H7HTMATAE",\
                "fp":"7a53ac82c4abc0069e522c13c7858e04",\
                "shshshfp":"58e6db9303138c19e01cc237dcb9ab3a",\
                "shshshfpa":"7c1add7b-68ed-a499-90a5-a3597e34355f-1527418980",\
                "shshshfpb":"084ae278678622b3156ac27c8e0494b97b557b6e4defa4bd35b0a7f1b3",\
                "jda":"122270672.1527418980635952293435.1527418980.1531235618.1539493072.27",\
                "pageClickKey":-1,\
                "platform":0,\
                "venderId":1000001132,\
                "projectId":1110696,\
                "_":1539493809111
                }   
        response = requests.get(self.act_url,headers=act_headers,params=act_params)
        #print(response)
        #print(response.content.decode("utf-8"))

        

    def parse_wap(self,zh_name,cookies):
        pass

    def parse_api(self,zh_name,cookies):
        pass

    def run(self):
        self.read_ZH_list()
        self.read_ticket_info()
        print("准备抢券:%s"%self.ticket_name)
        for i in self.ZH_list:
            accID = i["zh"]
            cookies = i["cookies"]
            t_act = threading.Thread(target=self.parse_act,args=(accID,cookies,))    
            t_wap = threading.Thread(target=self.parse_wap,args=(accID,cookies,))
            t_api = threading.Thread(target=self.parse_api,args=(accID,cookies,))
            t_act.start()
            t_wap.start()
            t_api.start()



if __name__ == "__main__":
    printUI()
    spider = JDSpider("Account.txt","Ticket.json")
    spider.run()
