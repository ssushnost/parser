from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def init_headless_browser():
    """init browser"""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    return browser


def get_links(school_number, browser=None):
    """get all links related to a school number from google search"""
    browser_not_passed = False
    if not browser:
        browser_not_passed = True
        browser = init_headless_browser()
    url = f"https://www.google.com/search?q=Школа+{school_number}+о+нас"
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    search = soup.find("div", {"id": "search"})
    if search is None:
        print("error in get_links func. search div does not exist")
        if browser_not_passed:
            browser.quit()
        return []
    links = search.find_all("a")
    proper_links = []
    for link in links:
        href = link.get("href")
        if not href:
            continue
        if not href.startswith("https"):
            continue
        if href not in proper_links:
            proper_links.append(href)
    if browser_not_passed:
        browser.quit()
    return proper_links