import os,sys
import pandas as pd
import selenium
from selenium import webdriver
import shutil
import random
import zipfile

target1 = input("Target1?  ")
target2 = input("Target2?  ")
target3 = input("Target3?  ")
target4 = input("Target4?  ")
target5 = input("Target5?  ")
target6 = input("Target6?  ")
target7 = input("Target7?  ")
target8 = input("Target8?  ")
target9 = input("Target9?  ")
target10 = input("Target10?  ")

Allele1 = input("Allele MHCI?  ")
Allele2 = input("Allele MHCII?  ")

TmMHCI = input("MHCI Lenght Epitopes?  ")
TmMHCII = input("MHCII Lenght Epitopes?  ")


PERRANK1 = ""
IC50_1 = ""
PERRANK2 = ""
IC50_2 = ""



def GetParams(string,list):
	i = list.index(string)
	return list[i+1]

cmds = sys.argv
try:
	if "-h" not in cmds:
		PERRANK1 = GetParams("-P1",cmds)
		PERRANK2 = GetParams("-P2",cmds)
		IC50_1 = GetParams("-I1",cmds)
		IC50_2 = GetParams("-I2",cmds)
		  	
	elif "-h" in cmds:
		print(
"""
""")
		sys.exit(0)
except:
	print("ERROR ")
	sys.exit(0)

Pcr1 = int(PERRANK1)
Pcr2 = int(PERRANK2)
Ic50_1 = int(IC50_1)
Ic50_2 = int(IC50_2)

lista = [target1,target2,target3,target4,target5,target6,target7,target8,target9,target10]
for x1 in lista:
    if x1 != "":
        print('\n',x1, "It's one of your targets.\n\n")

for x in lista:
    if x != "":
        with open(x) as f:
            content = " ".join([l.rstrip() for l in f])
            sequenciafinal = content.replace(" ", "")
        #AlelosMHCI:
        with open(Allele1) as alelinhos:
            content1 = " ".join([a.rstrip() for a in alelinhos])
            alelosfinais = content1.replace(" ", ",")
        #TamanhoDosEpítopos:
        TamanhoDoEpitopo = TmMHCI + ","        
        #Verificação da quantidade de alelos
        Contagem = [line.rstrip('\n') for line in open(Allele1)]
        new_list = [TamanhoDoEpitopo for x in Contagem]
        QuantidadeDeAlelosBETA = "".join(new_list)
        #Retirando a ultima virgula desnecessária
        QuantidadeDeAlelosMHCI = QuantidadeDeAlelosBETA[:-1]
        #AlelosMHCII:
        with open(Allele2) as alelinhos2:
            contentMHCII = " ".join([D.rstrip() for D in alelinhos2])
            alelosfinaisMHCII = contentMHCII.replace(" ", ",")
        #TamanhoDosEpítopos:
        TamanhoDoEpitopoMHCII = TmMHCII + ","
        #Verificação da quantidade de alelos
        ContagemMHCII = [lineMHCII.rstrip('\n') for lineMHCII in open(Allele2)]
        new_listMHCII = [TamanhoDoEpitopoMHCII for y in ContagemMHCII]
        QuantidadeDeAlelosBETAMHCII = "".join(new_listMHCII)
        #Retirando a ultima virgula desnecessária
        QuantidadeDeAlelosMHCII = QuantidadeDeAlelosBETAMHCII[:-1]
        #Junção dos comandos, comando + sequencia + comando parte 2, para rodar no os.system, sendo Sequencia, o alvo que vai ser predito os epitopos
        print(" \n Initializing Predictions \n")
        comando = 'curl --data "method=recommended&sequence_text='
        comando1 = '&allele='
        comando2 = '&length='
        comando3 = 'http://tools-cluster-interface.iedb.org/tools_api/mhci/ > IEDBmhci.txt'
        comando4 = 'http://tools-cluster-interface.iedb.org/tools_api/mhcii/ > IEDBmhcii.txt'
        NETmhciMET = 'curl --data "method=netmhccons&sequence_text='
        NETmhciiMET = 'curl --data "method=nn_align&sequence_text='
        NETmhciBUSC = 'http://tools-cluster-interface.iedb.org/tools_api/mhci/ > NETmhci.txt'
        NETmhciiBUSC = 'http://tools-cluster-interface.iedb.org/tools_api/mhcii/ > NETmhcii.txt'
        #Final é o comando que vai rodar no prompt!! rodamos com os.sys
        #IEDBmhci
        IEDBmhciFINAL = comando + sequenciafinal + comando1 + alelosfinais + comando2 + QuantidadeDeAlelosMHCI + '" ' + comando3
        print(IEDBmhciFINAL)
        teste = os.system(IEDBmhciFINAL)
        #NETmhci
        NETmhciFINAL = NETmhciMET + sequenciafinal + comando1 + alelosfinais + comando2 + QuantidadeDeAlelosMHCI + '" ' + NETmhciBUSC
        print(NETmhciFINAL)
        teste = os.system(NETmhciFINAL)
        #Transformando em arquivo csv!
        abrirNETmhci = pd.read_csv("NETmhci.txt", sep="	")
        abrirNETmhci.to_csv('NETmhci.csv',  
                         index = None)
        os.remove("NETmhci.txt")
        #Transformando em arquivo csv!
        abrir = pd.read_csv("IEDBmhci.txt", sep="	")
        abrir.to_csv('IEDBmhci.csv',  
                        index = None)
        os.remove("IEDBmhci.txt")
        IEDBmhciiFINAL = comando + sequenciafinal + comando1 + alelosfinaisMHCII + comando2 + QuantidadeDeAlelosMHCII + '" ' + comando4
        print(IEDBmhciiFINAL)
        teste = os.system(IEDBmhciiFINAL)

        NETmhciiFINAL = NETmhciiMET + sequenciafinal + comando1 + alelosfinaisMHCII + comando2 + QuantidadeDeAlelosMHCII + '" ' + NETmhciiBUSC
        print(NETmhciiFINAL)
        teste = os.system(NETmhciiFINAL)
        #Transformando em arquivo csv!
        abrirNETmhcii = pd.read_csv("NETmhcii.txt", sep="	")
        abrirNETmhcii.to_csv('NETmhcii.csv',  
                          index = None)
        os.remove("NETmhcii.txt")
        #Transformando em arquivo csv!
        abrirIEDBmhcii = pd.read_csv("IEDBmhcii.txt", sep="	")
        abrirIEDBmhcii.to_csv('IEDBmhcii.csv',  
                          index = None)
        os.remove("IEDBmhcii.txt")

        #RODANDO Bcell com selenium - importante ter selenium instalado, e o webdriver do navegador da pessoa 
        print("\n Initializing B cell epitope prediction with ABCpred \n")
        op = webdriver.FirefoxOptions()
        op.add_argument('headless')
        nav = webdriver.Firefox(options=op)
        nav.get("https://webs.iiitd.edu.in/raghava/abcpred/ABC_submission.html")
        nav.find_element_by_xpath('/html/body/form/font/textarea').send_keys(sequenciafinal)
        nav.find_element_by_xpath('/html/body/form/p[2]/input[2]').click()
        tabeladonav = nav.find_element_by_xpath('/html/body/pre[2]/table/tbody')
        lernav = tabeladonav.text
        print(lernav)
        nav.close()
        with open("Bcell0.csv", "w") as f:
            f.writelines(lernav)
        lerBcell = pd.read_csv("Bcell0.csv", sep=" ")
        lerBcell.to_csv('Bcell.csv',  
                          index = None)
        os.remove("Bcell0.csv")

        pasta = "./Targets"
        caminho = "Targets/" + x
        if os.path.isdir("Targets"):
            print("\n\nTransferred Target\n\n")
            os.replace(x, caminho)
        else:
            os.makedirs(pasta)
            os.replace(x, caminho)
        
        ############
        df = pd.read_table("IEDBmhci.csv", sep = ',')
        cortado = df.filter(["allele","peptide","percentile_rank"])
        filtrado = cortado[(cortado["percentile_rank"] <=Pcr1)]
        filtrado.to_csv('IEDBmhc1FIL.csv',  
                          index = None)
        ############
        df1 = pd.read_table("IEDBmhcii.csv", sep = ',')
        tirar = df1.replace('-', 0)
        tirar.to_csv('tirado.csv',  
                      index = None)
        jatirado = pd.read_table("tirado.csv", sep = ',')
        cortado1 = jatirado.filter(["allele","peptide", "percentile_rank","smm_align_ic50","nn_align_ic50","netmhciipan_ic50"])
        filtrado1 = cortado1[(cortado1["percentile_rank"]<Pcr2) & (cortado1["smm_align_ic50"]<Ic50_2) & (cortado1["nn_align_ic50"]<Ic50_2) & (cortado1["netmhciipan_ic50"]<Ic50_2)]
        filtrado1.to_csv('IEDBmhc2FIL.csv',  
                  index = None)
        os.remove('tirado.csv')
        ####################
        NetmhciMODE = pd.read_table("NETmhci.csv", sep = ',')
        cortarNET = NetmhciMODE.filter(["allele","peptide","ic50","percentile_rank"])
        filtragemNET = cortarNET[(cortarNET["ic50"] <Ic50_1) & (cortarNET["percentile_rank"] < Pcr1)]
        duplicate = filtragemNET.drop_duplicates(subset='peptide', keep="first")
        duplicate.to_csv('NETmhc1FIL.csv',  
                          index = None)

        df3 = pd.read_table("NETmhcii.csv", sep = ',')
        cortado3 = df3.filter(["allele","peptide","ic50","rank"])
        filtrado3 = cortado3[(cortado3["ic50"] < Ic50_2) & (cortado3["rank"] < Pcr2)]
        duplicate = filtrado3.drop_duplicates(subset='peptide', keep="first")
        duplicate.to_csv('NETmhc2FIL.csv',  
                          index = None)
        print("\n\nfinished Filtering\n\n")
        #Salvar os arquivos iniciais
        testando = str(x) + "FOLDER"
        Originals = './Originals/'+testando
        CaminhoOriginals = "Originals/"+testando
        if os.path.isdir(Originals):
            print("Transferred Originals")
            os.replace("IEDBmhci.csv", CaminhoOriginals + "/IEDBmhci.csv")
            os.replace("IEDBmhcii.csv", CaminhoOriginals + "/IEDBmhcii.csv")
            os.replace("NETmhci.csv", CaminhoOriginals + "/NETmhci.csv")
            os.replace("NETmhcii.csv", CaminhoOriginals + "/NETmhcii.csv")
        else:
            os.makedirs(Originals)
            os.replace("IEDBmhci.csv", CaminhoOriginals + "/IEDBmhci.csv")
            os.replace("IEDBmhcii.csv", CaminhoOriginals + "/IEDBmhcii.csv")
            os.replace("NETmhci.csv", CaminhoOriginals + "/NETmhci.csv")
            os.replace("NETmhcii.csv", CaminhoOriginals + "/NETmhcii.csv")
        #Etapa 2 - Preparação e Overllap!
        ##############################################################################################################
        """
        Preparação dos arquivos, trocando as colunas peptide por epitopo, e excluindo as demais desnecessárias.
        """
        oldIEDB1 = pd.read_table("IEDBmhc1FIL.csv", sep=',')
        newIEDB1 = oldIEDB1[['peptide']]
        renome = newIEDB1.rename(columns={'peptide': 'epitopo'})
        renome.to_csv('IEDBepi1.csv',  
                          index = None)
        oldNET1 = pd.read_table("NETmhc1FIL.csv", sep=',')
        newNET1 = oldNET1[['peptide']]
        renome1 = newNET1.rename(columns={'peptide': 'epitopo'})
        renome1.to_csv('NETepi1.csv',  
                        index = None)
        ##########################################
        #primeiro overlap de MHC1 NET x IEDB
        exec(open("epitopo1.py").read())
        ##########################################
        ###########################################################################################################
        #Salvar resultados
        mhc1 = './Overlapping/mhc1/' +testando
        os.makedirs(mhc1)
        mhc2 = './Overlapping/mhc2/' +testando
        os.makedirs(mhc2)
        Bcell = './Overlapping/Final/' +testando
        os.makedirs(Bcell)
        Overlap_MHC1_MHC2 = './Overlapping/OverlappingMHCI&MHCII' +testando
        os.makedirs(Overlap_MHC1_MHC2)
        EpitoposPASTA = './Epitopes/' +testando
        os.makedirs(EpitoposPASTA)
        src=r'IEDBepi1.csv_NETepi1.csv_9_out.txt'
        des=r'IEDBepi1xNETepi19.csv'
        shutil.copy(src, des)

        os.replace("IEDBepi1.csv_NETepi1.csv_9_out.txt", mhc1 + "/IEDBepi1.csv_NETepi1.csv_9_out.csv")
        os.replace("IEDBepi1.csv_NETepi1.csv_8_out.txt", mhc1 + "/IEDBepi1.csv_NETepi1.csv_8_out.csv")
        os.replace("IEDBepi1.csv_NETepi1.csv_7_out.txt", mhc1 + "/IEDBepi1.csv_NETepi1.csv_7_out.csv")
        os.remove("IEDBepi1.csv_NETepi1.csv_6_out.txt")
        os.remove("IEDBepi1.csv_NETepi1.csv_5_out.txt")
        os.remove("IEDBepi1.csv_NETepi1.csv_4_out.txt")
        os.remove("IEDBepi1.csv_NETepi1.csv_3_out.txt") 
        os.remove("IEDBepi1.csv_NETepi1.csv_2_out.txt")

        os.replace("IEDBepi1.csv", EpitoposPASTA + "/IEDBepi1.csv")
        os.replace("NETepi1.csv", EpitoposPASTA + "/NETepi1.csv")
        print("Finished MHCI x MHCI Overlapping\n\n")

        #Segundo overlap de MHC1 NET x IEDB
        ##################################################################################################
        oldIEDB2 = pd.read_table("IEDBmhc2FIL.csv", sep=',')
        newIEDB2 = oldIEDB2[['peptide']]
        renome3 = newIEDB2.rename(columns={'peptide': 'epitopo'})
        renome3.to_csv('IEDBepi2.csv',  
                          index = None)
        oldNET2 = pd.read_table("NETmhc2FIL.csv", sep=',')
        newNET2 = oldNET2[['peptide']]
        renome4 = newNET2.rename(columns={'peptide': 'epitopo'})
        renome4.to_csv('NETepi2.csv',  
                          index = None)
        print("Finished MHCII x MHCII Overlapping\n\n")
        ########################################
        exec(open("epitopo2.py").read())
        ########################################
        ###################################################################################################
        src1=r'IEDBepi2.csv_NETepi2.csv_15_out.txt'
        des1=r'IEDBepi2xNETepi215.csv'
        shutil.copy(src1, des1)
        os.replace("IEDBepi2.csv_NETepi2.csv_15_out.txt", mhc2 + "/IEDBepi2.csv_NETepi2.csv_15_out.csv")
        os.replace("IEDBepi2.csv_NETepi2.csv_14_out.txt", mhc2 + "/IEDBepi2.csv_NETepi2.csv_14_out.csv")
        os.replace("IEDBepi2.csv_NETepi2.csv_13_out.txt", mhc2 + "/IEDBepi2.csv_NETepi2.csv_13_out.csv")
        os.remove("IEDBepi2.csv_NETepi2.csv_12_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_11_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_10_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_9_out.txt") 
        os.remove("IEDBepi2.csv_NETepi2.csv_8_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_7_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_6_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_5_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_4_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_3_out.txt")
        os.remove("IEDBepi2.csv_NETepi2.csv_2_out.txt")

        os.replace("IEDBepi2.csv", "Epitopes/IEDBepi2.csv")
        os.replace("NETepi2.csv", "Epitopes/NETepi2.csv")
        #####################################################################################################
        #Salva os arquivos filtrados
        Filtered = './Filtered/' +testando
        os.makedirs(Filtered)
        os.replace("IEDBmhc1FIL.csv", Filtered + "/IEDBmhc1FIL.csv")
        os.replace("IEDBmhc2FIL.csv", Filtered + "/IEDBmhc2FIL.csv")
        os.replace("NETmhc2FIL.csv", Filtered + "/NETmhc2FIL.csv")
        os.replace("NETmhc1FIL.csv", Filtered + "/NETmhc1FIL.csv")
        #preparando arquivos finais para ultimo overlapping contra celula B
        #Bcell1 - prepara arquivo do overlap de MHC1

        Bcell1 = pd.read_table("IEDBepi1xNETepi19.csv", sep = ',')
        Preparado1 = Bcell1[["epitope_1"]]
        dups1 = Preparado1.drop_duplicates(subset='epitope_1', keep="first")
        renomear = dups1.rename(columns={'epitope_1': 'epitopo'})
        renomear.to_csv('MHC1overlap.csv',  
                          index = None)

        #Bcell2 - prepara arquivo do overlap de MHC2
        Bcell2 = pd.read_table("IEDBepi2xNETepi215.csv", sep = ',')
        Preparado2 = Bcell2[["epitope_1"]]
        dups2 = Preparado2.drop_duplicates(subset='epitope_1', keep="first")
        renomear1 = dups2.rename(columns={'epitope_1': 'epitopo'})
        renomear1.to_csv('MHC2overlap.csv',  
                          index = None)

        os.replace("IEDBepi1xNETepi19.csv", Overlap_MHC1_MHC2 + "/IEDBepi1xNETepi1_tm9.csv")
        os.replace("IEDBepi2xNETepi215.csv", Overlap_MHC1_MHC2 + "/IEDBepi2xNETepi2_tm15.csv")
        #BcellREAL prepara os epitopos de célula B para o overlapping final
        BcellREAL = pd.read_table("Bcell.csv", sep = ',')
        Colunar = BcellREAL[["Sequence"]]
        renomear2 = Colunar.rename(columns={'Sequence': 'epitopo'})
        temnadak = renomear2.dropna()
        temnadak.to_csv('BcellPrepared.csv',  
                        index = None)
        #Executa o overlapping final 
        exec(open("Bcell9.py").read())
        exec(open("Bcell15.py").read())
        print("Finished Overlapping MHCI x Bcell / MHCII x Bcell of  " + x)
        #limpa as pastas
        LeituraFinal = pd.read_csv("MHC1overlap.csv_BcellPrepared.csv_9_out.txt", sep = ",")
        SelecionandoOsTop = LeituraFinal[["kmer"]]
        DuplicadosTop = SelecionandoOsTop.drop_duplicates(subset='kmer', keep="first")
        DuplicadosTop.to_csv('EpítoposFinaisMHCI'+x+".txt",  
                        index = None)
    

        os.replace("MHC1overlap.csv_BcellPrepared.csv_9_out.txt", Bcell + "/MHC1overlap.csv_BcellPrepared.csv_9_out.csv")
        os.replace("MHC1overlap.csv_BcellPrepared.csv_8_out.txt", Bcell + "/MHC1overlap.csv_BcellPrepared.csv_8_out.csv")
        os.replace("MHC1overlap.csv_BcellPrepared.csv_7_out.txt", Bcell + "/MHC1overlap.csv_BcellPrepared.csv_7_out.csv")
        os.remove("MHC1overlap.csv_BcellPrepared.csv_6_out.txt")
        os.remove("MHC1overlap.csv_BcellPrepared.csv_5_out.txt")
        os.remove("MHC1overlap.csv_BcellPrepared.csv_4_out.txt")
        os.remove("MHC1overlap.csv_BcellPrepared.csv_3_out.txt")
        os.remove("MHC1overlap.csv_BcellPrepared.csv_2_out.txt")
        LeituraFinalMHCII = pd.read_csv("MHC2overlap.csv_BcellPrepared.csv_15_out.txt", sep = ",")
        SelecionandoOsTop2 = LeituraFinalMHCII[["kmer"]]
        DuplicadosTop2 = SelecionandoOsTop2.drop_duplicates(subset='kmer', keep="first")
        DuplicadosTop2.to_csv('EpítoposFinaisMHCII' + x + ".txt",  
                        index = None)
        os.replace("MHC2overlap.csv_BcellPrepared.csv_15_out.txt", Bcell + "/MHC2overlap.csv_BcellPrepared.csv_15_out.csv")
        os.replace("MHC2overlap.csv_BcellPrepared.csv_14_out.txt", Bcell + "/MHC2overlap.csv_BcellPrepared.csv_14_out.csv")
        os.replace("MHC2overlap.csv_BcellPrepared.csv_13_out.txt", Bcell + "/MHC2overlap.csv_BcellPrepared.csv_13_out.csv")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_12_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_11_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_10_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_9_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_8_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_7_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_6_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_5_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_4_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_3_out.txt")
        os.remove("MHC2overlap.csv_BcellPrepared.csv_2_out.txt")

        os.replace("Bcell.csv", CaminhoOriginals + "/Bcell.csv")
        os.remove("MHC1overlap.csv")
        os.remove("MHC2overlap.csv")
        os.replace("BcellPrepared.csv", EpitoposPASTA + "/BcellPrepared.csv")

        search_text11 = "kmer\n"
        replace_text11 = ""
        with open("EpítoposFinaisMHCI"+x+".txt",'r') as file11:
            data11 = file11.read()
            data11 = data11.replace(search_text11, replace_text11)
        with open('EpítoposFinaisMHCI'+x+".txt", 'w') as file12:
            file12.write(data11)
        
        with open("EpítoposFinaisMHCII"+x+".txt", 'r') as file22:
            data22 = file22.read()
            data22 = data22.replace(search_text11, replace_text11)
        with open('EpítoposFinaisMHCII'+x+".txt", 'w') as file22:
            file22.write(data22)

    continue

os.replace(Allele1, "Targets/"+Allele1)
os.replace(Allele2, "Targets/"+Allele2)

os.system("copy *.txt FinalEpitopes.txt")

search_For = ""
replace_for = ""
with open("FinalEpitopes.txt",'r') as fileFINAL:
    dataFINAL = fileFINAL.read()
    dataFINAL = dataFINAL.replace(search_For, replace_for)
with open("FinalEpitopes.txt", 'w') as fileFINAL2:
    fileFINAL2.write(dataFINAL)

import selenium
from selenium import webdriver
import time
MHCinav = webdriver.Firefox()
MHCinav.get("http://tools.iedb.org/immunogenicity/")    
MHCinav.find_element_by_xpath('//*[@id="id_sequence_file"]').send_keys(os.getcwd()+"\FinalEpitopes.txt")
time.sleep(1)
MHCinav.find_element_by_xpath('//*[@id="input-form"]/table/tbody/tr[6]/th/div/input[1]').click()
time.sleep(5)
tabeladoMHCIClass = MHCinav.find_element_by_xpath('//*[@id="result_table"]')
tabeladonavegadorMHCIclass = tabeladoMHCIClass.text
MHCinav.close()
quebradelinha = "Peptide\n"
virgula = "Peptide,"
quebradordelinhas= "Peptide,Length\n"
quebradordelinhas1= "Peptide,Length,"
trocatrocadetxt = " "
trocatrocadnv = ","
with open("FinalEpitopes.txt","w") as finaldosepitops:
    finalizarosepitopos = finaldosepitops.writelines(tabeladonavegadorMHCIclass)
with open("FinalEpitopes.txt","r") as reading:
    finalizadinho = reading.read()
    finalizadinho = finalizadinho.replace(quebradelinha,virgula)
with open("FinalEpitopes.txt", "w") as filepequeno:
    filepequeno.write(finalizadinho)
with open("FinalEpitopes.txt","r") as reading1:
    finalizadinho1 = reading1.read()
    finalizadinho1 = finalizadinho1.replace(quebradordelinhas,quebradordelinhas1)
with open("FinalEpitopes.txt", "w") as filepequeno1:
    filepequeno1.write(finalizadinho1)
with open("FinalEpitopes.txt","r") as reading12:
    finalizadinho12 = reading12.read()
    finalizadinho12 = finalizadinho12.replace(trocatrocadetxt,trocatrocadnv)
with open("FinalEpitopes.txt", "w") as filepequeno12:
    filepequeno12.write(finalizadinho12)

Finish = pd.read_csv("FinalEpitopes.txt",sep=",")
filtradinho = Finish[(Finish["Score"]>0.1)]
focanimim = filtradinho[["Peptide"]]
focanimim.to_csv("FinalEpitopes.txt", header=None, index=None)

Multi_Chimeric = input("How Many Models?  ")
Linker1 = input("Linker MHCI?  ")
Linker2 = input("Linker MHCII?  ")
Adjuvant = input("Adjuvant?  ")


epitopes = open("FinalEpitopes.txt", "r")
linebyline = epitopes.readlines()

resultados = []

for x in linebyline:
    resultados.append(x.replace("\n", ""))
transformar = "".join(resultados)
arquivo = open("FinalEpitopes.txt", "r")
lista = [line.rstrip('\n') for line in open("FinalEpitopes.txt")]

nova_lista = []
nova_lista2 = []
for item in lista:
	if len(item) < 10:
    		nova_lista.append(Linker1 + item)
for item2 in lista:
	if len(item2) > 10:
		nova_lista2.append(item2 + Linker2)


print(" @ NUMBER OF MODELS:", Multi_Chimeric, "\n", "@ THE LINKER FOR MHCI:", Linker1, "\n", "@ THE LINKER FOR MHCII:", Linker2, "\n\n---->  EPITOPES OF 9KMER:\n\n",nova_lista,"\n\n", "---->  EPITOPES OF 15KMER:\n\n",nova_lista2,"\n")

num = int(Multi_Chimeric)
num2 = num - 1
num3 = int(num2)
quimera = (">Chimeric_Protein_Model_")
i = 0
contador = 0
mudar = str(contador)
with open("Chimeric.faa", "w") as novos:
	while contador <= num3:
		contador = contador + 1
		mudar = str(contador)
		random.shuffle(nova_lista)
		StrA = "".join(nova_lista)
		random.shuffle(nova_lista2)
		StrB = "".join(nova_lista2)
		juncao = Adjuvant + StrB + StrA
		print(">CHIMERIC PROTEIN MODEL", mudar,":",".........done", "\n")
		novos.writelines(quimera + mudar + ":\n" + juncao + "\n")


with open(r'Chimeric.faa', 'r') as meuarq:
    data = meuarq.read()
    data = data.replace(Linker2+Linker1, Linker1)

with open(r'Chimeric.faa', 'w') as file:
    file.write(data)

import selenium
from selenium import webdriver
import os, pandas as pd
import numpy as np
import time

navegador10 = webdriver.Firefox()
navegador10.get("http://www.ddg-pharmfac.net/vaxijen/VaxiJen/VaxiJen.html")    
navegador10.find_element_by_xpath("/html/body/div/table/tbody/tr[4]/td[3]/form/table/tbody/tr[1]/td[2]/p/input").send_keys(os.getcwd()+"\Chimeric.faa")
time.sleep(5)
navegador10.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td[3]/form/table/tbody/tr[2]/td[2]/p/input[1]').click()
navegador10.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td[3]/form/table/tbody/tr[2]/td[2]/p/input[3]').click()
navegador10.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td[3]/form/table/tbody/tr[3]/td[2]/input[1]').click()
time.sleep(100)
Leituradonavegador10 = navegador10.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td[3]/table/tbody/tr/td')
lernavegador1 = Leituradonavegador10.text
print(lernavegador1)
navegador10.close()
with open("VaxijenResults.txt", "w") as fumar1:
    fumar1.writelines(lernavegador1)
buscartexto10 = " Overall Protective Antigen Prediction = "
buscartexto101 = " ( Probable ANTIGEN )."
new_text10 = ""
with open("VaxijenResults.txt","r") as trocadetxt:
    dataler10 = trocadetxt.read()
    dataler10 = dataler10.replace(buscartexto10, new_text10)
    dataler10 = dataler10.replace(buscartexto101, new_text10)
with open("VaxijenResults.txt", "w") as filezinho:
    filezinho.write(dataler10)

Vaxijen = pd.read_csv("VaxijenResults.txt",skiprows=1,sep=":")
Vaxijen.columns=["Model","Value"]
Vaxijen.to_csv('Vaxijen.csv',  
                          index = None)
os.remove("VaxijenResults.txt")

VaxFinal = pd.read_csv("Vaxijen.csv",sep=",")
VaxFinal1 = VaxFinal.sort_values(by=["Value"], ascending= False)
VaxModelName = VaxFinal1.filter(["Model"])
VaxModelName.to_csv("Vaxijen.txt", header=False, index = None)

with open("Vaxijen.txt","r") as vaxi:
    firstlineMODEL = vaxi.readline().rstrip()
    NameOfTheTopModel = firstlineMODEL + ":"
    print(NameOfTheTopModel)

antigao = "\n"
novao = ""
with open("Chimeric.faa","r") as trocadetxt1:
    dataler1 = trocadetxt1.read()
    dataler1 = dataler1.replace(antigao, novao)
with open("Chimeric.faa", "w") as filezinho1:
    filezinho1.write(dataler1)
with open("Chimeric.faa", "r") as tropadeelite:
    lerlivros = tropadeelite.read()
    lerlivros = lerlivros.split(">")
print(lerlivros)
Acaba1 = NameOfTheTopModel + "\n"
letrinha = ">"
for ia in range(0,len(letrinha)):
    NameOfTheTopModel1 =NameOfTheTopModel.replace(letrinha[ia],"")
    print(Acaba1)
    for protein in lerlivros:
        if NameOfTheTopModel1 in protein:
            with open("YourFinalModel.faa","w") as finalmodel:
                finalmodel.writelines(protein)
                print(lerlivros)
                print(protein)
            with open("YourFinalModel.faa","r") as editar:
                arrumaisso = editar.read()
                arrumaisso = arrumaisso.replace(NameOfTheTopModel1,Acaba1)
                with open("YourFinalModel.faa", "w") as filezinho2:
                    filezinho2.write(arrumaisso)
quebradetextMAIS = "\n>"
with open("Chimeric.faa","r") as ArrumarQuimeras:
    ArrumarQuimerasBora = ArrumarQuimeras.read()
    ArrumarQuimerasBora = ArrumarQuimerasBora.replace(letrinha,quebradetextMAIS)
with open("Chimeric.faa", "w") as ArrumarQuimerasFINALMENTE:
    ArrumarQuimerasFINALMENTE.write(ArrumarQuimerasBora)
os.remove("Vaxijen.txt")


import selenium
from selenium import webdriver
import time, os, pandas as pd

lersabudega = pd.read_csv("YourFinalModel.faa")
lersabudega.to_csv("FinalSemCabeca.txt", header=None, index=None)
with open("FinalSemCabeca.txt") as semcabeca:
    leituradotrem = semcabeca.read()

navegadorALLER = webdriver.Firefox()
navegadorALLER.get("https://www.ddg-pharmfac.net/AllerTOP/")    
navegadorALLER.find_element_by_xpath('//*[@id="sequence"]').send_keys(leituradotrem)
time.sleep(1)
navegadorALLER.find_element_by_xpath('//*[@id="protein_sequence"]/table/tbody/tr[3]/td[1]/input').click()
time.sleep(5)
vamoslerisso = navegadorALLER.find_element_by_xpath('//*[@id="protein_sequence"]/table/tbody/tr/td')
vamoslerisso1 = vamoslerisso.text

navegadorALLER.get("https://web.expasy.org/protparam/")    
navegadorALLER.find_element_by_xpath('//*[@id="sib_body"]/form/textarea').send_keys(leituradotrem)
time.sleep(1)
navegadorALLER.find_element_by_xpath('//*[@id="sib_body"]/form/p[1]/input[2]').click()
time.sleep(5)
vamoslerisso2 = navegadorALLER.find_element_by_xpath('//*[@id="sib_body"]/pre[2]')
vamoslerisso3 = vamoslerisso2.text

navegadorALLER.get("http://bioinf.cs.ucl.ac.uk/psipred/")  
navegadorALLER.find_element_by_xpath('//*[@id="id_job_name"]').send_keys("VaxG")
navegadorALLER.find_element_by_xpath('//*[@id="id_email"]').send_keys("bioinformaticsuftm@gmail.com")
navegadorALLER.find_element_by_xpath('//*[@id="id_input_data"]').send_keys(leituradotrem)
time.sleep(1)
navegadorALLER.find_element_by_xpath('//*[@id="main_form"]/div[6]/input[2]').click()
time.sleep(5)
pegarurl = navegadorALLER.current_url

navegadorALLER.close()
with open("Aller.txt","w") as escritadisso:
    hamescreveisso = escritadisso.writelines(vamoslerisso1)
with open("ProtParam.txt","w") as escritadisso1:
    hamescreveisso1 = escritadisso1.writelines(vamoslerisso3)
with open("PsiPred.txt","w") as escritadisso2:
    hamescreveisso2 = escritadisso2.writelines(pegarurl)

z = zipfile.ZipFile('Final.zip', 'w', zipfile.ZIP_DEFLATED)
z.write('Aller.txt')
z.write('Chimeric.faa')
z.write('ProtParam.txt')
z.write('PsiPred.txt')
z.write('FinalEpitopes.txt')
z.write('YourFinalModel.faa')
z.write('Vaxijen.csv')
z.close()

import win32com.client as win32

# criar a integração com o outlook
outlook = win32.Dispatch('outlook.application')

# criar um email
email = outlook.CreateItem(0)
# configurar as informações do seu e-mail
email.To = "d201910872@uftm.edu.br"
email.Subject = "VaxG-Results"
email.HTMLBody = f"""
<p>Hello there! Thanks for using VaxG</p>
"""
anexo = os.getcwd()+"\Final.zip"
email.Attachments.Add(anexo)
email.Send()
print("Email Enviado")

print("Done")
print("\n\n Thanks for using MultiGenerator")