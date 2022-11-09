from re import search
import time
import os
from os.path import exists
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

STATE_NAME = ""
BUTTON_INDEX = 7

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Remote(command_executor="http://localhost:57744", desired_capabilities={})
driver.session_id = "7ebe628b18f5cba2bbe2200e650d326e"
# print(driver.command_executor._url)
# print(driver.session_id)

# driver.get("https://src.udiseplus.gov.in/newSearchSchool/searchSchool")

elem = driver.find_elements(By.CLASS_NAME, "search-box")

button_list = []
for element in elem:
    buttons = element.find_elements(By.TAG_NAME, "a")
    for button in buttons:
        button_list.append(button)

actions = ActionChains(driver)

for button in button_list:
    # if button != button_list[BUTTON_INDEX]:
    #     continue
    actions.move_to_element(button).click().perform()
    
    time.sleep(1)
    ddelement= Select(driver.find_element(By.ID, 'stateName'))
    no_of_states = len(ddelement.options)
    
    for state_index in range(1, no_of_states):
        time.sleep(1)
        # actions.move_to_element(ddelement).select_by_index(state_index).perform()
        ddelement.select_by_index(state_index)
        if ddelement.first_selected_option.text != STATE_NAME:
            continue

        print(f"For state {ddelement.first_selected_option.text}")        
        time.sleep(1)
        distdelement= Select(driver.find_element(By.ID, 'districtId'))
        
        no_of_districts = len(distdelement.options)

        for district_index in range(1, no_of_districts):
            ddelement.select_by_index(state_index)
            time.sleep(1)
            distdelement.select_by_index(district_index)
            print(f"For district {distdelement.first_selected_option.text}")        
        
            time.sleep(1)
            block_element= Select(driver.find_element(By.ID, 'blockId'))
            
            no_of_blocks = len(block_element.options)

            for block_index in range(1, no_of_blocks):
                # print(block_element.options[block_index].text)
                # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"blockId[value={block_element.options[block_index].text}]")))
                ddelement.select_by_index(state_index)
                time.sleep(1)
                distdelement.select_by_index(district_index)
                time.sleep(1)
                block_element.select_by_index(block_index)
                print(f"For block {block_element.first_selected_option.text}") 
                filename = f"./school_data/{button.text}/{ddelement.first_selected_option.text}/{distdelement.first_selected_option.text}/{block_element.first_selected_option.text}.csv"
                
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                captcha = driver.find_element(By.NAME, "captcha")
                captcha.clear()
                for key in "e5c022":
                    captcha.send_keys(key)

                time.sleep(2)
                searchButton = driver.find_element(By.ID, "newSearchSchool")
                searchButton.submit()

                time.sleep(2)
                no_of_items_dropdown = Select(driver.find_element(By.NAME, "newSearchSchoolTable_length"))
                no_of_items_dropdown.select_by_visible_text("1,000")

                time.sleep(1)
                data_table = driver.find_element(By.ID, "newSearchSchoolTable")
                
                schools_dict_data = []
                for row in data_table.find_elements(By.CSS_SELECTOR, "tr"):
                    print("---NEW ROW---")
                    school_data = {"Seq No.":None, "UDISE Code":None, "School Name":None, "School Location": None}
                    school_list_data = []
                    for cell in row.find_elements(By.TAG_NAME, "td"):
                        school_list_data.append(cell.text)
                    if len(school_list_data) == 4:
                        school_data = {
                            "Seq No.":school_list_data[0], 
                            "UDISE Code":school_list_data[1], 
                            "School Name":school_list_data[2].replace("More Details","").strip(), 
                            "School Location": school_list_data[3]
                        }
                        schools_dict_data.append(school_data)
                    
                if len(schools_dict_data):
                    with open(filename, "w") as f:
                        writer_file = csv.DictWriter(f, fieldnames=["Seq No.", "UDISE Code", "School Name", "School Location"])
                        writer_file.writeheader()
                        writer_file.writerows(schools_dict_data) 

                time.sleep(10)
        


# driver.close()