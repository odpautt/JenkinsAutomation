import logging
import time
from telnetlib import EC
from time import sleep

import clipboard as cp
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ModificarPipelinesMasivo import config_logs
from ModificarPipelinesMasivo import readCSV, segundos_a_segundos_minutos_y_horas, readTXT, cleanSpecialCharacter


def rename_pipelines(archivoJobs):
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
    password.send_keys('Tigo.2023#odpr*')

    btnSingIn = browser.find_element(By.NAME, 'Submit')
    btnSingIn.click()


    for url in urls:
        u = str(url).replace("[", "").replace("]", "").replace("'", "")
        browser.get(u)  # abre la url en el navegador
        # divide la url en partes
        div_path = u.split("/")
        print(div_path)

        inputName = browser.find_element(By.XPATH, "//input[@name='newName']")
        #jobName = div_path[16].replace("Activacionescrm", div_path[8].replace("APP-",
        #                                                                   ""))  # .replace("Desarrollo", "Releasecandidate"). replace("Preproduccion", "Master")
        jobName = "Sostenibilidad-Frontend"
        inputName.clear()
        inputName.send_keys(jobName)
        sleep(3)
        btnRename = browser.find_element(By.ID, "yui-gen1-button")
        btnRename.click()
        sleep(3)


def renameFolder(archivoJobs):
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
    subFolders = ["Sostenibilidad-Backend", "Sostenibilidad-EAP", "Sostenibilidad-Financiacion"]
    semillasFolders = [1, 7, 8, 9, 10, 11]

    for url in urls:
        num = 1;
        # for i in range(1):# cambiar range por el numero de semillas a copiar
        u = str(url).replace("[", "").replace("]", "").replace("'", "")
        browser.get(u)

        div_path = u.split("/")
        print(div_path)
        for folder in subFolders:
            for semilla in semillasFolders:
                print("\n" + folder + " - Semilla " + str(semilla))
                # url_rename = f"http://10.100.82.238:8080/job/Accenture-T2/job/APP-CRM-PORTAL/job/{div_path[8]}/job/Operaciones/job/UAT/job/Semilla%20{num}/job/APP-OSB11g-AvailableServices-Deploy-Test/confirm-rename"
                url_rename = f"http://10.100.82.238:8080/job/Accenture-T2/job/APP-CRM-Sostenibilidad/job/{div_path[8]}/job/Operaciones/job/UAT/job/{folder}/job/Semilla%20{semilla}/job/APP-CRM-Portal-Sostenibilidad-Activacionescrm-Deploy-Test/confirm-rename"
                logging.info(url_rename)
                browser.get(url_rename)
                inputName = browser.find_element(By.XPATH, "//input[@name='newName']")
                jobName = f"APP-CRM-Portal-Sostenibilidad-{div_path[8].replace('APP-', '')}-Deploy-Test"
                inputName.clear()
                inputName.send_keys(jobName)
                sleep(3)
                btnRename = browser.find_element(By.ID, "yui-gen1-button")
                btnRename.click()
                sleep(3)

                # para el pipelines del RollBack
                url_rename = f"http://10.100.82.238:8080/job/Accenture-T2/job/APP-CRM-Sostenibilidad/job/{div_path[8]}/job/Operaciones/job/UAT/job/{folder}/job/Semilla%20{semilla}/job/APP-CRM-Portal-Sostenibilidad-Activacionescrm-Rollback-Test/confirm-rename"
                logging.info(url_rename)
                browser.get(url_rename)
                inputName = browser.find_element(By.XPATH, "//input[@name='newName']")
                jobName = f"APP-CRM-Portal-Sostenibilidad-{div_path[8].replace('APP-', '')}-Rollback-Test"
                inputName.clear()
                inputName.send_keys(jobName)
                sleep(3)
                btnRename = browser.find_element(By.ID, "yui-gen1-button")
                btnRename.click()

                num += 1


def productionSteps(div_path, componente,  ruta_despliegue):
    nombre_app = str(div_path[6]) + str(div_path[8]).replace("APP-", "-")
    print(nombre_app)
    print(componente)

    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/Sostenibilidad_Prod_{}.txt".format(
        str(div_path[8]).replace("APP-", "").replace("BD-", "").replace("Promociones-", ""))
    # print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "componente_jar_war"
    change4by = componente
    change5 = "semilla_cambio"
    change5by = "Backend"
    change6 = "ruta_despligue"
    change6by = ruta_despliegue
    pipeline = readTXT("resources/Pipeline_Deploy_Prod(Jboss Sostenibilidad).txt")
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
        elif change6 in line:
            new_pipeline.append(line.replace(change6, change6by))
        else:
            new_pipeline.append(line)

    w = cleanSpecialCharacter(new_pipeline)
    cp.copy(w)


def UATSteps(div_path, componente, ruta_despliegue):
    nombre_app = str(div_path[6]) + str(div_path[8]).replace("APP-", "-")

    print(nombre_app)
    print(componente)
    print(ruta_despliegue)
    semilla = str(div_path[16]).replace("%20", "").replace("Semilla", "")

    change1 = "logs_CD/cambiar.txt"
    change1by = "logs_CD/log_UAT_{}_{}_S{}.txt".format(str(div_path[8]).replace("APP-", "_"), str(div_path[14]),
                                                       semilla)
    print(change1by)
    change2 = "cambiar.txt"
    change2by = change1by.replace("logs_CD/", "")
    # print(change2by)
    change3 = "nombre_base_aplicacion"
    change3by = nombre_app
    change4 = "componente_jar_war"
    change4by = componente
    change5 = "semilla_cambio"
    change5by = "Semilla" + semilla
    change6 = "ruta_despligue"
    change6by = ruta_despliegue
    # if "Backend" in div_path[14]:
    #     change5by = "Jboss.sh"
    # elif "EAP" in div_path[14]:
    #     change5by = ""
    # else:
    #     change5by = "JbossS{semilla}.sh"
    # print(change5by)

    pipeline = readTXT("resources/Pipeline_Deploy_UAT(Jboss Sostenibilidad).txt")
    new_pipeline = []
    i = 0
    for line in pipeline:
        # if change5 in line and change1 in line:
        #     new_pipeline.append(line.replace(change5, change5by).replace(change1, change1by))
        if change1 in line and change2 in line:
            new_pipeline.append(line.replace(change2, change2by).replace(change1, change1by))
        elif change2 in line:
            new_pipeline.append(line.replace(change2, change2by))
        elif change3 in line:
            new_pipeline.append(line.replace(change3, change3by))
        elif change4 in line:
            new_pipeline.append(line.replace(change4, change4by))
        elif change5 in line:
            new_pipeline.append(line.replace(change5, change5by))
        elif change6 in line:
            new_pipeline.append(line.replace(change6, change6by))
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
    ruta_deploy = []
    for d in data:
        componente.append(d[0])
        urls.append(d[1])
        ruta_deploy.append(d[2])

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
        password.send_keys("Tigo.2023#odpr*")
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
                UATSteps(div_path, componente[i], ruta_deploy[i])

            elif "Produccion" in u:
                div_path = u.split("/")
                print(div_path, componente[i])
                productionSteps(div_path, componente[i], ruta_deploy[i])

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
                name.send_keys("BUILD_MASTER")
            # sleep(1)
            # browser.refresh()
            sleep(2)
            # se espera a que aparesca el tab de pipeline
            print("titulo pipeline")

            tabPipeline = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Pipeline')])[9]")))
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


if __name__ == '__main__':
    inicio = time.time()
    print("Inicia la ejecucion ")
    print("\n")
    config_logs()
    # renameFolder("resources/archivosdeEjecucion/newFolder.cvs")
    # jenkinsPipelineC("resources/archivosdeEjecucion/ejecutar_componentes.csv")
    rename_pipelines("resources/archivosdeEjecucion/newFolder.cvs")
    fin = time.time()
    print("Finaliza la ejecucion")
    print("\n")
    print(" *******  Tiempo de ejecución:  *******")
    min = (fin - inicio)
    tiempo = segundos_a_segundos_minutos_y_horas(min)

    print(tiempo)
