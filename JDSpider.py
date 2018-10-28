import requests
import json
import threading
import datetime
import time
import JDTime
import JDLog
from multiprocessing import Pool
import YDMHttp

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
        self.wap_url = "https://s.m.jd.com/activemcenter/mfreecoupon/getcoupon?"
        self.api_url = "https://api.m.jd.com/client.action?"
        self.ticket_name = None
        self.ticket_key = None
        self.ticket_id = None
        self.ticket_starttime = None
        self.ticket_sub_cnt = None
        self.ticket_sub_interval = None
        self.ZH_list = list()
        self.event = threading.Event()
        self.verity_event = threading.Event()
        self.act_event = threading.Event()
        self.wap_event = threading.Event()
        self.api_event = threading.Event()
        self.log = JDLog.JDLog()
        self.po = Pool(1)
        self.YDM = YDMHttp.YDMHttp()

    
    def read_ZH_list(self):
        with open(self.account_filename,"r") as f:
            account_info_str = f.read()
        acc_list = account_info_str.split("\n")
        acc_list.pop()      #去除最后一个
        for i in acc_list:
           tmp_list = i.split("----") 
           acc_dict = {"zh":tmp_list[0],"cookies":tmp_list[2]}
           self.ZH_list.append(acc_dict)

    def read_ticket_info(self):
        with open(self.ticket_filename,"r") as f:
            json_str = f.read()
        json_dict = json.loads(json_str)
        self.ticket_name = json_dict["name"]
        self.ticket_key = json_dict["key"]
        self.ticket_id = json_dict["id"]
        self.ticket_sub_cnt = json_dict["submitcnt"]
        self.ticket_sub_interval = json_dict["submitinterval"]
        #解析抢券时间，精确到毫秒
        timestr = json_dict["starttime"]
        time_list = timestr.split(".")
        GMT_Time = datetime.datetime.strptime(time_list[0],"%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=-15)
        self.ticket_starttime = int(str(int(time.mktime(time.strptime(GMT_Time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))) + time_list[1])
        #self.ticket_starttime = int(str(int(time.mktime(time.strptime(time_list[0], "%Y-%m-%d %H:%M:%S")))) + time_list[1])
        #self.ticket_starttime = time.mktime(time.strptime(time_list[0], "%Y-%m-%d %H:%M:%S"))

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
        req_cnt = int(self.ticket_sub_cnt)
        req_interval = int(self.ticket_sub_interval)
        self.event.wait()
        while req_cnt:
            try:
                response = requests.get(self.act_url,headers=act_headers,params=act_params)
                response_str = response.content.decode("utf-8")
                self.po.apply_async(self.log.record_response,(response_str,))
                if "成功" in response_str:
                    self.po.apply_async(self.log.record_result,(zh_name,))
                    break
            except Exception:
                break
            time.sleep(req_interval/1000)
            req_cnt -=1

        self.act_event.set()


    def parse_wap(self,zh_name,cookies):
        wap_headers = headers
        wap_headers["Referer"] = "http://coupon.m.jd.com/coupons/show.action?key=%s&roleId=%s&to=m.jd.com"%(self.ticket_key,self.ticket_id)
        wap_headers["Cookie"] = cookies
        wap_params = {\
                "key":self.ticket_key,\
                "roleId":self.ticket_id,\
                "to":"m.jd.com",\
                "verifycode":"",\
                "verifysession":"",\
                "_":1540655168117,\
                "sceneval":2,\
                "g_login_type":1,\
                "callback":"jsonpCBKF",\
                "g_ty":"ls"\
                    }
        req_cnt = int(self.ticket_sub_cnt)
        req_interval = int(self.ticket_sub_interval)
        self.verity_event.wait()
        while req_cnt:
            try:
                response = requests.get(self.wap_url,headers=wap_headers,params=wap_params)
                response_str = response.content.decode("utf-8")
                """
                解析验证码
                """
                json_str = response_str[15:-14]
                json_dict = json.loads(json_str)
                if json_dict["rvc"]["rvc_content"]:
                    verity_url = "http:" + json_dict["rvc"]["rvc_content"]
                    verity_response = requests.get(url=verity_url,headers=headers)
                    cid,result = self.YDM.decode(verity_response.content,1004,60)
                """
                验证码处理结束
                """
                wap_params["verifysession"] = json_dict["rvc"]["rvc_uuid"]
                wap_params["verifycode"] = result
                self.event.wait()
                response = requests.get(self.wap_url,headers=wap_headers,params=wap_params)
                response_str = response.content.decode("utf-8")

                self.po.apply_async(self.log.record_response,(response_str,))
                if "\"errmsg\":\"\"" in response_str:
                    self.po.apply_async(self.log.record_result,(zh_name,))
                    break
            except Exception:
                break
            time.sleep(req_interval/1000)
            req_cnt -=1

        self.wap_event.set()

    def parse_api(self,zh_name,cookies):
        api_headers = headers
        api_headers["Cookie"] = cookies
        params_str = "functionId=newBabelAwardCollection&body={\"activityId\":\"2KYi8tMN4hP8pUs5qCDqQDWz7nzk\",\"from\":\"H5node\",\"scene\":\"1\",\"args\":\"key=%s,roleId=%s\",\"mitemAddrId\":\"\",\"geo\":{\"lng\":\"\",\"lat\":\"\"}}&client=wh5&clientVersion=1.0.0"%(self.ticket_key,self.ticket_id)
        self.api_url +=params_str
        req_cnt = int(self.ticket_sub_cnt)
        req_interval = int(self.ticket_sub_interval)
        self.event.wait()
        while req_cnt:
            try:
                response = requests.get(self.api_url,headers=api_headers)
                response_str = response.content.decode("utf-8")
                self.po.apply_async(self.log.record_response,(response_str,))
                if "成功" in response_str:
                    self.po.apply_async(self.log.record_result,(zh_name,))
                    break
            except Exception:
                break
            time.sleep(req_interval/1000)
            req_cnt -=1

        self.api_event.set()

    def check_time_thread(self):
        """
        单独线程用以校对京东时间
        """
        jdt = JDTime.JDTime()
        t = threading.Thread(target=jdt.run)
        t.start()
        verity_flag = True
        while True:
            if self.ticket_starttime <= jdt.Time + 4000:
                #通知抢券线程开始抢券
                print("抢券开始。。。")
                self.event.set()
                break
            elif self.ticket_starttime <= jdt.Time+30000 and verity_flag:
                #通知wap开始打码
                verity_flag = False
                print("打码开始。。。")
                self.verity_event.set()

    def kill_pool(self):
        self.act_event.wait()
        self.wap_event.wait()
        self.api_event.wait()
        self.po.close()
        self.po.join()
        print("抢券结束。。。")

    def run(self):
        self.read_ZH_list()
        self.read_ticket_info()
        killpool_t = threading.Thread(target=self.kill_pool)        #单独线程用以回收进程池资源
        killpool_t.start()
        t = threading.Thread(target=self.check_time_thread)
        t.start()
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
