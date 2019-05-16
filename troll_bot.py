from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# YouTube account info
username = '-- Your YouTube username --'
password = '-- Your YouTube password --'

# information for search and comment
search_term = '-- Your search term --'
comment = '-- Your comment --'
# variables
video_count = 100
driver_path = '-- Your local chromedriver path --'
activate = True

# ------------------------------------------------------------------------------
# open driver
driver = webdriver.Chrome(driver_path)
# maximize window
driver.maximize_window()
# go to YouTube
driver.get('https://www.youtube.com')

# locate sign in button
sign_in = driver.find_element_by_link_text('SIGN IN')
sign_in.click()
# enter username
# username_field = driver.find_element_by_name('identifier')
username_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.NAME, 'identifier'))
)
username_field.send_keys(username + '\n')
# enter password
password_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_field.send_keys(password + '\n')

# enter search term
search_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, 'search'))
)
search_field.send_keys(search_term + '\n')

# ------------------------------------------------------------------------------
# expand page until required count of thumbnails are extracted
time.sleep(1)
videos = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-video-renderer'))
)
while (len(videos) < video_count):
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(1)
    videos = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-video-renderer'))
    )

# extract hyperlinks from videos
links = list()
for video in videos:
    thumbnail = video.find_element_by_id('thumbnail')
    links.append(thumbnail.get_attribute('href'))
# slice links list
links = links[:video_count]

# ------------------------------------------------------------------------------
# visit each link in list
for link in links:
    driver.get(link)
    # scroll down to comment
    time.sleep(1)
    try:
        driver.execute_script("window.scrollTo(0, 1000);")
        # locate comment element and click
        comment_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'ytd-comment-simplebox-renderer'))
        )
        comment_element.click()
        # locate comment field and enter comment
        comment_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'contenteditable-root'))
        )
        comment_field.send_keys(comment)
        # locate submit button and click
        submit_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'submit-button'))
        )
        if (activate):
            submit_button.click()
    except:
        continue

# close program
time.sleep(3)
driver.close()
time.sleep(3)
