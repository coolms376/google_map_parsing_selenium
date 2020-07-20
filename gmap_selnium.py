import io
import os
import csv
from selenium import webdriver as driver
from selenium import *
from time import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import logging



def elementfound(elementclass):
    if(len(dc.find_elements_by_class_name(elementclass))):
        return True
    else:
        return False

def write_file(dc):
    print("Wait Writing File... ")
    fieldnames = ['name', 'address','website','phone','rating','reviews','star_count','image', 'price','latitude','longitude','opening_hours']
    with open(file_path, mode='w',encoding="utf-8",newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(gether_data)
    print("Work Done Output are Place in a File that is Shown Below")
    print("File Directory =  "+file_path)
    dc.close()

def get_all_related_info(dc,action):

        result_json_data = open_hours = {}

        title = ratingdata = price = latitude = longitude = image = ''

        contact = {}

        rating = {}

        try:

            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME,'section-hero-header-image-hero-clickable'))
            )

            data_lat_and_long = dc.current_url.split("/")[6].split(",")

            latitude =  data_lat_and_long[0].replace('@','')

            longitude = data_lat_and_long[1] 

            title_array = dc.find_elements_by_css_selector(title_selector_class) # title

            image_data_array = dc.find_elements_by_css_selector("div.section-hero-header-image-hero-container.collapsible-hero-image > button > img")

            rating_data_array = dc.find_elements_by_css_selector(rating_review_star_selector)
            
            address  = dc.find_elements_by_css_selector('button[data-tooltip="Скопировать адрес"]')

            phone = dc.find_elements_by_css_selector('button[data-tooltip="Скопировать номер"]')

            web = dc.find_elements_by_css_selector('button[data-tooltip="Перейти на сайт"]')

            if(len(title_array)>0):
                title = title_array[0].text
                result_json_data['name'] = title
            else:
                result_json_data['name'] = ''
                
            if(len(address)>0):
                action.move_to_element(address[0])
                address = address[0].get_attribute('aria-label')[len('Адрес: '):-1]
                result_json_data['address'] = address
                

            if(len(phone)>0):
                action.move_to_element(phone[0])
                phone = phone[0].get_attribute('aria-label')[len('Телефон: '):-1]
                result_json_data['phone'] = phone

            if(len(web)>0):
                action.move_to_element(web[0])
                web = web[0].get_attribute('aria-label')[len('Сайт: '):-1]
                result_json_data['website'] = web
            

            if(len(rating_data_array)>0):

                ratingdata = rating_data_array[0].text.replace("\n","·").split("·")

                if(len(ratingdata) != 3):
                    for i in range(len(ratingdata),3):
                        ratingdata.append('')

                rating_title = ['rating','reviews','star_count']

                for i in range(len(rating_title)):
                    result_json_data[rating_title[i]] = ratingdata[i]
            else:
                result_json_data['rating'] = ''
                result_json_data['reviews'] = ''
                result_json_data['star_count'] = ''

            if(len(image_data_array)>0):
                    
                first_address = image_data_array[0]
                
                action.move_to_element(first_address)
                
                action.perform()
                
                image = image_data_array[0].get_attribute('src')
                if(len(image)>0 and image.find("maps.gstatic.com") == -1):
                    resolution_set = "=w1960-h1960-k-no"
                    start = 0
                    end = image.find('=w')
                    resolution_fix_image = image[start:end]+resolution_set
                    result_json_data['image'] = resolution_fix_image
            else:
                result_json_data['image'] =  ''

            price_array = dc.find_elements_by_class_name(price_selector_class)

            if(len(price_array)>0):
                price = price_array[0].text
                result_json_data['price'] = price
            else:
                result_json_data['price'] = ''

            sleep(1)

            result_json_data['latitude'] = latitude

            result_json_data['longitude'] = longitude

            if(len(dc.find_elements_by_class_name('cX2WmPgCkHi__expand-more'))>0 or len(dc.find_elements_by_class_name('cX2WmPgCkHi__expand-less'))>0):
                action.move_to_element(dc.find_elements_by_css_selector("#pane > div > div.widget-pane-content.scrollable-y > div > div > div.cX2WmPgCkHi__root.gm2-body-2.cX2WmPgCkHi__dense> div.cX2WmPgCkHi__summary-line.cX2WmPgCkHi__clickable")[0])
                action.click()
                action.perform()
                if(len(dc.find_elements_by_class_name('cX2WmPgCkHi__expand-less'))):
                    open_hours = get_open_hours()
                    if(len(open_hours)>0):
                        result_json_data['opening_hours'] = open_hours


            return result_json_data

        except NoSuchElementException:
            print("element")

# If the result Contains the Opening Hours then this method is responsible for Exracting Informtion From it.

def get_open_hours():

    opening_hours_array = []

    opening_hours_dict = {}

    opening_hours = dc.find_elements_by_class_name('section-open-hours-container')

    if(len(opening_hours)>0):

        action.move_to_element_with_offset(opening_hours[0],0,0)

        opening_hours = opening_hours[0].text

        opening_hours_array = opening_hours.rsplit('\n')

        element_special = dc.find_elements_by_class_name('lo7U087hsMA__row-special')

        elements_special = []

        for i in element_special:
            if(i.text != ''):
                elements_special.append(i.text)

        for i in elements_special:
                if(i in opening_hours_array):
                       opening_hours_array.remove(i)
        try:
             if(len(opening_hours_array)== 14 and len(opening_hours_array) %2 == 0):
                opening_hours_dict  = {opening_hours_array[i]: opening_hours_array[i + 1] for i in range(0, len(opening_hours_array), 2)}
            
        except:
            print(opening_hours_array)

        return opening_hours_dict

# This List hold all the gather results.

def main():

    wait = WebDriverWait(dc,30)

    # Mainly Script Startiing from this Line

    try:
        if(dc.current_url.find("/place/") == -1): # not a single place

            sleep(5)

            # No of pages for parsing info
            # max_page > 0 can be replace by true then this Script go to all the pages
            # and Extract result
            
            print(elementfound('section-result'))

            while(elementfound('section-result')):


                # Size specificies the results in the current page

                size = len(dc.find_elements_by_class_name('section-result'))

                if(size == 0):
                    break

                if(len(dc.find_elements_by_class_name('section-refresh-overlay-visible') )>0):

                    sleep(2)

                    # Wait untill ajax Call completed For gathering all Results for the Current page.
                    wait.until(
                            EC.invisibility_of_element((By.CLASS_NAME,'section-refresh-overlay-visible'))
                    )

                # Extracting the  results
                print(size)
                
                for i in range( size ):
                    try:     
                        wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME,'section-result'))
                        )

                        elements = dc.find_elements_by_class_name('section-result')

                        warning_of_corona = dc.find_elements_by_class_name('vTtwMg9xIJV__alert')

                        action = ActionChains(dc)

                        wait.until(
                            EC.invisibility_of_element((By.CLASS_NAME,"section-refresh-overlay-visible"))
                        )

            #print("Result button Click")

                        action.move_to_element(elements[i])

                        action.click(elements[i])

                        action.perform()

                        action = ActionChains(dc)

                        wait.until(
                            EC.invisibility_of_element((By.CLASS_NAME,"section-refresh-overlay-visible"))
                        )

                        wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME,'section-hero-header-title-title'))
                        )

                        temp_res = get_all_related_info(dc,action)

                        sleep(1)

                        gether_data.append(temp_res)

                        # get back to the previous page

                        dc.find_elements_by_class_name('section-back-to-list-button')[0].click()

                #print("Previous button Click")
                    except Exception as e: 
                        logger.error(e)
                        continue

                wait.until(
                         EC.presence_of_element_located((By.CLASS_NAME,'n7lv7yjyC35__button-next-icon'))
                )

                wait.until(
                         EC.invisibility_of_element((By.CLASS_NAME,'section-refresh-overlay-visible'))
                )

                button_array_after_refresh = dc.find_elements_by_class_name("n7lv7yjyC35__button-next-icon")

            #             print('Size = '+str(len(button_array_after_refresh)))

                if(len(button_array_after_refresh)>0):

                    button_after_refresh = button_array_after_refresh[0]

                    action.move_to_element(button_after_refresh)

                    if(button_after_refresh.get_attribute("disabled")):
                        break

                    button_after_refresh.click()

                    wait = WebDriverWait(dc,30)

                    wait.until(
                         EC.invisibility_of_element((By.CLASS_NAME,'section-refresh-overlay-visible'))
                    )
            write_file(dc)    
    except Exception as e:
            write_file(dc)


if __name__ == '__main__':
    
    # print("............................Work Done By Montu Sharma........................\n")
    # print("........If Works Fine Dont Forget to Give your Best Review And Reward........\n")
    # print("............................Love From India..................................\n")

    #get The input From the User

    givenString  = input("Please type Your Query String\n")

    givenString = givenString.strip()

    #opens a Chrome tab for automation

    dc = driver.Chrome() #

    # Some  DOM Class Constants
    #----------------------------------------------------------------------------
    title_selector_class = ".section-hero-header-title > div > div > h1"

    image_selector_class = "section-hero-header-image-hero-container collapsible-hero-image"

    price_selector_class = "bRqcEmw6ZsI__price-row"

    rating_review_star_selector = "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-description > div.section-hero-header-title-description-container > div > div.GLOBAL__gm2-body-2.section-rating-line"

    address_telephone_website_class = "widget-pane-link"

    #----------------------------------------------------------------------------

    # Chaging the given into a formatted Query String  For  Google Search

    queryStr = givenString.replace(" ", "+")

    print(queryStr)

    # URL To Search


    url = r"https://www.google.com/maps/search/"+queryStr+"/data=!3m1!4b1?hl=ru"

    # Specify File Name For the Saving the Extracted Content

    file_name = givenString.replace(' ','_')

    file_path = os.getcwd() + os.path.sep + file_name+ '.csv'

    # print(url)


    # Opening The Page

    page = dc.get(url)

    # Wait Is used for wait some Content to Load if that content is
    # this waits for max 30 Seconds before raising TimeoutException

    wait = WebDriverWait(dc,30)
    action = ActionChains(dc)

    # Main Function that Extact all the Informtion from the webresult and Prepare the gether_data list.


    #logging
    #-------------------------------------------------------------
    logger = logging.getLogger()

    logging_file  = os.getcwd() + os.path.sep + file_name+ '_logging.txt'

    logging.basicConfig(filename= logging_file, 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

    logger.setLevel(logging.ERROR)

    #Creating
    #--------------------------------------------------------------

    gether_data = []
    
    main()
