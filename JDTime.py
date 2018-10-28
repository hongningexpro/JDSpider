import requests
import json
import time
import threading

class JDTime(object):
    def __init__(self):
        self.__JDServerTime = 0
        self.__url = "http://api.m.jd.com/client.action?functionId=version&clientVersion=5.6.0&build=40742&client=android&d_brand=360&d_model=1503-A01&osVersion=6.0&screen=1920*1080&partner=jingdong&uuid=861483036220693-74ac5f86164b&area=15_1158_1224_46486&networkType=wifi&st=1483168743663&sign=5234c3fb4702d356810129f660206881&sv=102&body=%7B%22osVersion%22%3A23%2C%22platform%22%3A100%2C%22buildId%22%3A%2240742%22%2C%22wlanSwitch%22%3A%221%22%7D&"

    @property
    def Time(self):
        return self.__JDServerTime

    def parseJDServerTime(self):
        response = requests.get(self.__url) 
        if response:
            json_dict = json.loads(response.content.decode("utf-8"))
            self.__JDServerTime = json_dict["curTimestamp"]

    def run(self):
        while True: 
            self.parseJDServerTime()
            #print(self.__JDServerTime)



if __name__ == "__main__":
    j = JDTime()
    t = threading.Thread(target=j.run)
    t.start()
    while True:
        t = time.time()
        print("JDServerTime:%d"%j.Time)
        print(int(round(t*1000)))
        time.sleep(0.1)
