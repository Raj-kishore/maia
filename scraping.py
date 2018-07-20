import os
from ..default.helpers import scrapehelper as sh
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
def scrape(username: str, password: str) -> None:
  current_dir = os.path.dirname(os.path.abspath(__file__))
  driver = sh.get_driver("chrome")
  driver.implicitly_wait(10)
  Blocks = ""
  #metaLink = objGS().get_meta_link()
  metaLink = "https://erptools.capgemini.com/content/capgemini-auto-remediation-tool-c-art"
  assetDetails = 0
  print("Meta link  > " + metaLink)
  # Get some content
  # TODO
  driver.get(metaLink)
  print(driver)
  Str = driver.title
  print(Str.replace("|",""))
  try:
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "page-header"))
    )
  finally:
    # write some content
    # TODO
    title = driver.find_element_by_xpath("/html/body/div[2]/div/section/h1").text

    # block 1 : Page title
    PageTitle = "title\n"
    PageTitle = PageTitle + driver.find_element_by_xpath('//*[@id="edit-group_asset"]/div/div[1]/div[2]/div').text
    PageTitle = PageTitle + "\n"

    # block 2 : Page summary
    PageSummary = "\nsummary\n"
    fieldItemEven = driver.find_element_by_xpath('//*[@id="edit-group_description"]/div/div/div/div')
    fieldItemEvenHTML = fieldItemEven.get_attribute("innerHTML")
    find1stTwoChar = fieldItemEvenHTML[:2]
    print("tag starts with " + find1stTwoChar)
    if find1stTwoChar == "<u":
      countList = len(driver.find_elements_by_xpath('//*[@id="edit-group_description"]/div/div/div/div/ul/li'))
      for x in range(countList):
        x += 1
        PageSummary = PageSummary + driver.find_element_by_xpath(
          '//*[@id="edit-group_description"]/div/div/div/div/ul/li['+str(x)+']').text+" "
    elif find1stTwoChar == "<p":
      countPTags = len(driver.find_elements_by_xpath('//*[@id="edit-group_description"]/div/div/div/div/p'))
      for x in range(countPTags):
        x+=1
        PageSummary += driver.find_element_by_xpath(
        '//*[@id="edit-group_description"]/div/div/div/div/p['+str(x)+']').text+" "
    else:
      print("Check error")


    PageSummary = PageSummary + "\n"

    print("--------- Asset_Details----------")
    # block 3 : Asset details
    AssetDetail_Content = "-----Asset details-----\n"
    # Category
    # Price details
    # version number
    # asset tech
    AssetsCount = len(driver.find_elements_by_xpath('//*[@id="edit-group_asset"]/div/div'))
    for i in range(AssetsCount):
      i+=1
      getTitle = driver.find_element_by_xpath('//*[@id="edit-group_asset"]/div/div['+str(i)+']/div[1]').text
      if getTitle[:2] != "Na":
         if getTitle[:2] == "Ca":
           AssetDetail_Content += getTitle+"\n"
           catCount = len(driver.find_elements_by_xpath('//*[@id="edit-group_asset"]/div/div[2]/div[2]/div/span'))
           for r in range(catCount):
             r += 1
             getSummary = driver.find_element_by_xpath(
               '//*[@id="edit-group_asset"]/div/div[2]/div[2]/div/span[' + str(r) + ']').text
             AssetDetail_Content += getSummary+" "
           AssetDetail_Content += "\n"
         elif getTitle[:2] == "Ve":
           getSummary = driver.find_element_by_xpath('//*[@id="edit-group_asset"]/div/div[4]/div[2]/div/div/div[2]/div').text
           AssetDetail_Content += getTitle+"\n"
           AssetDetail_Content += getSummary+"\n"
         elif getTitle[:2] == "As":
           getSummary = driver.find_element_by_xpath(
             '//*[@id="edit-group_asset"]/div/div[5]/div[2]/div/span').text
           AssetDetail_Content += getTitle + "\n"
           AssetDetail_Content += getSummary + "\n"
         else:
           getSummary = driver.find_element_by_xpath(
             '//*[@id="edit-group_asset"]/div/div['+str(i)+']/div[2]/div').text
           AssetDetail_Content += getTitle + "\n"
           AssetDetail_Content += getSummary + "\n"
  # AssetDetail_Content += Category + Pricing + VersionNo + AssetTech + Target


    print("--------- Asset details ----------")
    # block 4 : Asset owner details
    AssetDetail_Owner = "-----Asset_Owner_Details-----\n"
    AssetOwnerItems = len(driver.find_elements_by_xpath('//*[@id="edit-group_asset_owner"]/div/div'))
    for ra in range(AssetOwnerItems):
      ra+=1
      getOwnerTitle = driver.find_element_by_xpath('//*[@id="edit-group_asset_owner"]/div/div['+str(ra)+']/div[1]').text
      getOwnerTitle = getOwnerTitle.strip()
      AssetDetail_Owner += getOwnerTitle + "\n"
      if getOwnerTitle[-3:] == "BU:" :
        getOwnerTSummary = driver.find_element_by_xpath('//*[@id="edit-group_asset_owner"]/div/div[1]/div[2]/div/span').text
      else:
        getOwnerTSummary = driver.find_element_by_xpath(
          '//*[@id="edit-group_asset_owner"]/div/div['+str(ra)+']/div[2]/div').text
      AssetDetail_Owner += getOwnerTSummary+"\n"


    # block 5 : Key features
    print("Scrapping key features")
    keyFeatures = "-----Key_Features-----\n"
    keyFeatures += "Key Features\n"
    fieldItemEven = driver.find_element_by_xpath('//*[@id="edit-group_key_features"]/div/div/div/div')
    fieldItemEvenHTML = fieldItemEven.get_attribute("innerHTML").strip()
    find1stTwoChar = fieldItemEvenHTML[:2]
    print("Key feature tag starts with "+find1stTwoChar)
    if find1stTwoChar == "<u":
      print("Tag found is : u")
      for l in range(len(driver.find_elements_by_xpath('//*[@id="edit-group_key_features"]/div/div/div/div/ul/li'))):
        l += 1
        keyFeatures += driver.find_element_by_xpath(
          '//*[@id="edit-group_key_features"]/div/div/div/div/ul/li['+str(l)+']').text
      print("Looking for tag : p")
      Pxpath = '//*[@id="edit-group_key_features"]/div/div/div/div/p'
      checkElem = check_exists_by_xpath(Pxpath, driver)
      if checkElem:
        print("p tag found")
        for l in range(len(driver.find_elements_by_xpath('//*[@id="edit-group_key_features"]/div/div/div/div/p'))):
           ll = l + 1
           keyFeatures += driver.find_element_by_xpath(
          '//*[@id="edit-group_key_features"]/div/div/div/div/p[' + str(ll) + ']').text
        print("p tag added successfully")
    elif find1stTwoChar == "<p":
      print("Tag found is : p")
      for l in range(len(driver.find_elements_by_xpath('//*[@id="edit-group_key_features"]/div/div/div/div/p'))):
        ll = l + 1
        keyFeatures += driver.find_element_by_xpath(
          '//*[@id="edit-group_key_features"]/div/div/div/div/p[' + str(ll) + ']').text
      print("Looking for tag : u")
      ULxpath = '//*[@id="edit-group_key_features"]/div/div/div/div/ul/li'
      checkElem = check_exists_by_xpath(ULxpath, driver)
      if checkElem: # check if ul tag exists
        print("u tag found")
        for l in range(len(driver.find_elements_by_xpath('//*[@id="edit-group_key_features"]/div/div/div/div/ul/li'))):
          l += 1
          keyFeatures += driver.find_element_by_xpath(
            '//*[@id="edit-group_key_features"]/div/div/div/div/ul/li[' + str(l) + ']').text
          print("u tag added successfully")
    else:
      print("Check for error")

    keyFeatures += "\n"

    # bolck 6 : Assets
    Assets = "-----Asset_Object-----\n"
    AssetElements = driver.find_elements_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div')
    CountAssetElements = len(AssetElements)
    for i in range(CountAssetElements):
      i += 1
      print("Level 1 :"+str(i))

      # get Asset titles
      AssetTitle = driver.find_element_by_xpath(
        '//*[@id="edit-group_asset_upload"]/div/div/div[' + str(i) + ']/h4').text
      print("Asset Titles Found : " + AssetTitle)
      Assets += "\n" + AssetTitle + "\n"

      # get Asset sub titles
      countParentofEvenOdd = len(
        driver.find_elements_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div[' + str(i) + ']/div'))
      for m in range(countParentofEvenOdd):
        m += 1
        SubT = driver.find_element_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div['+str(i)+']/div['+str(m)+']/div[1]').text
        Assets += SubT +" {"

        xpath = '//*[@id="edit-group_asset_upload"]/div/div/div['+str(i)+']/div['+str(m)+']/div[2]/div'
        checkElem = check_exists_by_xpath(xpath,driver)
        if checkElem:
          CountAssetChildren = len(driver.find_elements_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div['+str(i)+']/div['+str(m)+']/div[2]/div'))
          if CountAssetChildren != 0:
            for j in range(CountAssetChildren):
              j += 1
              # get if tag is span of a type
              checkSpan = driver.find_element_by_xpath(
              '//*[@id="edit-group_asset_upload"]/div/div/div[' + str(i) + ']/div['+str(m)+']/div[2]/div[' + str(j) + ']')
              checkSpanHTML = checkSpan.get_attribute("innerHTML").strip()
              getfirstTwoChar = checkSpanHTML[:2]
              print("first two characters are " + getfirstTwoChar)
              #print("Node 1 =" + str(ii) + " Node 2 ="+str(m)+" & Node 3 =" + str(jj))
              if getfirstTwoChar == "<s":
                bt = driver.find_element_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div['+str(i)+']/div['+str(m)+']/div[2]/div[' + str(j) + ']/span/a').text
                bh = driver.find_element_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div['+str(i)+']/div['+str(m)+']/div[2]/div[' + str(j) + ']/span/a').get_attribute("href")
              elif getfirstTwoChar == "<a":
                 bt = driver.find_element_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div[' + str(i) + ']/div['+str(m)+']/div[2]/div[' + str(j) + ']/a').text
                 bh = driver.find_element_by_xpath('//*[@id="edit-group_asset_upload"]/div/div/div[' + str(i) + ']/div['+str(m)+']/div[2]/div[' + str(j) + ']/a').get_attribute("href")
              else:
                bh,bt = ""

              Assets += '{"'+ bt +'","'+bh+'"}'
              if j != CountAssetChildren:
                Assets += ","
        if m != countParentofEvenOdd:
          Assets += ","
    Assets += "}"
    Assets += "\n"
    print("-------------***-------------------")
    print("Assets in the end :"+Assets+"\n")
    print("-------------***-------------------")
    # block 9 : rating
    Rating = "\n-----Average_Rating-----\n"
    Rating += "Rating\n"
    countSpans = len(driver.find_elements_by_xpath('//*[@id="fivestar-custom-widget"]/div/div/div/div/div[2]/div/span'))
    print("Number of spans found :"+str(countSpans))
    if countSpans == 3:
      # if span = 3, votes found
      b2 = driver.find_element_by_xpath('//*[@id="fivestar-custom-widget"]/div/div/div/div/div[2]/div/span[2]/span').text
      Rating += b2+"\n"
    elif countSpans == 1:
      # if span = 1, no votes yet
      b2 = driver.find_element_by_xpath('//*[@id="fivestar-custom-widget"]/div/div/div/div/div[2]/div/span').text
      Rating += b2 + "\n"
    else:
      Rating += "Check for errors \n"


    regChar = title.replace("|","")
    Blocks = Blocks + PageTitle +PageSummary+  AssetDetail_Content + AssetDetail_Owner + keyFeatures + Assets + Rating
    sh.write_scraping_data(Blocks, current_dir, "Asset Details -"+regChar,
                             metaLink,
                             "txt", "")

  driver.quit()

def check_exists_by_xpath(Xpath, Driver):
    try:
        Driver.find_element_by_xpath(Xpath)
    except NoSuchElementException:
        return False
    return True