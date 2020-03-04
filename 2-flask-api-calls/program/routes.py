from program import app
from flask import render_template, request
from datetime import datetime
import requests

#Try out the PokeApi to see if you can pull other data than color
#Each return also gives a url for that specific pokemon, if you use request.get(url)
#you should get a JSON file with all the attributes of that pokemon
#Use the proper label to then pull the desired data and display it in another column

@app.route('/')
@app.route('/index')

def index():
        timenow = str(datetime.today())
        return render_template('index.html', time=timenow)

@app.route('/100Days')
def p100Days():
        return render_template('100days.html')


@app.route('/chuck')
def chuck():
        joke = get_chuck_joke()
        return render_template('chuck.html',
                                joke=joke)
def get_chuck_joke():
        r = requests.get('https://api.chucknorris.io/jokes/random')
        data = r.json()
        return data['value']

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
        pokemon = []
        if request.method == 'POST' and 'pokecolor' in request.form:
                color = request.form.get('pokecolor')
                if check_valid_color(color):
                        invalid_input = check_valid_color(color)
                else:
                        invalid_input = False
                pokemon = get_poke_colors(color)
        return render_template('pokemon.html', 
                                pokemon = pokemon,
                                invalid_input = invalid_input)

def check_valid_color(color):
        '''
        Sends a request for all valid color types to the api, returns a list of the valid inputs
        '''
        valid = requests.get('https://pokeapi.co/api/v2/pokemon-color')
        data = valid.json()
        valid_data = []
        for i in data['results']:
                valid_data.append(i['name'])
        
        error_messages = 'Please enter a valid color, {}'.format(valid_data)

        if color not in valid_data:
                invalid_input = valid_data
                return error_messages

        else:
                pass

def get_poke_colors(color):
        if check_valid_color(color): #If check_valid_color returns, the user entered something that doesn't exist
                pass
        else: #If it doesn't return, the user entered a valid input. Follow through the rest of the steps
                r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + color.lower()) 
                pokedata = r.json()
                pokemon = []

                for i in pokedata['pokemon_species']:
                        pokemon.append(i['name'])

                return pokemon