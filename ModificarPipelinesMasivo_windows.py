# ODP


import csv
import clipboard as cp
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def readCSV(fileName):
    data = []
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            separator = str(row) \
                .replace("[", "") \
                .replace("]", "") \
                .replace("'", "") \
                .replace('"', "") \
                .split(";")
            data.append(separator)
    return data


def readTXT2(filename):
    array = []
    b = "APP-OSB_12C_Activations"
    r = "APP-OSB_12C_nuevo"
    v = "activations.war"
    v2 = "nuevo.jar"
    b1 = "log_Prod_OSB12c_Activations.txt"
    b2 = "log_Prod_OSB12c_nuevo.txt"
    with open(filename, encoding="utf-8") as file:
        text = file.readlines()
    for i in text:
        if b in i:
            array.append(i.replace(b, r))
        elif v in i:
            array.append(i.replace(v, v2))
        elif b1 in i:
            array.append(i.replace(b1, b2))
        else:
            array.append(i)

    print(array)
    stringToCopy = ""
    for a in array:
        # print(a)
        a = a.replace("['p", "p").replace("']", "").replace(r'\n,', "\n").replace(r'\n",', "\n") \
            .replace(r"\n',", "\n").replace(r"\'", "'").replace('"    ', "").replace(r"\t", "\t")
        # print(a)
        stringToCopy = stringToCopy + a
    return stringToCopy


def readTXT(filename):
    with open(filename, encoding="utf-8") as file:
        text = file.readlines()
    return text


def cleanSpecialCharacter(arrayList):
    stringToCopy = ""
    for a in arrayList:
        # print(a)
        a = a.replace("['p", "p").replace(r'\n,', "\n").replace(r'\n",', "\n") \
            .replace(r"\n',", "\n").replace(r"\'", "'").replace('"    ', "").replace(r"\t", "\t")\
            .replace("if [ -f ${", '"   if [ -f ${', 1)
        # print(a)
        stringToCopy = stringToCopy + a
    return stringToCopy


def productionSteps(div_path):
    if "Operaciones" in div_path[10]:
        nombre_app = str(div_path[8])
    else:
        nombre_app = str(div_path[10])
    print(nombre_app)
    apliacionyml = "./crm_portal/DeliveryDatasources_CRM-Portal-{}_prod.yml".format(str(div_path[8]))
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/logs_Prod_{}.txt".format(nombre_app.replace("APP-", ""))
    #print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    #print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "apliacion_base"
    change4by = apliacionyml

    pipeline = readTXT("resources/pipeline_prod.txt")
    new_pipeline = []
    contador = 0
    for line in pipeline:
        if change1 in line:
            if change2 in line:
                new_pipeline.append(line.replace(change2, change2by).replace(change1, change1by))
            else:
                new_pipeline.append(line.replace(change1, change1by))
        elif change2 in line:
            new_pipeline.append(line.replace(change2, change2by))
        elif change3 in line:
            new_pipeline.append(line.replace(change3, change3by))
        elif change4 in line:
            new_pipeline.append(line.replace(change4, change4by))
        else:
            new_pipeline.append(line)

    w = cleanSpecialCharacter(new_pipeline)

    cp.copy(w)


def preproductionSteps(div_path):
    nombre_app = "APP-CRM-Portal-" + str(div_path[8]) + "/" + str(div_path[14]).replace("%20", "")
    print(nombre_app)
    apliacionyml = "./crm_portal/DeliveryDatasources_CRM-Portal-{}_prod.yml".format(str(div_path[8]))
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/CRMBD_UAT_{}S{}.txt".format(
        str(div_path[8]).replace("APP-", "").replace("BD-", ""),
        str(div_path[14]).replace("%20", "").replace("Semilla", ""))
    print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    print(change2by)
    w = cleanSpecialCharacter(readTXT("resources/pipeline_preprod.txt"))
    cp.copy(w)


def desarrolloSteps(filename, div_path):
    nombre_app = str(div_path[8])
    #nombre_app = "APP-CRM-Portal-" + str(div_path[8]) + "/" + str(div_path[14]).replace("%20", "")
    print(nombre_app)
    apliacionyml = ""
    change1 = "Deploy to Production"
    change1by = "Deploy to Production_222"
    #print(change1by)
    change2 = 'environments: "Production"'
    change2by = change2.replace("Production", "Production_222")
    #print(change2by)
    change3 = "nombre_componente"
    change3by = nombre_app
    change4 = "apliacion_base"
    change4by = apliacionyml

    pipeline = readTXT(filename)
    new_pipeline = []
    for line in pipeline:
        if change1 in line:
            if change2 in line:
                new_pipeline.append(line.replace(change2, change2by).replace(change1, change1by))
            else:
                new_pipeline.append(line.replace(change1, change1by))
        elif change2 in line:
            new_pipeline.append(line.replace(change2, change2by))
        elif change3 in line:
            new_pipeline.append(line.replace(change3, change3by))
        elif change4 in line:
            new_pipeline.append(line.replace(change4, change4by))
        else:
            new_pipeline.append(line)

    w = cleanSpecialCharacter(new_pipeline)
    cp.copy(w)


def jenkinsPipeline(addparameter, fileURLsName, pipelineDes):
    """
    :param addparameter: 1 para agregar el parametro tipo string, 0 - si no desea agregar
    :param fileURLsName: ruta del archivo donde estan las urls de los pipelines
    :param pipelineDes: ruta del archivo base del pipeline

    """
    i = 0
    urls = readCSV(fileURLsName)
    segunda = 0
    try:
        url_home = "http://10.100.66.112:8080/job/RPA/job/Desarrollo/job/Anulacion_De_Pedidos/configure"

        browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

        browser.get(url_home)
        browser.maximize_window()
        browser.implicitly_wait(10)

        wait = WebDriverWait(browser, 10)
        assert 'Sign in [Jenkins]' in browser.title

        # se realiza el login en jenkins
        username = browser.find_element(By.ID, 'j_username')
        username.send_keys('admin')

        password = browser.find_element(By.NAME, "j_password")
        password.send_keys('admin123')

        btnSingIn = browser.find_element(By.NAME, 'Submit')
        btnSingIn.click()

        for url in urls:
            # for i in range(0, 1):

            u = str(url).replace("[", "").replace("]", "").replace("'", "")
            browser.get(u)

            if segunda == 1:
                alert = browser.switch_to.alert
                sleep(1)
                alert.accept()

            if "Desarrollo" in u:
                div_path = u.split("/")
                #print(div_path)
                desarrolloSteps(pipelineDes, div_path)

            elif "Preproduccion" in u:
                div_path = u.split("/")
                #print(div_path)
                productionSteps(div_path)

            elif "Produccion" in u:
                div_path = u.split("/")
                #print(div_path)
                productionSteps(div_path)

            # browser.get("http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/Hola%20mundo/configure")
            sleep(1)
            browser.execute_script("window.scrollTo(0, 1800)")
            sleep(1)

            if addparameter == 1:
                # agrega un nuevo valor parametrizado al projecto
                add_parameter = browser.find_element(By.XPATH, "//button[contains(@suffix,'parameterDefinitions')]")

                # print(add_parameter.text)
                add_parameter.click()

                select_parameter = browser.find_elements(By.CSS_SELECTOR, ".yuimenuitem")
                for parameter in select_parameter:
                    # print(parameter.text)
                    if parameter.text == "Parámetro de cadena":
                        parameter.click()
                        break
                name = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='parameter.name' and @value='']")))
                name.send_keys("ChangeOrder")
                sleep(2)
            sleep(2)

            # se hace click el el cuadrop de texto, se selecciona todo con ctrl+a y se borra todo
            scriptPipeline =  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ace_content')]")))
            scriptPipeline.click()
            action = ActionChains(browser)
            action.key_down(Keys.CONTROL) \
                .send_keys("a") \
                .key_up(Keys.CONTROL).send_keys(Keys.RETURN) \
                .perform()
            sleep(1)
            action.key_down(Keys.CONTROL) \
                .send_keys("v") \
                .key_up(Keys.CONTROL) \
                .perform()
            sleep(2)

            # nombre = "evidencia" + str(i) + ".png"
            # browser.save_screenshot(nombre)

            #se guardan los cambios

            btnSave = browser.find_element(By.XPATH, "/html/body/div[4]/div[2]/form/div[1]/div[8]/div/span[1]/span/button")
            #action.move_to_element(btnSave).click().perform()
            btnSave.click()
            sleep(2)
            i += 1
            segunda = 0

    except Exception as e:
        print(e)
        browser.quit()

    browser.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    inicio = time.time()
    print("Inicia la ejecucion ")
    print("\n")


    jenkinsPipeline(0, "./resources/ejecutar_windows.csv", "resources/pipeline_uipath.txt")

    fin = time.time()
    print("Finaliza la ejecucion")
    print("\n")
    print(" *******  Tiempo de ejecución:  *******")
    print(fin - inicio)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
