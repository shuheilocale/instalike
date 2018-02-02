import os
import json
import codecs
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys


"""ドライバ生成"""
def create_driver():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.implicitly_wait(10)
    return driver


class Instagram:
    def __init__(self, driver):
        self.driver = driver

    def login(self, id, pswd):
        url = "https://www.instagram.com/accounts/login/?hl=ja"
        self.driver.get(url)

        input = self.driver.find_elements_by_css_selector("._ph6vk._jdqpn._o716c")
        input[0].send_keys(id)
        input[1].send_keys(pswd)
        input[1].send_keys(keys.ENTER)
        time.sleep(5)

    def search(self, word):
        url = "https://www.instagram.com/explore/tags/{}/?hl=ja".format(word)
        self.driver.get(url)
        time.sleep(2)

   
    def sequencial_like(self, repeat):
        # まず最初の投稿にアクセスする
        post = self.driver.find_elements_by_css_selector("._si7dy")[0]
        post.click()
        time.sleep(2)

        for i in range(repeat):

            # いいねクリック
            heart = self.driver.find_elements_by_css_selector("._8scx2.coreSpriteHeartOpen")
            if len(heart):
                heart[0].click()
                time.sleep(1) 
                
            # 次へ
            next_arrow = self.driver.find_elements_by_css_selector("._3a693.coreSpriteRightPaginationArrow")[0]
            next_arrow.click()
            time.sleep(1) 

def load_param(path):
    f = codecs.open(path,"r","utf-8")
    param = json.load(f)
    f.close()
    return param


def main():
    psr = argparse.ArgumentParser()
    psr.add_argument("-c", "--config", default="")
    psr.add_argument("-u", "--user", default="")
    psr.add_argument("-p", "--pswd", default="")
    psr.add_argument("-w", "--word", default="")
    psr.add_argument("-r", "--repeat", default=100)
    args = psr.parse_args()

    if args.config is not "":
        conf = load_param(args.config)
    elif args.user is not "" and args.pswd is not "" and args.word is not "":
        conf["user"] = args.user
        conf["pswd"] = args.pswd
        conf["word"] = args.word
        conf["repeat"] = args.repeat
    else:
        print("invalid parameters.")
        return

    driver = create_driver()

    insta = Instagram(driver)
    insta.login(conf["user"], conf["pswd"])
    insta.search(conf["word"])
    insta.sequencial_like(conf["repeat"])

    driver.close()


if __name__ == '__main__': main()
