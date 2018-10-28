import time
import datetime

class JDLog(object):
    def record_result(self,name):
        time_head = "[%s]:\n"%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_content = time_head + name + ":抢券成功!\n"
        with open("result_log.txt","a") as f:
            f.write(log_content)


    def record_response(self,response):
        time_head = "[%s]:\n"%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_content = time_head + response + "\n"
        with open("response_log.txt","a") as f:
            f.write(log_content)


if __name__ == "__main__":
    pass
