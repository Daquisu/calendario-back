#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 08:25:44 2020

@author: viniciusariel
"""
import nltk
import gensim
import json
import unicodedata as ucd

#Classe que define um tweet
class Tweet:
    def __init__(self, frases, autor, favs, retwts):
        self.frases = frases #Frases que compoõem o texto do tweet
        self.autor = autor   #Autor do tweet
        self.favs = favs     #Número de favoritados/Curtidas
        self.retwts = retwts #Número de Retweets
    
    #faz a classe se tornar JSON serializable
    def toJSON(self):
        return {'author': self.autor,
                'favorite_count': self.favs,
                'retweet_count': self.retwts,
                'text': (self.frases[0]).encode('utf8').decode('utf8')}
    
#Recebe como parâmetro o caminho de um arquivo .json no diretório e, a partir dele, cria
#cria objetos da classe "Tweet"
def lerJson (caminho):
    tweets = []
    
    arqJson = open(caminho, "r")
    conteudoJson = arqJson.read()
    
    while(conteudoJson.find("text") != -1):
        info = conteudoJson[conteudoJson.find("author"): conteudoJson.find("}") + 1]
        #autor
        autor = info[info.find("author") + 9: info.find(",") -1]
        info = info[info.find(",") + 1:]
        #favoritados
        favs = int(info[info.find("favorite") + 16: info.find(",")])
        info = info[info.find(",") + 1:]
        #retweets
        retwts = int(info[info.find("retweet") + 15: info.find(",")])
        info = info[info.find(",") + 1:]
        #texto
        texto = info[info.find("text") + 7: info.find("}") -1]
        frases = nltk.sent_tokenize(texto) #separa o texto em um vetor de frases
        info = None                        #deixa a info vazia por até o pŕoximo loop
        #novoTweet
        novoTweet = Tweet(frases, autor, favs, retwts)
        if(retwts >= 60):
            tweets.append(novoTweet)
        #atualiza o conteúdo do Json que falta ser lido
        conteudoJson = conteudoJson[conteudoJson.find("}") + 1:]
        
    arqJson.close()
    return tweets

def verificarSemelhanca(texto1, texto2, tweets):
    textosDoDia = []
    for tweet in tweets:
        for frase in tweet.frases:
            if(frase != texto1):
                textosDoDia.append(frase)
    
    indiceTexto2 = textosDoDia.index(texto2)
    
    #Deixar tudo em minúscula:
    textosDoDia = [[palavra.lower() for palavra in nltk.word_tokenize(texto)] for texto in textosDoDia]
    texto1 = [palavra.lower() for palavra in nltk.word_tokenize(texto1)]
    #texto2 = [palavra.lower() for palavra in nltk.word_tokenize(texto1)]
    
    #Criação de um Dicionário:
    dicionario = gensim.corpora.Dictionary(textosDoDia)
    
    #Ciração de um Corpus:
    corpus = [dicionario.doc2bow(texto) for texto in textosDoDia]
    
    #Criação de um tf_idf:
    tf_idf = gensim.models.TfidfModel(corpus)
    
    sims = gensim.similarities.Similarity('./',tf_idf[corpus], num_features=len(dicionario))
    
    sacoDePalavras = dicionario.doc2bow(texto1)
    
    query_doc_tf_idf = tf_idf[sacoDePalavras]
    
    listaSim = str(sims[query_doc_tf_idf])
    
    i = 0
    while(i < indiceTexto2):
        listaSim = listaSim[listaSim.find(" ") +1 :]
        i += 1
    
    try:
        if(listaSim[0] == "["):
           return float(listaSim[1:listaSim.find(" ")])
       
        return float(listaSim[:listaSim.find(" ")])
    except(ValueError):
        return 0.0
    
def semelhancaDeTweets(twt1, twt2, tweets):
    tamanhoTotal = 0
    for frase in twt1.frases:
        tamanhoTotal += len(frase)
    for frase in twt2.frases:
        tamanhoTotal += len(frase)
    
    semelhanca = 0
    for frase1 in twt1.frases:
        for frase2 in twt2.frases:
            semelhanca += (verificarSemelhanca(frase1, frase2, tweets)) * (len(frase1) + len(frase2))
    
    semelhanca = semelhanca / tamanhoTotal
    
    return semelhanca

def limparTweets(tweets):
    i = 0
    for tweet1 in tweets:
        
        for tweet2 in tweets[tweets.index(tweet1) + 1:]:
            i+=1
            if(semelhancaDeTweets(tweet1, tweet2, tweets) >= 0.25):
                if(tweet1.retwts > tweet2.retwts):
                    tweets.remove(tweet2)
                else:
                    tweets.remove(tweet1)
    
    return tweets

def mergeSort(arr): 
    if len(arr) >1: 
        mid = int(len(arr)//2) #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i].retwts < R[j].retwts: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

def gerarTxt(tweets, caminhoTxt):
    arqTxt = open(caminhoTxt, "w")
    
    for tweet in tweets:
        arqTxt.write("Autor: " + str(tweet.autor) + "\n")
        arqTxt.write("Retweets: "+ str(tweet.retwts) + "\n")
        for frase in tweet.frases:
            arqTxt.write(frase)
        arqTxt.write("\n")
        arqTxt.write("\n")
    
    arqTxt.close()



def main():
    for year_month in os.listdir('./top_tweets/raw/')
        for json_file in os.listdir('./top_tweets/raw/' + year_month + '/'):
            caminhoJson = './top_tweets/raw/' + year_month + '/' + json_file
            caminhoTxt = './top_tweets/processed/txts'  + '/' + json_file[:-4] + '.txt'
            caminhoJsonSaida = './top_tweets/processed/' + year_month + '/' + json_file
            print("Lendo arquivo .josn...")
            tweets = lerJson(caminhoJson)
            print("Limpando tweets semelhantes...")
            tweets = limparTweets(tweets)
            print("Colocando tweets em ordem de maior retweets...")
            mergeSort(tweets)
            tweets.reverse()
            print("Escrevendo tweets...")
            gerarTxt(tweets, caminhoTxt)
            print("Gerando .json...")
            tweetsJson = []
            for tweet in tweets:
                tweetsJson.append(tweet.toJSON())
            with open(caminhoJsonSaida, "w") as fp:
                json.dump(tweetsJson, fp)
    

main()