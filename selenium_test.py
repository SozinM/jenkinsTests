from selenium import webdriver
import time
import jenkins
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import argparse
import sys

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 10:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class wait_for_page_load(object):
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)


class SeleniumTest:

    def __init__(self):
        self.params = {}
        self.job_name = 'xpath test'
        self.url = 'http://192.168.71.129:8080/'
        self.filePath = 'fields.txt'
        self.login = 'admin'
        self.password = '2b2db67372b84eef822f2d71c85fded7'
        self.open_browser()
        self.parse_fields()
        self.auth()
        self.chose_job()
        self.find_and_fill_values()
        self.build_project()


    def open_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def auth(self):
        self.driver.find_element_by_xpath('//*[@id="j_username"]').send_keys(self.login)
        self.driver.find_element_by_xpath('/html/body/div/div/form/div[2]/input').send_keys(self.password)

        with wait_for_page_load(self.driver):
            self.driver.find_element_by_xpath('/html/body/div/div/form/div[3]/input').click()

    def chose_job(self):
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_link_text(self.job_name).click()
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_link_text('Build with Parameters').click()#Build with Parameters

    def find_and_fill_values(self):
        '''parameters = self.driver.find_elements_by_name('parameter')
        print(self.params)

        for param in parameters:
            value = self.params.get(param.find_element_by_name('name').get_attribute("value"))
            if not value: continue
            print(value)
            self.driver.execute_script("document.evaluate("+param.find_element_by_name('value')+", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).setAttribute('value','text_to_put')")
            param.find_element_by_name('value').send_keys(value.replace('\n',''))

            time.sleep(1)
'''
        lenght = self.driver.execute_script(
                    'return document.getElementsByName("parameter").length')
        for i in range(0,lenght):
            name = self.driver.execute_script(
                    'return document.getElementsByName("parameter")[{}].firstChild.getAttribute("value");'.format(str(i)))
            value = self.params.get(name)
            if not value: continue
            print(value)
            script = 'document.getElementsByName("parameter")[{}].lastChild.setAttribute("value","{}");'.format(str(i),value.replace('\n',''))
            print(script)
            self.driver.execute_script(script)

    def build_project(self):
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_xpath('//*[@id="yui-gen1-button"]').click()

    def parse_commandline(self):
        parser = argparse.ArgumentParser()
        args, unknown = parser.parse_known_args(sys.argv[1::])
        for name in unknown:
            name = name.replace('--','').split('=')
            self.params.update({name[0]:name[1]})

    def parse_fields(self):
        file = open('fields.txt','r')
        name = file.readline()
        while(name):
            name = name.strip('\n')
            if name.startswith('[') and name.endswith(']'):
                name = name.strip('[').strip(']')
                value = file.readline()
                if not value:
                    print('File corrupted')
                self.params.update({name:value}) # find by value in braces and send data which in next line
            name = file.readline()




def main():
    test = SeleniumTest()
    time.sleep(10)

if __name__ == '__main__': main()