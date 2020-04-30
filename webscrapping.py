from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()
    news_title, news_p = mars_news2(browser)
    data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "feature_image" : feature_imgae(browser),
        "hemispheres" : hemispheres(browser),
        "mars_weather" : mars_weather(browser),
        "mars_facts" : mars_facts()
    }
    browser.quit()
    return data
def mars_news1(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    soup = news_soup.select_one("ul.item_list li.slide")
    news_title = soup.find('div', class_='content_title').got_text()
    news_p = soup.find('div', class_='article_teaser_body').got_text()
    return news_title, news_p
def mars_news2(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
def feature_imgae(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&catergory=Mars'
    browser.visit(url)
    response1 = browser.find_by_id("full_image")
    response1.click()
    response2 = browser.find_link_by_partial_text('more info')
    response2.click()
    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')
    img = soup1.select_one("figure.lede a img").get("src")
    img_url = 'https://www.jpl.nasa.gov/'+ img
    print(img_url)
    return img_url
def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')
    results = hemisphere_soup.find_all('div', class_ = "item")
    url_list = []
    base_url = "https://astrogeology.usgs.gov/"
    for result in results:
        hemisphere_img_url = {}
        response = result.find('div', class_ = "description")
        response2 = response.find('a', class_ = "itemLink product-item")
        # su kisimdaki resmin linki yanlis geliyordu buyuk ihtimal derste yazildiysa adam yanlis yazdi suanki 68 satiri ekledim. Degisikliklere bakarak anlasilir.
        response3 = result.find('img', class_ = "thumb")
        link = response3["src"]
        title = response2.find('h3').text
        hemisphere_img_url['title'] = title
        hemisphere_img_url['img_url'] = base_url + link
        url_list.append(hemisphere_img_url)
    return url_list  
def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    browser.is_element_present_by_tag("article", wait_time=10)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    mars_weather_span = weather_soup.article.find_all('span')
    mars_weather = mars_weather_span[4].text
    return mars_weather
def mars_facts():
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns = ["mars", "info"]
    return df.to_html(index = False)
if __name__ == "__main__":
    print(scrape())