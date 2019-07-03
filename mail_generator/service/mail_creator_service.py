import os
import random
import names
import time

import pandas as pd

import mail_generator

from pynput.keyboard import Controller, Key
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


class MailCreator:

    chrome_driver_path = os.path.join(os.path.dirname(mail_generator.__file__), 'configs/chromedriver')

    url = 'https://account.mail.ru/signup?from=main&rf=auth.mail.ru'
    # Setup
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    def __init__(self):
        self.driver.get(self.url)
        time.sleep(1)
        self.keyboard = Controller()

    def perform_space(self):
        self.keyboard.press(Key.space)
        time.sleep(0.1)
        self.keyboard.release(Key.space)
        time.sleep(0.5)

    def perform_tab(self):
        self.keyboard.press(Key.tab)
        time.sleep(0.1)
        self.keyboard.release(Key.tab)
        time.sleep(0.5)

    def perform_enter(self):
        self.keyboard.press(Key.enter)
        time.sleep(0.1)
        self.keyboard.release(Key.enter)
        time.sleep(0.5)

    def perform_right_arrow(self):
        self.keyboard.press(Key.right)
        time.sleep(0.1)
        self.keyboard.release(Key.right)
        time.sleep(0.5)

    def type_word(self, word):
        """ Handle pop up by simulating key presses
        :return:
        """
        for char in word:
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(0.05)
        self.keyboard.press(Key.tab)
        time.sleep(0.1)
        self.keyboard.release(Key.tab)
        time.sleep(0.5)

    def wait_and_find_by_xpath(self, xpath: str, sec=17):
        """Try to find selenium element by given xpath for 15sec, if fail to find raise Timeout Exception
        :param xpath: specific string of selenium.webdriver.remote.webelement.WebElement element
        :param sec: seconds to wait
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        return WebDriverWait(self.driver, sec).until(ec.visibility_of_element_located((By.XPATH, xpath)))

    def create_account(self, person):
        self.type_word(person['name'])
        self.type_word(person['surname'])
        self.type_word(person['day'])
        self.type_word(person['month'])
        self.type_word(person['year'])
        if person['gender'] == 'female':
            self.perform_right_arrow()
        else:
            self.perform_space()
        self.perform_tab()
        self.type_word(person['email'])
        self.perform_tab()
        self.type_word(person['password'])
        self.type_word(person['password'])
        self.perform_tab()
        self.perform_tab()
        self.perform_enter()
        self.driver.find_element_by_xpath('//span[@class="btn__text"]').click()
        # self.wait_and_find_by_xpath('//i[@class="x-ph__menu__button__text x-ph__menu__button__text_auth"]', sec=25)
        time.sleep(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def generate_person() -> dict:
    person = dict()
    person['gender'] = random.choice(('male', 'female'))
    person['name'] = names.get_first_name(person['gender'])
    person['surname'] = names.get_last_name()
    person['email'] = f"{person['name']}-{person['surname']}-2019-gen"
    person['password'] = f"{person['name'][:2]}{person['surname'][:2]}2019gen"
    person['day'] = str(random.randint(1, 27))
    person['month'] = str(random.randint(1, 12))
    person['year'] = str(random.randint(1930, 1995))
    return person


if __name__ == '__main__':
    df = pd.DataFrame()
    for i in range(5):
        person = generate_person()
        print(person)
        MailCreator().create_account(person=person)
        df = df.append(pd.Series(person), ignore_index=True)

    df.to_excel('/home/vahagn/Dropbox/dev/generated_persons_data.xlsx', sheet_name='bench1', index=False)
