# ODP


import csv
import logging
import time
from time import sleep

import clipboard as cp
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
        a = a.replace("['p", "p").replace("']", "").replace(r'\n,', "\n").replace(r'\n",', "\n") \
            .replace(r"\n',", "\n").replace(r"\'", "'").replace('"    ', "").replace(r"\t", "\t") \
            .replace("if [ -f ${", '"   if [ -f ${', 1)
        # print(a)
        stringToCopy = stringToCopy + a
    return stringToCopy


def productionStep(div_path):
    if "Operaciones" in div_path[10]:
        nombre_app = str(div_path[8])
    else:
        nombre_app = str(div_path[10])
    print(nombre_app)
    apliacionyml = "./crm_portal/DeliveryDatasources_CRM-Portal-{}_prod.yml".format(str(div_path[8]))
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/logs_Prod_{}.txt".format(nombre_app.replace("APP-", ""))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "apliacion_base"
    change4by = apliacionyml

    pipeline = readTXT("resources/Pipeline_Deploy_Prod(Fenix).txt")
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


def productionStepRutas(div_path, ruta):
    if "Operaciones" in div_path[10]:
        nombre_app = str(div_path[8]).replace("PrepagoBD-", "GODIGO-")
    else:
        nombre_app = str(div_path[10]).replace("PrepagoBD-", "GODIGO-")
    print(nombre_app)
    apliacionyml = "./crm_portal/" + ruta
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/logs_Prod_{}.txt".format(nombre_app.replace("APP-", ""))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = "APP-CRM-Portal-" + nombre_app
    change4 = "apliacion_base"
    change4by = apliacionyml

    pipeline = readTXT("resources/Pipeline_Deploy_Prod(Prepago y CRM BD).txt")
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


def productionSteps(div_path, componente):
    # nombre_app = "APP-JbossComunitario-" + div_path[8].replace("APP-", "")
    nombre_app = div_path[8]
    print(nombre_app)
    print(componente)
    apliacionyml = "Nom_Pipeline"
    # change1 = "logs_CD/cambiar.txt"
    # change1by = "logs_CD/log_PROD_JbossComunitario{}.txt".format(div_path[8].replace("APP-", "_"))
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/Promociones_Prod_{}.txt".format(
        str(div_path[8]).replace("APP-", "").replace("BD-", "").replace("Promociones-", ""))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "nombrepromo"
    change4by = componente
    change5 = "Componente_SIN_Extension"
    change5by = componente.replace(".ear", "").replace(".war", "")
    pipeline = readTXT("resources/Pipeline_Deploy_Prod(Promociones).txt")
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
        elif change5 in line:
            new_pipeline.append(line.replace(change5, change5by))
        else:
            new_pipeline.append(line)

    w = cleanSpecialCharacter(new_pipeline)
    cp.copy(w)


def preproductionStep(div_path):
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


def preproductionSteps(div_path, componente):
    print("preproduccion componentes")
    nombre_app = "APP-JbossComunitario-" + div_path[8].replace("APP-", "")
    print(nombre_app)
    print(componente)
    apliacionyml = "Nom_Pipeline"
    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/log_UAT_JbossComunitario{}_S11.txt".format(div_path[8].replace("APP-", "_"))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "componente_EAR"
    change4by = componente
    change5 = "Componente_SIN_Extension"
    change5by = componente.replace(".ear", "").replace(".war", "")
    pipeline = readTXT("resources/Pipeline_Deploy_Preproduccion(Jboss Comunitario CRM) (1).txt")
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
        elif change5 in line:
            new_pipeline.append(line.replace(change5, change5by))
        else:
            new_pipeline.append(line)

    w = cleanSpecialCharacter(new_pipeline)
    cp.copy(w)


def UATStep(div_path):
    if "Operaciones" in div_path[10]:
        nombre_app = str(div_path[8])
    else:
        nombre_app = str(div_path[10])
    # nombre_app = "APP-CRM-Portal-" + str(div_path[8]).replace("PrepagoBD-", "GODIGO-") + "/" + str(
    #     div_path[14]).replace("%20", "").title()
    print(nombre_app)
    if "Semilla" in str(div_path[14]):
        apliacionyml = "./crm_portal/DeliveryDatasources_CRM-Portal-{}_UAT_S{}.yml".format(
            str(div_path[8]), str(div_path[14]).replace("%20", "").replace("Semilla", ""))
        change1 = "logs_CD/cambiar.txt"
        change1by = "logs_CD/logs_UAT_{}_S{}.txt".format(div_path[8], str(div_path[14]).replace("%20", "")
                                                         .replace("Semilla", ""))
    else:
        apliacionyml = "./crm_portal/DeliveryDatasources_CRM-Portal-{}_UAT_G{}.yml".format(
            str(div_path[8]).replace("PrepagoBD-", "GODIGO-"),
            str(div_path[14]).replace("GODIGO", "").replace("GODIG", ""))
        change1 = "logs_CD/cambiar.txt"
        change1by = "logs_CD/logs_UAT_{}.txt".format(div_path[10])
        # change1by = "logs_CD/logs_UAT_{}_{}.txt".format(div_path[8], str(div_path[14]))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "apliacion_base"
    change4by = apliacionyml

    pipeline = readTXT("resources/Fenix_Rollback(UAT).txt")
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


def UATSteps(div_path, componente):
    nombre_app = "APP-JbossComunitario-" + str(div_path[8]).replace("APP-", "") + "/" + str(div_path[14]).replace("%20",
                                                                                                                  "")
    nombre_app = "APP-OSB12C" + str(div_path[9]).replace("APP-", "-")
    # nombre_app = div_path[8]
    print(nombre_app)
    print(componente)
    semilla = str(div_path[14]).replace("%20", "").replace("Semilla", "")

    change1 = "logs_CD/cambiar.txt"
    # change1by = "logs_CD/Promociones_UAT_{}.txt".format(
    #     str(div_path[8]).replace("APP-", "").replace("BD-", "").replace("Promociones-", ""))
    change1by = "logs_CD/log_UAT_OSB12C_{}.txt".format(
        str(div_path[9]).replace("APP-", "").replace("BD-", ""))
    print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "componente_EAR"
    change4by = componente
    change5 = "cambiar.sh "
    if "7" in semilla:
        change5by = "Jboss.sh"
    else:
        change5by = f"JbossS{semilla}.sh"
        print(change5by)

    pipeline = readTXT("resources/Pipeline_Deploy_Prod(OSB_WL_12C).txt")
    new_pipeline = []
    i = 0
    for line in pipeline:
        if change5 in line and change1 in line:
            new_pipeline.append(line.replace(change5, change5by).replace(change1, change1by))
        elif change1 in line and change2 in line:
            new_pipeline.append(line.replace(change2, change2by).replace(change1, change1by))
        elif change2 in line:
            new_pipeline.append(line.replace(change2, change2by))
        elif change3 in line:
            new_pipeline.append(line.replace(change3, change3by))
        elif change4 in line:
            new_pipeline.append(line.replace(change4, change4by))
        else:
            new_pipeline.append(line)
        i += 1

    w = cleanSpecialCharacter(new_pipeline)
    cp.copy(w)


def jenkinsPipelineC(rutaArchivoEjecutar, guardarCambio=True, addparameter=0):
    i = 0
    data = readCSV(rutaArchivoEjecutar)
    urls = []
    componente = []
    for d in data:
        componente.append(d[0])
        urls.append(d[1])
    segunda = 0
    try:
        url_home = "http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/UIPath-Pipelie/configure"

        browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

        browser.get(url_home)
        browser.maximize_window()
        browser.implicitly_wait(10)

        wait = WebDriverWait(browser, 10)
        assert 'Sign in [Jenkins]' in browser.title

        # se realiza el login en jenkins
        username = browser.find_element(By.ID, 'j_username')
        username.send_keys('opauttri')

        password = browser.find_element(By.NAME, "j_password")
        password.send_keys("Tigo.2023#odp*")
        sleep(2)
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

            if "UAT" in u:
                div_path = u.split("/")
                print(div_path, componente[i])
                UATSteps(div_path, componente[i])

            elif "Preproduccion" in u:
                div_path = u.split("/")
                print(div_path, componente[i])
                preproductionSteps(div_path, componente[i])

            elif "Produccion" in u:
                div_path = u.split("/")
                print(div_path, componente[i])
                productionSteps(div_path, componente[i])

            # browser.get("http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/Hola%20mundo/configure")
            sleep(1)
            browser.execute_script("window.scrollTo(0, 600)")
            sleep(1)

            # agregar parametro

            if addparameter == 1:
                print("[+] agregando parametro")
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
            # sleep(1)
            # browser.refresh()
            sleep(2)
            # se espera a que aparesca el tab de pipeline
            print("titulo pipeline")

            tabPipeline = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[text()='Pipeline'])[1]")))
            tabPipeline.click()
            sleep(1)
            # se hace click el el cuadrop de texto, se selecciona todo con ctrl+a y se borra todo
            scriptPipeline = browser.find_element(By.XPATH, "//div[@class='ace_content']")
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

            # se guardan los cambios

            if guardarCambio:
                btnSave = browser.find_element(By.XPATH,
                                               "/html[1]/body[1]/div[6]/div[1]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[217]/td[1]/div[2]/div[2]/span[1]/span[1]")
                action.move_to_element(btnSave).click().perform()

            sleep(2)
            i += 1
            segunda = 0

    except Exception as e:
        print(e)
        browser.quit()

    browser.quit()


def createJob(archivoJobs, copyfrom=""):
    urls = readCSV(archivoJobs)

    url_home = "http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/UIPath-Pipelie/configure"

    browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

    browser.get(url_home)
    browser.maximize_window()
    browser.implicitly_wait(10)

    wait = WebDriverWait(browser, 10)
    assert 'Sign in [Jenkins]' in browser.title

    # se realiza el login en jenkins
    username = browser.find_element(By.ID, 'j_username')
    username.send_keys('lgarcimo')

    password = browser.find_element(By.NAME, "j_password")
    password.send_keys('TIGO#Lau.Gar.22')

    btnSingIn = browser.find_element(By.NAME, 'Submit')
    btnSingIn.click()

    for url in urls:
        u = str(url).replace("[", "").replace("]", "").replace("'", "")
        browser.get(u)

        div_path = u.split("/")
        print(div_path)

        nombreJob = div_path[8] + "-Deploy_Master" if "Produccion" in div_path else div_path[8] + "-Deploy_Test"

        # realiza la creacion del Job
        try:
            carpetaVacia = browser.find_element(By.XPATH, "//h1[contains(.,'¡Bienvenido a Jenkins!')]")
            if (carpetaVacia.is_displayed()):
                print(carpetaVacia.is_displayed())
                btnNewItem = browser.find_element(By.XPATH, "//a[contains(., 'New Item')]")
                btnNewItem.click()

                inputName = browser.find_element(By.ID, "name")
                inputName.send_keys(nombreJob)

                inputCopyFrom = browser.find_element(By.ID, "from")
                inputCopyFrom.send_keys(copyfrom,
                                        Keys.TAB)

                btnOK = wait.until(
                    EC.element_to_be_clickable((By.ID, "ok-button")))  # browser.find_element(By.ID, "ok-button")
                btnOK.click()
                sleep(2)
                btnSave = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Guardar')]")))
                btnSave.click
                sleep(2)
        except Exception as e:
            print(e)
            print("La carpeta no esta vacia")
            continue


def config_logs():
    logging.basicConfig(filename="./urls.log", filemode='w', format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def copyFolder(archivoJobs, copyFrom, folderName, rename=False):
    urls = readCSV(archivoJobs)

    url_home = "http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/UIPath-Pipelie/configure"

    browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

    browser.get(url_home)
    browser.maximize_window()
    browser.implicitly_wait(10)

    wait = WebDriverWait(browser, 10)
    assert 'Sign in [Jenkins]' in browser.title

    # se realiza el login en jenkins
    username = browser.find_element(By.ID, 'j_username')
    username.send_keys('opauttri')

    password = browser.find_element(By.NAME, "j_password")
    password.send_keys('Tigo.2023#odp*')

    btnSingIn = browser.find_element(By.NAME, 'Submit')
    btnSingIn.click()

    for url in urls:
        num = 1;
        # for i in range(1):# cambiar range por el numero de semillas a copiar
        u = str(url).replace("[", "").replace("]", "").replace("'", "")
        browser.get(u)

        div_path = u.split("/")
        print(div_path)

        # nameFolder = "Semilla " + str(num)
        nameFolder = folderName
        btnNewItem = browser.find_element(By.XPATH, "//a[contains(., 'New Item')]")
        btnNewItem.click()

        inputName = browser.find_element(By.ID, "name")
        inputName.send_keys(nameFolder)

        inputCopyFrom = browser.find_element(By.ID, "from")
        inputCopyFrom.send_keys(copyFrom,
                                Keys.TAB)

        btnOK = wait.until(
            EC.element_to_be_clickable((By.ID, "ok-button")))  # browser.find_element(By.ID, "ok-button")
        btnOK.click()
        sleep(1)
        # btnSave = wait.until(EC.element_to_be_clickable((By.ID, "yui-gen30-button")))
        # btnSave.click
        if (rename == True):
            url_rename = f"http://10.100.82.238:8080/job/Accenture-T2/job/APP-CRM-PORTAL/job/{div_path[8]}/job/Operaciones/job/UAT/job/Semilla%20{num}/job/APP-OSB11g-AvailableServices-Deploy-Test/confirm-rename"
            logging.info(url_rename)
            browser.get(url_rename)
            inputName = browser.find_element(By.XPATH, "//input[@name='newName']")
            jobName = f"APP-JbossComunitario-{div_path[8].replace('APP-', '')}-Deploy-Test"
            inputName.clear()
            inputName.send_keys(jobName)
            sleep(3)
            btnRename = browser.find_element(By.ID, "yui-gen1-button")
            btnRename.click()
            num += 1


def deleteFolder(archivoJobs):
    urls = readCSV(archivoJobs)

    url_home = "http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/UIPath-Pipelie/configure"

    browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

    browser.get(url_home)
    browser.maximize_window()
    browser.implicitly_wait(10)

    wait = WebDriverWait(browser, 10)
    assert 'Sign in [Jenkins]' in browser.title

    # se realiza el login en jenkins
    username = browser.find_element(By.ID, 'j_username')
    username.send_keys('lgarcimo')

    password = browser.find_element(By.NAME, "j_password")
    password.send_keys('TIGO#Lau.Gar.23')

    btnSingIn = browser.find_element(By.NAME, 'Submit')
    btnSingIn.click()

    for url in urls:
        num = 1;
        # for i in range(1):# cambiar range por el numero de semillas a copiar
        u = str(url).replace("[", "").replace("]", "").replace("'", "")
        browser.get(u)

        div_path = u.split("/")
        print(div_path)

        sleep(1)
        btnDelete = browser.find_element(By.ID, "yui-gen1-button")
        btnDelete.click()


def jenkinsPipeline(addparameter=0, guardarCambio=True):
    i = 0
    urls = readCSV("resources/archivosdeEjecucion/ejecutarFenix.csv")
    segunda = 0
    try:
        url_home = "http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/UIPath-Pipelie/configure"

        browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

        browser.get(url_home)
        browser.maximize_window()
        browser.implicitly_wait(10)

        wait = WebDriverWait(browser, 10)
        assert 'Sign in [Jenkins]' in browser.title

        # se realiza el login en jenkins
        username = browser.find_element(By.ID, 'j_username')
        username.send_keys('lgarcimo')

        password = browser.find_element(By.NAME, "j_password")
        password.send_keys('TIGO#Lau.Gar.23')

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

            if "UAT" in u:
                div_path = u.split("/")
                print(div_path)
                UATStep(div_path)

            elif "Preproduccion" in u:
                print("mal mal")
                div_path = u.split("/")
                print(div_path)
                # productionSteps(div_path)

            elif "Produccion" in u:
                div_path = u.split("/")
                print(div_path)
                productionStep(div_path)

            # browser.get("http://10.100.82.238:8080/job/DevOps/job/DevOps%20AM/job/Hola%20mundo/configure")
            sleep(1)
            browser.execute_script("window.scrollTo(0, 600)")
            sleep(1)

            # agregar parametro

            if addparameter == 1:
                print("[+] agregando parametro")
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
            # se espera a que aparesca el tab de pipeline
            tabPipeline = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[text()='Pipeline'])[1]")))
            tabPipeline.click()
            sleep(1)
            # se hace click el el cuadrop de texto, se selecciona todo con ctrl+a y se borra todo
            scriptPipeline = browser.find_element(By.XPATH, "//div[@class='ace_content']")
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

            # se guardan los cambios
            if guardarCambio:
                btnSave = browser.find_element(By.XPATH,
                                               "/html[1]/body[1]/div[6]/div[1]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[217]/td[1]/div[2]/div[2]/span[1]/span[1]")
                action.move_to_element(btnSave).click().perform()

                sleep(2)
            i += 1
            segunda = 0

    except Exception as e:
        print(e)
        browser.quit()

    browser.quit()


def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}:{minutos}:{segundos}"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inicio = time.time()
    print("Inicia la ejecucion ")
    print("\n")
    config_logs()
    jenkinsPipelineC("resources/archivosdeEjecucion/ejecutar_componentes.csv")
    # jenkinsPipeline("resources/archivosdeEjecucion/ejecutarFenix.csv")
    # copyFolder("resources/archivosdeEjecucion/newFolder.cvs", "/DevOps/DevOps AM/Operaciones/Produccion", "Produccion")
    # deleteFolder("resources/archivosdeEjecucion/newFolder.cvs")
    fin = time.time()
    print("Finaliza la ejecucion")
    print("\n")
    print(" *******  Tiempo de ejecución:  *******")
    min = (fin - inicio)
    tiempo = segundos_a_segundos_minutos_y_horas(min)

    print(tiempo)
