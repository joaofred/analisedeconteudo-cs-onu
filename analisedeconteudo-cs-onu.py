#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:49:27 2017

@author: fred
"""

import pandas as pd
import html2text as h2t

import os

paisesdb = pd.read_table("./countries.txt")
paises = list(paisesdb.Country)

def consolidar_htmls():
    local = "./htmls/"
    arquivos = os.listdir(local)
    arquivos = sorted(arquivos)
    lista = []
    dflist = []
    #dfout = pd.DataFrame(columns=["string","periodo"])
    for i in arquivos:
        caminho = local+i
        periodo=i[0:7]
        html = open(caminho).read()
        texto = h2t.html2text(html)
        lista.append(texto)
        dflist.append(pd.DataFrame({"string":[texto], "periodo":[periodo]}))
    dfout = pd.concat(dflist)
    dfout = dfout.reset_index()
    return(dfout)
        
def extract_countries(string):
    lista = []
    for i in paises:
        if i in string: lista.append(i)
    return(lista)

htmls = consolidar_htmls()
htmls["paisescitados"] = htmls.string.map(lambda x: extract_countries(x))
todosospaises = list(set(sum(htmls.paisescitados, [])))

def contador(pais):
    contador = 0
    for i in htmls.paisescitados:
        if pais in i: contador+=1
    return((pais, contador))

def conta_todos():
    tuplas = []
    for i in todosospaises: 
        tuplas.append(contador(i))
    dfout = pd.DataFrame(tuplas, columns=["País", "Contagem"])
    return(dfout)

def contador2(pais):
    contador = [pais]
    for i in htmls.paisescitados:
        cont = 0
        if pais in i: cont+=1
        contador.append(cont)
    soma = sum(contador[1:])
    contador.append(soma)
    contador = tuple(contador)
    return((contador))

def conta_todos2():
    tuplas = []
    for i in todosospaises: 
        tuplas.append(contador2(i))
    colunas = ["país"] + list(htmls.periodo) + ["TOTAL"]
    dfout = pd.DataFrame(tuplas, columns=colunas)
    return(dfout)

dfconta = conta_todos2()




# a1213 = [x[0] for x in _tuplas2 if x[1]==1]