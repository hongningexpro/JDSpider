from selenium import webdriver
import time

url = "https://passport.jd.com/uc/login?ltype=logout"
driver = webdriver.Firefox()

def get_cookies():
    driver.get(url)
    driver.find_element_by_link_text("账户登录").click()
    driver.find_element_by_id("loginname").send_keys("***********")
    driver.find_element_by_id("nloginpwd").send_keys("************")
    driver.find_element_by_id("loginsubmit").click()
    time.sleep(5)
    cookies = driver.get_cookies()
    print(cookies)
    return cookies

if __name__ == "__main__":
    get_cookies()
