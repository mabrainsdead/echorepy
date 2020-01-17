#!/usr/bin/env python3


''' Import.py eh o script de importacao de objetos dicom da do aparelho de eco '''


#modulos do sistema
import sys, os, pydicom, time
from datetime import datetime, date
from django.conf import settings
from shutil import copyfile, rmtree
#import pymysql.cursors

#modulos locais
from funcoes import  logger, getTag, dcmToMp4, dcmToJpg, dcm2xml #dcmdump, ageCalculator, 
from constantes import LOGSFILE, DCMTEMP, DCMRECEIVED


######### Define caminhos para Instaciar o DataSet
logger("I: Iniciando importacao do estudo..")

dcmFile = sys.argv[1] if sys.argv[1] else ''  #define o nome do arquivo recebido

ds = pydicom.dcmread(DCMTEMP + "/" + dcmFile) #instancia objeto dicom

studyDate = datetime.strptime(ds.StudyDate, "%Y%m%d") #importa a data do estudo

estudoDirDestino = DCMRECEIVED + str(studyDate.year) + "/" + str(studyDate.month)  +"/" + str(studyDate.day) + "/" + str(ds.StudyInstanceUID) +"/" #Criar diretorio onde sera armazenado o estudo


######## Transfere os arquivos do diretorio temporario para o definitivo

### o diretorio definitivo nao existe - Situacao na qual a primeira imagem e enviada. 

if not os.path.exists(estudoDirDestino):
    os.makedirs(estudoDirDestino)  #cria o diretorio em received se ele nao existir    
    os.chmod(estudoDirDestino, 0o755) #define permissões no diretório
    copyfile(DCMTEMP + "/" + dcmFile, estudoDirDestino + dcmFile) #Copiar arquivo do diretorio temporario para o definitivo
    ########## Inicia processamento do arquivo
    
    if getTag(ds, '0028', '0008'): # Checa se o arquivo é vídeo
        try:
            os.makedirs(estudoDirDestino + "/" + "mp4")
            dcmToMp4(dcmFile,  estudoDirDestino + "mp4")
            if os.path.exists(estudoDirDestino + "/" + "mp4/" + dcmFile + ".mp4"):
                logger("I: video dicom convertido para mp4")
            
        except FileExistsError:
            logger("I:8 o diretorio ::'" + estudoDirDestino +"mp4' ::: já existe")
            
            
    elif getTag(ds, '0008', '0060') == "SR": #se o arquivo for um laudo estruturado, nao faz nada.
        #logger("I: O arquivo " + dcmFile + " e um laudo estruturado")
        os.makedirs(estudoDirDestino + "sr")
        #logger("I: diretorio '" + folder + "sr' criado com sucesso")
        dcm2xml(DCMTEMP + "/" + dcmFile, estudoDirDestino)
        logger("I:9 aquivo de laudo estruturado foi importado com sucesso")
         
    else:
        try:
            os.makedirs(estudoDirDestino + "/" + "jpeg", 0o755) #cria diretorio para fotos em png
            #os.chmod(estudoDirDestino + "/" + "jpeg", 0o755)
            dcmToJpg(dcmFile, estudoDirDestino + "jpeg/" + dcmFile + ".jpeg") #grava os arquivos em jpeg
            if os.path.exists(estudoDirDestino + "jpeg/" + dcmFile + ".jpeg"):
                logger("I: Arquivo DICOM convertido com sucesso!")
            #os.chmod(estudoDirDestino + "jpeg/" + dcmFile + ".jpeg", 0o777)
           
        except Exception as e: logger("\nE: " + str(e) + "\n")
    
    
###  O diretorio definitivo existe - Situacao na qual mais de uma imagem eh enviada.  
else: 
    copyfile(DCMTEMP + "/" + dcmFile, estudoDirDestino + dcmFile) #Copiar arquivo do diretorio temporario para o definitivo
    


