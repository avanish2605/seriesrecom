import streamlit as st
import pickle
import pandas as pd
import requests
import lzma

anime = pd.read_csv("imdb_anime.csv")
OMDB_API_KEY = '2b94772e'

# 🔧 Helper: Check if it's anime (you can improve with a flag column)
def is_anime(title):
    return title.lower().strip() in anime['Title'].str.lower().str.strip().values


# 🔧 Helper: Get Poster from Jikan or OMDb
def get_poster(title):
    if is_anime(title):
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['data'][0]['images']['jpg']['image_url']
            except:
                return "Anime Poster Not Found"
        else:
            return "Anime API Error"
    else:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True" and data.get("Poster") != "N/A":
                return data['Poster']
            else:
                return "Series Poster Not Found"
        else:
            return "Series API Error"



def rem(sa):
    name = tv[tv['Title']==sa].index[0]
    similarity1 = csimi[name]
    tv_list = sorted(list(enumerate(similarity1)),reverse = True ,key = lambda x: x[1])[1:11]
    recom = []
    for i in tv_list:
        title = tv['Title'][i[0]]
        des = tv['tags'][i[0]]
        poster = get_poster(title)
        #t = print(f'\n🎬 Name --> {title}\n📝Overview:\n{des} \n ')
        print(f"\n🎬 Name: {title}\n\n📝 Overview:\n{des}\n\n🖼️ Poster: {poster}\n")
        recom.append((title, des, poster))

    return recom

tv_dict = pickle.load(open('tv_dict6.pkl','rb'))
tv = pd.DataFrame(tv_dict)

with lzma.open('csimi3.pkl.xz','rb') as f:
    csimi = pickle.load(f)

options = ['Tap here to select from dropdown menu or write it !!'] + list(tv['Title'].values)
st.title('Web series and anime recommender system')

selected = st.selectbox('Give me the name of any anime or web series so that i can suggest you some similar ones !!',options)

if st.button('suggest'):
    recommendations = rem(selected)

    for title, des, poster in recommendations:
        col1, col2 = st.columns([1, 3])
        with col1:
            default_poster = "https://via.placeholder.com/150?text=No+Image"

            if poster and poster.startswith("http"):
                st.image(poster, width=150)
            else:
                st.image(default_poster, width=150)

        with col2:
            st.write(f"**{title}**")
            st.write(des)



