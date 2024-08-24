"""
Scrape NYT connections data to train our classifier
"""
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def run():
    try:
        # the superior browser
        driver = webdriver.Firefox()
        URL = "https://tryhardguides.com/nyt-connections-answers/"
        driver.get(URL)
        li_elements_with_strong = driver.find_elements(By.XPATH, '//li[strong]')

        data = []
        for li in li_elements_with_strong:
            element_text = li.text
            try:
                category, words = element_text.split(" - ")
                words = words.split(",")
                words_map = map(lambda word: word.strip(), words)
                words = list(words_map)
                data.append({"category": category, "words": words})
            except ValueError:
                print(f"Skipping {li.text}")
        
        with open("data/answers.json", 'w') as f:
            json.dump(data, f, indent=4)
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    run()
