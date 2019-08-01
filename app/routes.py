import os
from app import app
from flask import render_template, request, redirect
from app.models import model
import json
import ast
import requests
from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'wishlist'
app.config['MONGO_URI'] = 'mongodb+srv://admin:magic@cluster0-dwlid.mongodb.net/wishlist?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    wishlist = mongo.db.wishlist
    gustavo_wishlist = list(wishlist.find({'name':'gustavo'}))
    logan_wishlist = list(wishlist.find({'name':'logan'}))
    sean_wishlist = list(wishlist.find({'name':'sean'}))
    return render_template('index.html', gustavo_wishlist=gustavo_wishlist, logan_wishlist=logan_wishlist, sean_wishlist=sean_wishlist)
    
@app.route('/wish', methods=['GET', 'POST'])
def wish():
    if request.method == 'GET':
        return "Fill out the form, dummy"
    else:
        formData = dict(request.form)
        name = formData['name']
        name = name.lower()
        if (name != 'gustavo') and (name.lower() == 'logan') and (name.lower() == 'sean'):
            return "Pick one of your Magic crew, dummy!"
        else:
            card_name = formData['card_name']
            cardData = model.fetchCard(card_name)
            response = requests.get(cardData)
            responseData = json.loads(response.content.decode('utf-8'))
            card_name_full = responseData['name']
            price = responseData['prices']['usd']
            foil_price = responseData['prices']['usd_foil']
            card_image_src = responseData['image_uris']['png']
            buy_link = responseData['purchase_uris']['tcgplayer']
            wishlist = mongo.db.wishlist
            wishlist.insert({"name":name, "card_name_full":card_name_full, "price":price, "foil_price":foil_price, "card_image_src":card_image_src, "buy_link":buy_link})
            gustavo_wishlist = list(wishlist.find({'name':'gustavo'}))
            logan_wishlist = list(wishlist.find({'name':'logan'}))
            sean_wishlist = list(wishlist.find({'name':'sean'}))
            print("#"*100,responseData['name'])
            return render_template('index.html', name=name, card_name_full=card_name_full, price=price, foil_price=foil_price, card_image_src=card_image_src, buy_link=buy_link, gustavo_wishlist=gustavo_wishlist, logan_wishlist=logan_wishlist, sean_wishlist=sean_wishlist)
            
# @app.route('/clear/<name>')
# def clear(name):
#     wishlist = mongo.db.wishlist
#     wishlist.remove({'name':name})
#     return render_template('index.html') 
    
