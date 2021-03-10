#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 16:57:24 2019

@author: keshav
"""
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
count = CountVectorizer(stop_words='english')

df1=pd.read_csv('books_cleaned.csv')
df1.loc[(df1.original_publication_year<1000),'original_publication_year']=np.nan
df1=df1.dropna()

C=df1['average_rating'].mean()
m=df1['ratings_count'].quantile(0.1)

def WR(x):
    v=x['ratings_count']
    R=x['average_rating']
    return (v/(v+m)*R) + (m/(m+v)*C)

df1['score'] = df1.apply(WR,axis=1)

def lng(x,str1):
    if (x['language_code'] == str1):
        return x

def clean_data(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''

df1['authors'] = df1['authors'].apply(clean_data)

def create_soup(x):
    return ' ' + x['authors'] + ' ' +  x['description']
df1['soup'] = df1.apply(create_soup, axis=1)
def get_recommendations(titles):
    try:
        return get_recommendation(titles)
    except:
        return ["BOOK NOT IN DATABASE"]
def get_recommendation(titles):
    # Get the index of the movie that matches the title
    df3=df1
    scr=5
    df2=pd.DataFrame()
    all_titles=""
    all_soup=""
    for title in titles:
        lang=df1['language_code'][df1.original_title == title].values[0]
                ##################### CONCATENATION DONE#################################################
        df2=df2.append(df3[df3.language_code == lang])
        df3=df3[df3.language_code !=lang]
        scr_temp=int(df1['score'][df1.original_title == title].values[0])
        all_titles+=title+" "
        all_soup+=df1.loc[(df1.original_title==title),'soup'].values[0] + " "
        if(scr_temp<scr):
            scr=scr_temp
    scr=scr - 0.5
    df2=df2[df2.score>scr]
    print
    for title in titles:
        i = df2[(df2.original_title==title)].index.values[0]
        df2 = df2.drop(i)
    df2 = df2.append({'book_id':0000, 'authors':'not required', 'original_publication_year':20, 'original_title':all_titles,
       'title':all_titles, 'language_code':lang, 'average_rating':0, 'ratings_count':0000,'score':scr,'soup':all_soup} , ignore_index=True)
    count_matrix = count.fit_transform(df2['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    df2 = df2.reset_index()
    indices = pd.Series(df2.index, index=df2['original_title'])
    idx = indices[all_titles]
    # Get the pairwsie similarity scores of all movies with that movie
    #C_M(lang)
    sim_scores = list(enumerate(cosine_sim2[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    #print(sim_scores)
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return df2['original_title'].iloc[movie_indices].values


def UI():
    df_book_names=df1.sort_values(by='original_title')
    names=df_book_names['original_title'].values
    req=[]
    i=0
    req_book=[]
    req=input("Enter starting words of book ")
    for name in names:
        if name.lower().startswith(req):
            req_book.append(name)
    req[0]
    if len(req_book)==0:
        print("No such book found")
        return 0
    while(i<len(req_book)):
        print(i,'.',req_book[i])
        i+=1
    choices=input("Enter your choices separated by space ")
    book_name=[req_book[int(choice)] for choice in choices.split()]
    A = df1[df1.apply(got_book,args=([book_name]),axis=1)]
    print("Similar Books")
    for i in get_recommendations(A.original_title):
        print(i)
def got_book(x,title):
    if(x['original_title'] in title):
        print('Book Name: ',x['original_title'])
        print()
        print('Book Author:',x['authors'])
        print()
        print('Publication Year:', x['original_publication_year'])
        print()
        print('Language:',x['language_code'])
        print()
        print('our_rating:',x['score'])
        print()
        print('description:')
        print()
        print(x['description'])
        print()
        a=user.loc[(user.book_id==x['book_id'])].shape[0]
        a=a/user.shape[0]
        a=a*100
        print('percentage of people read this book = ',a)
        return True
    return False
        
        
        
user=pd.read_csv('ratings.csv')
def accept(vals,A,comb,head_lbl):
    A.append(comb.get())
    prfx = "Books similar to - "
    all_recs = get_recommendations(A)
    head_lbl.set(prfx+','.join(A))
    #print("books similar to {} :-".format(A))
    #print(all_recs)
    
    for i in range(10):
        vals[i].set(all_recs[i])
def GUI():
    A=[]
    df_book_names=df1.sort_values(by='original_title')
    names=df_book_names['original_title'].values
    AllNames=[]
    for i in names:
        AllNames.append(i)
    root = tk.Tk()
    myFont = font.Font(size=20)
    root["bg"] ="black"
    vals = ["" for i in range(10)]
    
    head_lbl = tk.StringVar() 
    for i in range(10):
        vals[i] = tk.StringVar()
    width= root.winfo_screenwidth()  
    height= root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height)) 
    root.title("Book Recommenation System") 
    root.option_add("*TCombobox*Listbox*Font", myFont)
    label = tk.Label(root, text="Select Book!",bg="black",fg="white",font=myFont) 
    label.pack() 
    d={'0':'1','2':'2'}
    w = ttk.Combobox(root,font=myFont,width=80)
    w['values'] = AllNames
    w.pack()
    btn = ttk.Button(root, text="Submit",command=lambda:accept(vals,A,w,head_lbl))
    btn.pack()
    myFont1 = font.Font(size=30)
    tk.Label(root, textvariable=head_lbl,font=myFont1,bg='black',fg='green').pack()
    for i in range(10):
        tk.Label(root, textvariable=vals[i],font=myFont,bg='black',fg='white').pack()
    #print('hi',w.get())
    root.mainloop()
def getBookList():
    df_book_names=df1.sort_values(by='original_title')
    names=df_book_names['original_title'].values
    AllNames=[]
    j = 0
    for i in names:
        AllNames.append((str(j),i))
        j+=1
    return tuple(AllNames)
if __name__=='__main__':
    GUI()
    #UI()