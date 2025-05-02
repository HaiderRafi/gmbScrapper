# extracting- photos, rating 
# test- working, just work on image url, phone number, map url


# import os
# import stat
# import json
# import requests
# import wget
# import zipfile36 as zipfile
# from urllib.parse import urlparse, parse_qs
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Step 1: Expand GMB short link
# def expand_gmb_link_and_get_kgmid_url(short_link):
#     try:
#         response = requests.get(short_link, allow_redirects=True)
#         expanded_url = response.url
#         print(f"Expanded URL: {expanded_url}")
#         parsed_url = urlparse(expanded_url)
#         query_params = parse_qs(parsed_url.query)

#         if 'kgmid' in query_params:
#             kgmid = query_params['kgmid'][0]
#             clean_url = f"https://www.google.com/search?kgmid={kgmid}"
#             print(f"Clean KG URL: {clean_url}")
#             return clean_url
#         else:
#             print("No 'kgmid' found.")
#             return None
#     except Exception as e:
#         print(f"Error expanding GMB link: {e}")
#         return None

# # Step 2: Download and setup ChromeDriver
# def download_and_extract_chromedriver():
#     try:
#         download_url = "https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.95/win64/chromedriver-win64.zip"
#         zip_path = wget.download(download_url, 'chromedriver.zip')
#         extracted_dir = os.getcwd()

#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(extracted_dir)
#             extracted_path = os.path.join(extracted_dir, 'chromedriver-win64', 'chromedriver.exe')
#             os.chmod(extracted_path, os.stat(extracted_path).st_mode | stat.S_IEXEC)

#         os.remove(zip_path)
#         return extracted_path
#     except Exception as e:
#         print(f"Error downloading ChromeDriver: {e}")
#         return None

# # Step 3: Stealth Chrome setup
# def initialize_driver():
#     driver_path = download_and_extract_chromedriver()
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

#     service = ChromeService(executable_path=driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
#     })

#     return driver

# # Step 4: Scrape data from the kgmid-based URL
# def extract_google_details(kgmid_url):
#     driver = initialize_driver()
#     try:
#         driver.get(kgmid_url)
#         wait = WebDriverWait(driver, 10)

#         # Name
#         name = "Not found"
#         try:
#             name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-attrid='title']"))).text
#         except:
#             pass


#         # Address
#         address = "Not found"
#         try:
#             address = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.LrzXr"))).text
#         except:
#             pass

#            # Phone Number
#         phone = "Not found"
#         try:
#             phone = wait.until(EC.presence_of_element_located(
#                 (By.XPATH, "//span[@class='LrzXr zdqRlf kno-fv']//span[contains(@aria-label, 'Call phone number')]")
#             )).text
#         except:
#             pass

#         # Open status
#         open_status = "Not found"
#         try:
#             open_status = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.TLou0b"))).text
#         except:
#             pass

#         # Price
#         price_info = "Not found"
#         try:
#             price_info = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Price per person:')]/following-sibling::span"))).text
#         except:
#             pass

#         # Rating
#         rating = "Not found"
#         try:
#             rating = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.Aq14fc"))).text
#         except:
#             pass

#         # About (after clicking "More")
#         about = "Not found"
#         try:
#             more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Show more']")))
#             driver.execute_script("arguments[0].click();", more_button)
#             about_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jscontroller='QBLtbf']")))
#             about = about_element.get_attribute("data-long-text") or about_element.text
#         except Exception as e:
#             print("About section not found or not expandable:", e)

#         # Click "See photos"
#         try:
#             see_photos = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'See photos')]")))
#             driver.execute_script("arguments[0].click();", see_photos)
#         except Exception as e:
#             print("See photos not clickable:", e)

#         # Wait for image carousel and extract image URLs

#         image_urls = []
#         try:
#             wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='FCeiOe']")))
#             images = driver.find_elements(By.CSS_SELECTOR, "div[jsname='FCeiOe'] img")
#             image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src") and "googleusercontent" in img.get_attribute("src")]
#         except:
#             pass

#         # Close the photo modal before clicking Directions
#         try:
#             close_modal_button = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//span[contains(@class, 'jA3abb') and @aria-hidden='true']")))
#             driver.execute_script("arguments[0].click();", close_modal_button)
#             print("Photo modal closed.")
#         except Exception as e:
#             print("Could not close photo modal (may not be open):", e)

#         #  Google Maps URL (from Directions)

#         maps_url = "Not found"
#         try:
#             current_url = driver.current_url

#             directions_button = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//span[text()='Directions']/ancestor::div[@role='link']")))
#             driver.execute_script("arguments[0].click();", directions_button)

#             WebDriverWait(driver, 10).until(EC.url_changes(current_url))

#             if "google.com/maps" in driver.current_url:
#                 maps_url = driver.current_url
#             else:
#                 maps_url = "Redirected but not to maps"
#         except Exception as e:
#             print("Maps URL error:", e)


#         # Output result
#         result = {
#             "business_name":name,
#             "address": address,
#             "phone_number":phone,
#             "opening_hours": open_status,
#             "price_per_person": price_info,
#             "rating": rating,
#             "about":about,
#             "image_urls": image_urls,
#             "map_ulr":maps_url,
#         }

#         print(json.dumps(result, indent=2, ensure_ascii=False))
#         return result

#     except Exception as e:
#         print(f"Error extracting details: {e}")
#         return None
#     finally:
#         driver.quit()

# # === Entry Point ===
# if __name__ == "__main__":
#     short_gmb_link = "https://g.co/kgs/FzNbcTp"  # Replace with actual short GMB link
#     kgmid_url = expand_gmb_link_and_get_kgmid_url(short_gmb_link)

#     if kgmid_url:
#         extract_google_details(kgmid_url)

















# ----------------------------------------------------------------


# trying headless

import os
import stat
import json
import requests
import wget
import zipfile36 as zipfile
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Expand GMB short link
def expand_gmb_link_and_get_kgmid_url(short_link):
    try:
        response = requests.get(short_link, allow_redirects=True)
        expanded_url = response.url
        print(f"Expanded URL: {expanded_url}")
        parsed_url = urlparse(expanded_url)
        query_params = parse_qs(parsed_url.query)

        if 'kgmid' in query_params:
            kgmid = query_params['kgmid'][0]
            clean_url = f"https://www.google.com/search?kgmid={kgmid}"
            print(f"Clean KG URL: {clean_url}")
            return clean_url
        else:
            print("No 'kgmid' found.")
            return None
    except Exception as e:
        print(f"Error expanding GMB link: {e}")
        return None

# Step 2: Download and setup ChromeDriver
def download_and_extract_chromedriver():
    try:
        download_url = "https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.95/win64/chromedriver-win64.zip"
        zip_path = wget.download(download_url, 'chromedriver.zip')
        extracted_dir = os.getcwd()

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
            extracted_path = os.path.join(extracted_dir, 'chromedriver-win64', 'chromedriver.exe')
            os.chmod(extracted_path, os.stat(extracted_path).st_mode | stat.S_IEXEC)

        os.remove(zip_path)
        return extracted_path
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return None

# Step 3: Stealth Chrome setup
def initialize_driver():
    driver_path = download_and_extract_chromedriver()
    chrome_options = Options()
    
    # Essential headless config
    chrome_options.add_argument("--headless=new")  # New headless mode
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # Anti-detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Performance
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Stealth scripts
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]})
        """
    })
    
    return driver

# Replace ChromeDriver download with system Chromium// uncomment when deploy on server and comment above one
# def initialize_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.binary_location = "/usr/bin/chromium-browser"  # Path to Chromium
#     return webdriver.Chrome(options=chrome_options)


# Step 4: Scrape data from the kgmid-based URL
def extract_google_details(kgmid_url):
    driver = initialize_driver()
    try:
        driver.get(kgmid_url)
        driver.save_screenshot("debug_screen.png")
        wait = WebDriverWait(driver, 20)

        # Name
        name = "Not found"
        try:
            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-attrid='title']"))).text
        except:
            pass


        # Address
        address = "Not found"
        try:
            address = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.LrzXr"))).text
        except:
            pass

           # Phone Number
        phone = "Not found"
        try:
            phone = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[@class='LrzXr zdqRlf kno-fv']//span[contains(@aria-label, 'Call phone number')]")
            )).text
        except:
            pass

        # Open status
        open_status = "Not found"
        try:
            open_status = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.TLou0b"))).text
        except:
            pass

        # Price
        price_info = "Not found"
        try:
            price_info = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Price per person:')]/following-sibling::span"))).text
        except:
            pass

        # Rating
        rating = "Not found"
        try:
            rating = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.Aq14fc"))).text
        except:
            pass

        # About (after clicking "More")
        about = "Not found"
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Show more']")))
            driver.execute_script("arguments[0].click();", more_button)
            about_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jscontroller='QBLtbf']")))
            about = about_element.get_attribute("data-long-text") or about_element.text
        except Exception as e:
            print("About section not found or not expandable:", e)

        # Click "See photos"
        try:
            see_photos = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'See photos')]")))
            driver.execute_script("arguments[0].click();", see_photos)
        except Exception as e:
            print("See photos not clickable:", e)

        # Wait for image carousel and extract image URLs

        image_urls = []
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='FCeiOe']")))
            images = driver.find_elements(By.CSS_SELECTOR, "div[jsname='FCeiOe'] img")
            image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src") and "googleusercontent" in img.get_attribute("src")]
        except:
            pass

        # Close the photo modal before clicking Directions
        try:
            close_modal_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'jA3abb') and @aria-hidden='true']")))
            driver.execute_script("arguments[0].click();", close_modal_button)
            print("Photo modal closed.")
        except Exception as e:
            print("Could not close photo modal (may not be open):", e)

        #  Google Maps URL (from Directions)

        maps_url = "Not found"
        try:
            current_url = driver.current_url

            directions_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Directions']/ancestor::div[@role='link']")))
            driver.execute_script("arguments[0].click();", directions_button)

            WebDriverWait(driver, 10).until(EC.url_changes(current_url))

            if "google.com/maps" in driver.current_url:
                maps_url = driver.current_url
            else:
                maps_url = "Redirected but not to maps"
        except Exception as e:
            print("Maps URL error:", e)


        # Output result
        result = {
            "business_name":name,
            "address": address,
            "phone_number":phone,
            "opening_hours": open_status,
            "price_per_person": price_info,
            "rating": rating,
            "about":about,
            "image_urls": image_urls,
            "map_ulr":maps_url,
        }

        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

    except Exception as e:
        print(f"Error extracting details: {e}")
        return None
    finally:
        driver.quit()

# === Entry Point ===
if __name__ == "__main__":
    short_gmb_link = "https://g.co/kgs/FzNbcTp"  # Replace with actual short GMB link
    kgmid_url = expand_gmb_link_and_get_kgmid_url(short_gmb_link)

    if kgmid_url:
        extract_google_details(kgmid_url)

