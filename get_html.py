from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
driver = webdriver.Chrome()
url = 'https://dulichviet.com.vn/du-lich-trong-nuoc'
driver.get(url)
pages = 208
try:
    for page in range(pages):
        print("In page ", page)
        # Find the element you want to click using a selector (you may need to adjust the selector)
        button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/form/div/div[2]/div[4]/span")
        # clicking on the button
        button.click()
        time.sleep(3)
    html_content = driver.page_source
    file_path = 'html.txt'
    # Write the HTML content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
except Exception as e:
    print(f"An error occurred: {e}")
# driver.quit()