from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import wget
import os

driver = webdriver.Chrome("/home/wai/Applications/chromedriver")

def getLogout():
    if checkLogin():
        driver.get('https://www.lynda.com/signout')

def getLogin():
    driver.get('https://www.lynda.com/signin')
    driver.find_element_by_id('email-address').send_keys("xxxx@googlemail.com", Keys.RETURN)
    time.sleep(3)
    driver.find_element_by_id('password-input').send_keys("xxxxx", Keys.RETURN)
    time.sleep(4)
    return checkLogin()

def checkLogin():
    try:
        driver.get('https://www.lynda.com/')
        driver.find_element_by_class_name('account-name')
        return True
    except:
        return False

def getPublicLinks(courseLink):
    cos = courseLink
    if checkLogin() == False:
        print("checking")
        getLogin()
    driver.get(cos)
    title = driver.find_element_by_class_name('default-title')
    title = title.get_attribute('data-course')
    courseVideoList = driver.find_elements_by_class_name("video-name")
    newCourseVideoList = []
    for i in courseVideoList:
        link = i.get_attribute('href')
        name = i.text
        tmp = [name, link]
        newCourseVideoList.append(tmp)

    return newCourseVideoList



def getExercise(courseLink):
    try:
        if checkLogin() == False:
            getLogin()
            driver.get(courseLink)
            driver.find_element_by_id('exercise-tab').send_keys(Keys.RETURN)
            time.sleep(3)
            exercise_file = driver.find_element_by_class_name('course-file').get_attribute('href')
            # print(exercise_file)
            #driver.find_element_by_link_text(exercise_file).click()
            driver.find_element_by_class_name('exercise-name').click()
        else:
            driver.get(courseLink)
            driver.find_element_by_id('exercise-tab').send_keys(Keys.RETURN)
            time.sleep(3)
            exercise_file = driver.find_element_by_class_name('course-file').get_attribute('href')
            #driver.find_element_by_link_text(exercise_file).click()
            driver.find_element_by_class_name('exercise-name').click()
    except:
        print ("no exercise file")

def askedCourse():
    courseLinks = []
    while True:
        ans = input("Want to add")
        if ans == "Y" or ans == "y":
            link = input("> ")
            if link:
                courseLinks.append(link)
        else:
            break

    return courseLinks

def createFolder(name):
    path = os.getcwd()+'/videos/'+name
    os.mkdir(path)
    if os.path.isdir(path):
        return (path)

def getTitle(courseLink):
    cos = courseLink
    if checkLogin() == False:
        print ("checking")
        getLogin()
    driver.get(cos)
    title = driver.find_element_by_class_name('default-title')
    title = title.get_attribute('data-course')
    return (title)

def getVideo(courseLink,directory):
    cos = courseLink
    if checkLogin() == False:
        #print ("checking")
        getLogin()
    driver.get(cos)
    title = driver.find_element_by_class_name('default-title')
    title = title.get_attribute('data-course')
    print (title)
    #print ('go back to page')
    driver.get(cos)
    time.sleep(2)
    #print ("calling")
    tmp = getPublicLinks(cos)
    #print (tmp)

    #for i in tmp:
    #    name = i[0]
    #    f = open(title + '.txt', '+a')
    #    f.write(name+'\n')
    #    f.close()

    for i in tmp:
        link = i[1]
        print (link)
        driver.get(link)
        # print (driver.page_source)
        time.sleep(4)
        ans = driver.find_elements_by_class_name('player')
        res = (ans[1].get_attribute('data-src'))
        #print(res)
        #f = open(title + '.txt', 'a+')
        #f.write(res + '\n')
        wget.download(res, directory)
        #f.close()
        time.sleep(2)


def readFILE():
    ans = []
    with open("/home/wai/Documents/page.txt")as file:
        for line in file:
            if "\n" in line:
                line = line.replace("\n", " ")
                if line != ' ':
                    line = line
                    line = " ".join(line.split())
                    ans.append(line)
    return ans

links = readFILE()
if checkLogin() == False:
    getLogin()
    time.sleep(3)
for i in links:
   direct = createFolder(getTitle(i))
   getVideo(i,direct)
getLogout()
driver.close()

def getVideo(courseLink):
    cos = courseLink
    if checkLogin() == False:
        getLogin()
    driver.get(cos)
    title = driver.find_element_by_class_name('default-title')
    title = title.get_attribute('data-course')
    print (title)
    driver.get(cos)
    time.sleep(2)
    tmp = getPublicLinks(cos)

    for i in range(len(tmp)):
        if i > 21:
            link = tmp[i][1]
            print (link)
            driver.get(link)
            time.sleep(4)
            ans = driver.find_elements_by_class_name('player')
            res = (ans[1].get_attribute('data-src'))
            wget.download(res)
            time.sleep(2)


