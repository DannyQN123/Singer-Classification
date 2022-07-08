import requests
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

PATH = "C:\\Users\\dungn\\OneDrive\\Máy tính\\Stuff\\Project 1 ML, SVM,  Celeb Classifier (Seed Idea)\\image_scraping\\chromedriver.exe"
wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
    def scrolldown(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url ="https://www.google.com/search?q=katy+perry&tbm=isch&ved=2ahUKEwj5lJSm6sb4AhUIxGEKHX6uCgwQ2-cCegQIABAA&oq=katy+p&gs_lcp=CgNpbWcQARgAMgQIIxAnMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgQIABBDOggIABCxAxCDAToFCAAQsQM6CAgAEIAEELEDOgsIABCABBCxAxCDAVCwCFitF2CkIWgAcAB4AIABYIgB7QSSAQE3mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=hBG2YvnCAoiIhwP-3Kpg&bih=641&biw=790&hl=en"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scrolldown(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME,"Q4LuWd")

        for img in thumbnails[len(image_urls)+skips : max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "KAlRDb")

            for image in images:
                if image.get_attribute("src") in image_urls:
                    max_images +=1
                    skips +=1
                    break

                if image.get_attribute("src") and "http" in image.get_attribute("src"):
                    image_urls.add(image.get_attribute("src"))
                    print(f"Image {len(image_urls)}")


    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("success")
    except Exception as e:
        print("failed - ", e)

urls = get_images_from_google(wd, 2, 110)

for i, url in enumerate(urls):
    download_image("image_dataset/katy_perry/", url, str(i) + ".jpg")

wd.quit()







