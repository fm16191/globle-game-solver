#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from random import choice
from time import sleep
import json

from distance import distances


def choose_random_country():
    fo = open("country_data.json")
    data = json.load(fo)
    fo.close()
    country_names = [cdata["properties"]["ABBREV"] for cdata in data["features"]]
    return choice(country_names)


def try_country(driver, target_country):
    box_xpath = '//input[@name="guess" and @placeholder="Enter country name here"]'
    box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, box_xpath)))
    if not box.is_displayed() or not box.is_enabled():
        return False
    box.clear()
    box.click()

    actions = ActionChains(driver)
    for l in target_country:
        actions.send_keys(l)

    actions.send_keys(Keys.ENTER)
    actions.perform()
    return True


def check_end(driver):
    sleep(0.5)
    end_xpath = '//h2[text()="Statistics"]'
    end = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, end_xpath)))
    return True if end else False


def process():
    f_options = FirefoxOptions()

    driver = webdriver.Firefox(options=f_options)
    # driver.maximize_window()

    driver.get("https://globle-game.com/")

    cookies_xpath = '//button/span[text()="AGREE"]'
    cookies = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, cookies_xpath)))
    cookies.click()

    play_button_xpath = '//div/b[text()="Click the globe to play!"]'
    play_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, play_button_xpath)))
    play_button.click()

    tested = []

    target_country = choose_random_country()

    print(f"Test [{len(tested):3d}] {target_country}")
    if not try_country(driver, target_country):
        print("Box cannot be interacted with")
        exit()
    tested.append(target_country)

    old_closest_text = None

    closest_xpath = '//ul[@data-cy="countries-list"]/li/button/span'
    closest_border_xpath = '//p/span[contains(text(),"Closest border")]/..'

    while True:
        closest = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, closest_xpath)))
        closest_text = closest.get_attribute("textContent")

        closest_border = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, closest_border_xpath)))
        target_distance = closest_border.get_attribute("outerHTML").split("</span>:")[-1][:-4].strip().replace(',', '')

        if old_closest_text != closest_text:
            print(f"Get distances to {closest_text} {target_distance}")
            results = distances(closest_text, float(target_distance))
        old_closest_text = closest_text

        # except exceptions.InvalidElementStateException:

        # for cname, d in results[::-1]:
        for cname, d in results:
            if cname in tested: continue
            print(f"Test [{len(tested):3d}] {cname}")
            if not try_country(driver, cname) and check_end(driver):
                print(f"WP ! Found country : {tested[-1]}\nTries : {len(tested)}")
                exit()
            tested.append(cname)
            break

    # print("[Press enter to quit]", end="\r")
    # input()
    # driver.quit()


if __name__ == "__main__":
    process()
