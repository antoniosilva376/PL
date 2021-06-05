import re
import subprocess
import os


def ex1(conteudo):
    inscricao = re.findall(r'\{[^}]+\}', conteudo)
    res = []
    for elemento in inscricao:
        nome = re.search(r'"nome":"([^"]+)"', elemento)
        morada = re.search(r'"morada":".*(?i:valongo)"', elemento)
        equipa = re.search(r'"equipa":"(?i:individual)"', elemento)
        if(morada and equipa):
            res.append(nome.group(1).upper())
    print("")
    print(res)

def ex2(conteudo):
    inscricao = re.findall(r'\{[^}]+\}', conteudo)
    for elemento in inscricao:
        nome = re.search(r'"nome":"(.*(Ricardo|Paulo).*)"', elemento)
        email = re.search(r'"email":"(.+@gmail.com)"', elemento)
        prova = re.search(r'"prova":"([^"]+)"',elemento)
        if(nome and email):
            print("")
            print(nome.group(1)+ ' | ' + email.group(1) + ' | ' + prova.group(1))

def ex3(conteudo):
    inscricao = re.findall(r'\{[^}]+\}', conteudo)
    for elemento in inscricao:
        nome = re.search(r'"nome":"([^"]+)"', elemento)
        dataNasc = re.search(r'"dataNasc":"([^"]+)"', elemento)
        morada = re.search(r'"morada":"([^"]+)"', elemento)
        email = re.search(r'"email":"([^"]+)"', elemento)
        prova = re.search(r'"prova":"([^"]+)"', elemento)
        escalao = re.search(r'"escalao":"([^"]+)"', elemento)
        equipa = re.search(r'"equipa":"((?i:TURBULENTOS))"', elemento)
        if(equipa):
            print("")
            print(nome.group(1) + ' | ' + dataNasc.group(1) + ' | ' + morada.group(1) + ' | ' + 
            email.group(1) + ' | ' + prova.group(1) + ' | ' + escalao.group(1) + ' | ' + equipa.group(1))

def ex4(conteudo):
    inscricao = re.findall(r'\{[^}]+\}', conteudo)
    res = []
    #(escalao,count)
    for elemento in inscricao:
        escalao = re.search(r'"escalao":"([^"]+)"', elemento)
        if(escalao):
            flag = True
            t = (escalao.group(1),1)
            if len(res)!=0:
                i=0
                for tuplo in res:
                    if(t[0].upper() == tuplo[0].upper()):
                        res[i] = (escalao.group(1), tuplo[1] + 1)
                        flag = False
                    i+=1
            if(flag):
                res.append(t)
    print("")
    print(sorted(res,key=lambda tup:tup[0]))

def ex5(conteudo):
    inscricao = re.findall(r'\{[^}]+\}', conteudo)
    equipas = []
    for elemento in inscricao:
        equipa = re.search(r'"equipa":"([^"]+)"', elemento)
        
        nome = re.search(r'"nome":"([^"]+)"', elemento)
        
        prova = re.search(r'"prova":"([^"]+)"', elemento)

        if(equipa and nome and prova):
            flag = True
            t = (equipa.group(1),1,list((nome.group(1),prova.group(1))))
            if len(equipas)!=0:
                i=0
                for tuplo in equipas:
                    if(t[0].upper() == tuplo[0].upper()):
                        tuplo[2].append((nome.group(1),prova.group(1)))
                        equipas[i] = (equipa.group(1), tuplo[1] + 1, tuplo[2])
                        flag = False
                    i+=1
            if(flag):
                equipas.append(t)
                
    equipas = sorted(equipas,key=lambda tup:(-tup[1],tup[0]))
    indice = 0
    for equipa in equipas:
                equipaM = open(("html/" + str(indice)) + ".html","+w")
                equipaTxt = ""
                equipaTxt = equipaTxt + "<!DOCTYPE HTML>\n<html>\n"
                equipaTxt = equipaTxt + "<head>\n<style>\n body{ \n background-image: url(foto1.jpeg); \n background-attachment: fixed; \n background-size: cover; \n background-repeat: no-repeat; \n } \n </style> \n </head>"
                equipaTxt = equipaTxt + "<title>Membros</title>\n\n"
                equipaTxt = equipaTxt + "<style>"
                equipaTxt = equipaTxt + " * {\n font-family: sans-serif; \n}\n"
                equipaTxt = equipaTxt + "   #container{\n   display: flex; \n   justify-content: center;\n}\n"
                equipaTxt = equipaTxt + "\n   .content-table {\n     border-collapse: collapse; \n     margin: 25px 0; \n     font-size: 0.9em; \n     min-width: 400px; \n     border-radius: 5px 5px 0 0; \n     overflow: hidden; \n     box-shadow: 0 0 20px rgba(0,0,0,0.15); \n}\n"
                equipaTxt = equipaTxt + ".content-table th,\n.content-table td {\n  padding: 12px 15px;\n}\n.content-table tbody tr {\n border-bottom: 1px solid #dddddd; \n background-color: #ffffff; \n}\n "
                equipaTxt = equipaTxt + "\n   .content-table thead tr {\n     background-color: #009879; \n     color: #ffffff; \n     text-align: left; \n     font-weight: bold; \n}\n .content-table tbody tr:nth-of-type(even) {\n background-color: #f3f3f3;\n}\n .content-table tbody tr:last-of-type {\n border-bottom: 2px solid #009879;\n} \n .content-table tbody tr.active-row { \nfont-weight: bold; \n color: #009879; \n}\n"
                equipaTxt = equipaTxt + "</style>\n\n"
                equipaTxt = equipaTxt + "<STYLE>A {text-decoration: none;} </STYLE>"
                equipaTxt = equipaTxt + "<body>\n <p style=text-align:center;font-size:26px;><b> \n Atletas da equipa \""+ str(equipa[0]) +"\" inscritos por prova</b></p> <div id='container'>\n<table class='content-table'>\n<thead>\n<tr>\n<th>Nome do Atleta</th>\n<th>Nome da Prova</th></tr></thead>"
                equipa[2].sort(key=lambda tup:(tup[0]))  
                count = 0             
                for qlq in equipa[2]:
                    equipaTxt = equipaTxt + "<tr><p><td><b>" + str(qlq[0]) + "</b> <td>" + str(qlq[1]) + "</td></p></li></tr>\n"
                    count += 1
                equipaTxt = equipaTxt + "</ul>\n</div></body>\n</html\n"  
                equipaM.write(equipaTxt)
                equipaM.close()
                indice += 1

    s = ""
    s = s + "<!DOCTYPE HTML>\n<html>\n"
    s = s + "<head>\n<style>\n body{ \n background-image: url(foto.jpeg); \n background-attachment: fixed; \n background-size: cover; \n background-repeat: no-repeat; \n } \n </style> \n </head>"
    s = s + "<title>Equipas</title>\n\n"
    s = s + "<style>"
    s = s + " * {\n font-family: sans-serif; /* Change your font family */\n}\n"
    s = s + "   #container{\n   display: flex; \n   justify-content: center;\n}\n"
    s = s + "\n   .content-table {\n     border-collapse: collapse; \n     margin: 25px 0; \n     font-size: 0.9em; \n     min-width: 400px; \n     border-radius: 5px 5px 0 0; \n     overflow: hidden; \n     box-shadow: 0 0 20px rgba(0,0,0,0.15); \n}\n"
    s = s + ".content-table th,\n.content-table td {\n  padding: 12px 15px;\n}\n.content-table tbody tr {\n border-bottom: 1px solid #dddddd; \n  background-color: #ffffff;}\n "
    s = s + "\n   .content-table thead tr {\n     background-color: #009879; \n     color: #ffffff; \n     text-align: left; \n     font-weight: bold; \n}\n .content-table tbody tr:nth-of-type(even) {\n background-color: #f3f3f3;\n}\n .content-table tbody tr:last-of-type {\n border-bottom: 2px solid #009879;\n} \n .content-table tbody tr.active-row { \nfont-weight: bold; \n color: #009879; \n}\n"
    s = s + "</style>\n\n"
    s = s + "<STYLE>a:link {\n color: rgb(0, 0, 0);\n background-color: transparent; \n text-decoration: none; \n } \n\n a:visited { \n color: rgb(0, 0, 0); \n background-color: transparent; \n text-decoration: none; \n }\n\n a:hover { \n color: rgb(0, 0, 0); \n background-color: transparent; \n text-decoration: underline; \n }\n\n  a:active { \n color: rgb(0, 0, 0); \n background-color: transparent; \n text-decoration: underline; \n } \n </STYLE>"
    s = s + "<body> \n   <div id='container'>\n<table class='content-table'>\n<thead>\n<tr>\n<th>Nome da Equipa</th>\n<th>Número de atletas</th></tr></thead>"

    contador = 0
    for equipa in equipas:
        s = s + "<tr><p><td> <a href=\"html/" + str(contador) + ".html\"> <b>" + equipa[0] + "</b></a>" + "<td style='text-align:center; vertical-align:middle'>" + str(equipa[1]) + "</td></p></li></tr>\n"
        contador += 1
    s = s + "</ul>\n</div></body>\n</html\n"
    index = open("index.html","w+")
    index.write(s)
    index.close()
    url = "/Users/ivo/Downloads/TP/index.html"
    try: #Windows
        os.startfile(url)
    except AttributeError:
        try: #MacOS and linux
            subprocess.call(['open', url])
        except:
            print('Could not open URL')
    

with open('inscritos-form.json') as f:
    next(f)
    conteudo = f.read()

    print("\nProcessador de Inscritos numa atividade Desportiva")
    opc = int( input("\nEscolha:\n1. Imprimir o nome (convertido para maiúsculas) de todos os concorrentes que se inscrevem como 'Individuais' e são de 'Valongo';\n2. Imprimir o nome completo, o telemóvel e a prova em que está inscrito cada concorrente cujo nome seja 'Paulo' ou 'Ricardo', desde que usem o GMail;\n3. Imprimir toda a informação dos atletas da equipe 'TURBULENTOS'; \n4. Imprimir a lista dos escalões por ordem alfabética e para cada um indicar quantos atletas estão inscritos nesse escalão;\n5. Gerar uma página HTML com a lista das equipes inscritas em qualquer prova, indicando o seu nome e o número dos atletas que a constituem e que se inscreveram pelo menos uma vez numa prova; essa lista deve estar ordenada por ordem decrescente do número de atletas; além disso, cada equipe deve ter um link para outra página HTML com a informação que achar interessante sobre cada atleta indicando as provas em que cada um participou; \n\n0. Terminar?\n\n ") )
    while opc:
      if (opc<0 or opc >5):
         print("Opção Inválida!") 
      else:
        if opc == 1:
           ex1(conteudo)
        elif opc == 2:
           ex2(conteudo)
        elif opc == 3:
           ex3(conteudo)
        elif opc == 4:
           ex4(conteudo) 
        elif opc == 5:
           ex5(conteudo)     
    
      opc = int( input("\nEscolha:\n1. Imprimir o nome (convertido para maiúsculas) de todos os concorrentes que se inscrevem como 'Individuais' e são de 'Valongo';\n2. Imprimir o nome completo, o telemóvel e a prova em que está inscrito cada concorrente cujo nome seja 'Paulo' ou 'Ricardo', desde que usem o GMail;\n3. Imprimir toda a informação dos atletas da equipe 'TURBULENTOS'; \n4. Imprimir a lista dos escalões por ordem alfabética e para cada um indicar quantos atletas estão inscritos nesse escalão;\n5. Gerar uma página HTML com a lista das equipes inscritas em qualquer prova, indicando o seu nome e o número dos atletas que a constituem e que se inscreveram pelo menos uma vez numa prova; essa lista deve estar ordenada por ordem decrescente do número de atletas; além disso, cada equipe deve ter um link para outra página HTML com a informação que achar interessante sobre cada atleta indicando as provas em que cada um participou; \n\n0. Terminar?\n\n ") )