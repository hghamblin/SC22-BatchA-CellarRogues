# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user?
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model?
"""

# import basics
import os
# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
from better_profanity import profanity
# import stuff for our models
from aitextgen import aitextgen

import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer

# load up a model from memory. Note you may not need all of these options.
# ai = aitextgen(model_folder="model/",
#                tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)

default_model = aitextgen(model_folder = "models/default-model", to_gpu=False)
silly_model = aitextgen(model_folder = "models/silly-model", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver


@app.route(f'{base_url}')
def home():
    return render_template('index.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('generator.html', generated=data)
    else:
        return render_template('generator.html', generated=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text.
    """
    #get input from website
    prompt = request.form['prompt']
    fun_on = request.form.getlist('funny_output')
    emoji_on = request.form.getlist('emojis')

    if fun_on == []: # just captions
        if prompt is not None:
            generated = default_model.generate(
            n=3,
            batch_size=3,
            prompt=str(prompt),
            max_length=40,
            temperature=0.8,
            return_as_list=True
        )
            
        print(generated)
        
        chopped = []
        for caption in generated:
            lines = caption.split('\n')
            if lines[0] == prompt:
                first_two = lines[0] + " " + lines[1]
                chopped.append(first_two)
            else:
                chopped.append(lines[0])
        generated = chopped

    else: # all data
        if prompt is not None:
            generated = silly_model.generate(
            n=3,
            batch_size=3,
            prompt=str(prompt),
            max_length=40,
            temperature=0.9,
            return_as_list=True
        )

#         if prompt.multiple_text is not None:
#             generated = nltk.sent_tokenize(generated)
#             generated = generated[0:3]

        #replace slashes with new line
        removed_slashes = []
        for line in generated:
            line = line.replace(" / ", "\n")
            removed_slashes.append(line)

        generated = removed_slashes
        
    print(generated)
    
    #emoji sentiment analysis
    if emoji_on != []:
        sia = SentimentIntensityAnalyzer()
        with_emojis = []
        for caption in generated:
            scores = sia.polarity_scores(caption)
            if scores['compound'] > 0:
                with_emojis.append(caption + "😁")

            elif scores['compound'] < 0:
                with_emojis.append(caption + "😥")

            elif scores['compound'] == 0:
                with_emojis.append(caption + '😐')

            print("emojis: ", with_emojis)

            generated = with_emojis
    
    #change everything to lowercase then change "i" to "I"
    caps_list = []
    for i in range(len(generated)):
        clean_sentence = ""
        sentence = generated[i]
        tokenized_text = nltk.word_tokenize(sentence)
        for word in tokenized_text:
            clean_word = word.lower()
            if (clean_word == 'i'):
                clean_word = 'I'
            clean_sentence += clean_word + ' '
        caps_list.append(clean_sentence)
    generated = caps_list

    # tokenized_text is the cleaned output
    
    print("fixed caps: ", generated)


    generated_clean = []
    
    # generated = ['sentence one', 'sentence two', 'number three']

    #ronok -- censor profanity
    for text in generated:
        # remove profanity
        censored = profanity.censor(text)
        # only take first sentence
        generated_clean.append(censored)
        
    generated = generated_clean
    
    print("censored: ", generated)
    
    

    data = {'generated_ls': generated}
    session['data'] = generated
    return redirect(url_for('results'))


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc4.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
