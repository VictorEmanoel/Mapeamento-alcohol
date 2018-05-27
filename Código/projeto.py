# -*- coding: utf-8 -*-
"""
Created on Sun May 27 12:26:27 2018

@author: victo
"""
import requests
import sqlite3 as lite
import folium

con = lite.connect('destilariasporlatitude.db')
c = con.cursor()

con1 = lite.connect('destilariasporlongitude.db')
c1 = con1.cursor()

r = requests.get('http://dados.al.gov.br/dataset/293b2048-210d-4024-9d2e-8f47790897ae/resource/aee1a25e-7472-4141-9473-cfe774e9c790/download/usinasedestilarias.geojson')
x=r.json()
    
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS NomeLatitude(Nome TEXT, Latitude REAL)")
    c1.execute("CREATE TABLE IF NOT EXISTS NomeLongitude(Nome TEXT, Longitude REAL)")
        
def dynamic_data_entry(nome,latitude,longitude):
    
    c.execute("INSERT INTO NomeLatitude (Nome, Latitude) VALUES (?,?)",(nome,latitude))
    c1.execute("INSERT INTO NomeLongitude (Nome, Longitude) VALUES (?,?)",(nome,longitude))
    con.commit
    con1.commit

create_table()
for i in range(len(x['features'])):   
    nome=x['features'][i]['properties']['Nome']
    longitude=x['features'][i]['geometry']['coordinates'][0]   
    latitude=x['features'][i]['geometry']['coordinates'][1]
    dynamic_data_entry(nome,latitude,longitude)

c.close
con.close

c1.close
con1.close

c.execute("SELECT * FROM (NomeLatitude)")
c1.execute("SELECT * FROM (NomeLongitude)")

rows = c.fetchall()
rows1= c1.fetchall()

def map_destilarias():
    mapa = folium.Map(location=[rows[9][1],rows1[9][1]],zoom_start=8)
    
    for row in range(25):
        folium.Marker([rows[row][1],rows1[row][1]],popup=rows[row][0]).add_to(mapa)
        
    mapa.save('mapa.html')
    
map_destilarias()