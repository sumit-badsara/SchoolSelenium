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


STATE_NAME = "Telangana"
BUTTON_INDEX = 7

driver = webdriver.Remote(command_executor="http://localhost:56242", desired_capabilities={})
driver.close()
driver.session_id = "59000df3a35fc46dba347b04c461e788"
print(driver.session_id)


tree_struct = {
    "Karnataka":[
        "BENGALURU RURAL",
        "BENGALURU U NORTH",
        "BENGALURU U SOUTH"
    ],
    "Telangana":[
        "HYDERABAD",
        "RANGAREDDY",
        "MEDCHAL"
    ]
}

elem = driver.find_elements(By.CLASS_NAME, "search-box")

button_list = []
for element in elem:
    buttons = element.find_elements(By.TAG_NAME, "a")
    for button in buttons:
        button_list.append(button)

actions = ActionChains(driver)

for button_index in range(2, len(button_list)):
    button = button_list[button_index]
    actions.move_to_element(button).click().perform()
    
    time.sleep(1)
    ddelement= Select(driver.find_element(By.ID, 'stateName'))
    no_of_states = len(ddelement.options)
    
    for state_text in tree_struct.keys():
        time.sleep(2)
        # actions.move_to_element(ddelement).select_by_index(state_index).perform()
        ddelement.select_by_visible_text(state_text)

        print(f"For state {ddelement.first_selected_option.text}")        
        time.sleep(2)
        distdelement= Select(driver.find_element(By.ID, 'districtId'))
        
        no_of_districts = len(distdelement.options)

        for district_text in tree_struct[state_text]:
            ddelement.select_by_visible_text(state_text)
            time.sleep(2)
            distdelement.select_by_visible_text(district_text)
            print(f"For district {distdelement.first_selected_option.text}")        
        
            time.sleep(2)
            block_element= Select(driver.find_element(By.ID, 'blockId'))
            
            no_of_blocks = len(block_element.options)

            for block_index in range(1, no_of_blocks):
                # print(block_element.options[block_index].text)
                # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"blockId[value={block_element.options[block_index].text}]")))
                ddelement.select_by_visible_text(state_text)
                time.sleep(0.5)
                distdelement.select_by_visible_text(district_text)
                time.sleep(0.5)
                block_element.select_by_index(block_index)
                print(f"For block {block_element.first_selected_option.text}") 
                filename = f"./data/{button.text}/{ddelement.first_selected_option.text}/{distdelement.first_selected_option.text}/{block_element.first_selected_option.text}.csv"
                file_exists = exists(filename)
                if file_exists:
                    continue
                print("Missing")

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                captcha = driver.find_element(By.NAME, "captcha")
                captcha.clear()
                for key in "200bf7":
                    captcha.send_keys(key)

                # time.sleep(2)
                searchButton = driver.find_element(By.ID, "newSearchSchool")
                searchButton.submit()

                # time.sleep(2)
                no_of_items_dropdown = Select(driver.find_element(By.NAME, "newSearchSchoolTable_length"))
                no_of_items_dropdown.select_by_visible_text("1,000")

                # time.sleep(2)
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

                time.sleep(2)
        


# driver.close()