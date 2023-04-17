from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

import os
import sys
import time
import pickle as pk
#from bs4 import BeautifulSoup as bs 
from selenium.webdriver.chrome.options import Options

def check_for_extn_installation(driver, name):  #generates a screenshot to check for extension installation
    driver.get("https://chrome.google.com/webstore/detail/ghostery-%E2%80%93-privacy-ad-blo/mlomiejdfkolichcflejclcbmpeaniij?hl=en")
    #save screenshot
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
    file_name = name + '.png'
    driver.find_element(by=By.TAG_NAME, value='body').screenshot(file_name)

def extension_add(opts, extn): #adds extension
    opts.add_extension(extn)
    return opts

def dwn_path_add(opts, pth): #adds download path to download fingerprints
    prefs = {"download.default_directory" : pth}
    opts.add_experimental_option("prefs",prefs)

def iterate_and_add_text(extn, date_lst, text_lst):
    if len(date_lst) != len(text_lst):
        print("list lengths not equal")
        exit(1)

    for i in range(len(date_lst)):
        review_dict[extn][0].append(date_lst[i].text)
        review_dict[extn][1].append(text_lst[i].text)

def write_to_pickle(data_str, filename):
    filehandler = open(filename, 'wb')
    pk.dump(data_str, filehandler)
    filehandler.close()

def write_to_textfile(data_str, filename):
    filehandler = open(filename, 'wt')
    filehandler.write(str(data_str))
    filehandler.close()

def pretty_write_to_textfile(data_str, filename):
    filehandler = open(filename, 'wt')
    for key in data_str:
        filehandler.write(key)
        filehandler.write('\n')
        filehandler.write(str(len(review_dict[key][0])))
        filehandler.write('\n')
        for j in range(len(review_dict[key][0])):
            filehandler.write(review_dict[key][0][j])
            filehandler.write("\n")
            filehandler.write(review_dict[key][1][j])
            filehandler.write("\n---------------------------------------\n")

        filehandler.write('\n'*3)
        filehandler.write("-----------------------------------------------------------------------"*2)
        filehandler.write('\n'*3)
    filehandler.close()

xf = Xvfb()  #  xf = Xvfb(1920, 1080) - will create virtual display with 1920x1080 size
xf.start()
# browser won't appear

#extn_lst = ['', 'grammarly', 'gtranslate', 'honey', 'windows', 'cisco', 'tamper', 'netflix', 'scrcast', 'metamask']
#extn_lst = ['adobe', 'grammarly', 'honey', 'gtranslate', 'windows', 'tamper', 'netflix', 'scrcast', 'cisco', 'metamask']
extn_identifier = ["cfhdojbkjhnklbpkdaibdccddilifddb", "cjpalhdlnbpafiamejdnhcphjbkeiagm", "mlomiejdfkolichcflejclcbmpeaniij", "gcbommkclmclpchllfjekcdonpmejbdp", "jeoacafpbcihiomhlakheieifhpjdfeo", "pkehgijcmpdhfbdbbnkijodmdjhbjlgp", "lanfdkkpgfjfdikkncbnojekcppdebfp", "djflhoibgkdhkhhcedjiklpkjnoahfmg", "oiigbmnaadbkfbmpbfijlflahbdbdgdf", "ldpochfccmkkmhdbclfhpagapcfdljkj", "bgnkhhnnamicmpeenaelnjfhikgbkllg", "nngceckbapebfimnlniiiahkandclblb", "ahnanjpbkghcdgmlchbcfoiefnifjeni"]
extn_lst = ["adblock-plus-free-ad-bloc", "ublock-origin", "ghostery-–-privacy-ad-blo", "https-everywhere", "disconnect", "privacy-badger", "canvas-fingerprint-defend", "user-agent-switcher-for-c", "scriptsafe", "decentraleyes", "adguard-adblocker", "bitwarden-free-password-m", "no-script-suite-lite"]
#extn_lst = ['', 'ghostery', 'https', 'disconnect', 'user_agent', 'privacy_badger', 'adblock', 'ublock', 'cydec', 'canvas_antifp']

review_dict = {} #the dict has the key as extn_id and value as pair of date_list and text_list
for i in extn_lst:
    review_dict[i] = [[],[]]


for i in range(len(extn_lst)):
    options = Options()
    
    options.add_argument("--incognito")
    #cwd = os.getcwd() #assuming that the script is run inside the repo
    #pth = cwd+'/extensions/non_privacy_extn_crx/'
    #pth = pth + i + '.crx'
    #pth = '/home/ritik/pes/ghostery.zip'
    print("###########################")
    
    ### We dont need to add extensions for this experiment!
    #if i != '':
    #    options = extension_add(options, pth)

    driver = webdriver.Chrome(options=options)    
    url = "https://chrome.google.com/webstore/detail/"
    url = url + extn_lst[i] + "/" + extn_identifier[i]
    print(url)

    tabs_dict = {"review": "h-e-f-z-b.e-f-b.g-b", "support": "h-e-f-v-b.e-f-b.g-b"}
    date_n_text = {"review": ["ba-Eb-Nf", "ba-Eb-ba"], "support": ["v-b-E-Nf", "v-b-E-Oa"]}
    next_btn = {"review": ["dc-se"], "support": ["Aa.v-b-dc-se"]}
    for key in tabs_dict:
        driver.get(url)
        print(key)
        try:
            element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, tabs_dict[key]))
                    )
            element.click()
            time.sleep(10)
        except:
            print(str(extn_lst[i])+" does not have " + key + " tab")
            print("continuing to next extension.....")
            continue

        try:    
            review_date_element = driver.find_elements(By.CLASS_NAME, value=date_n_text[key][0])
            review_text_element = driver.find_elements(By.CLASS_NAME, value=date_n_text[key][1])
            iterate_and_add_text(extn_lst[i], review_date_element, review_text_element)
            print(1, extn_lst[i])
        except Exception as e:
            print(e)
            print("reviews/support " + key + " not found for extension: " + str(extn_lst[i]))
            print("continuing to next extension.....")
            continue

        while True:
            try:
                ret = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, next_btn[key][0])))
            
                ret.click() #clicking on next
                time.sleep(10) #sleep to allow reviews to load
                
                try:    
                    review_date_element = driver.find_elements(By.CLASS_NAME, value=date_n_text[key][0])
                    review_text_element = driver.find_elements(By.CLASS_NAME, value=date_n_text[key][1])
                    iterate_and_add_text(extn_lst[i], review_date_element, review_text_element)
                    print(2, extn_lst[i])
                except Exception as e:
                    print(e)
                    print("reviews/support " + key + " not found for extension: "+str(extn_lst[i]))
                    print("continuing to next extension.....")
                    break
        
            except TimeoutException as ex:
                print("Timeout Exception encountered")
                break

            except:
                print("Non-Timeout Exception encountered")
                break
    
    print(review_dict)
    driver.quit()

print("writing to file starts ...")
pretty_write_to_textfile(review_dict, "pretty_review.txt")
write_to_textfile(review_dict, "review.txt")
write_to_pickle(review_dict, "review.pickle")