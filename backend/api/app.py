import os
import random
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import json

app = Flask(__name__)

VOTES_LOCATION = 'votes.json'
BATTLES_LOCATION = 'battles.json'
votes = defaultdict(lambda: {'likes': 0, 'dislikes': 0})
battles = defaultdict(lambda: {'wins': 0, 'losses': 0})

if os.path.exists(VOTES_LOCATION):
  with open(VOTES_LOCATION, 'r') as file:
    votes = json.load(file)
if os.path.exists(BATTLES_LOCATION):
  with open(BATTLES_LOCATION, 'r') as file:
    battles = json.load(file)

# List of image URLs
images = os.listdir(os.path.join(os.path.dirname(__file__), 'static/images'))

#region Pages

@app.route('/', methods=['GET'])
def get_home_page():
  '''Returns the home page of the app'''
  return render_template('index.html')

@app.route('/battle', methods=['GET'])
def get_battle_page():
  '''Returns the battle page of the app'''
  return render_template('battle.html')

@app.route('/battle/data', methods=['GET'])
def get_battle_data():
  '''Returns the battle results of the app'''
  return jsonify(battles)

@app.route('/refresh', methods=['GET'])
def get_refresh_page():
  '''Returns the refresh page of the app'''
  return render_template('refresh.html')

@app.route('/votes', methods=['GET'])
def get_votes_page():
  '''
  Returns the votes for each image as a JSON object
  
  Future improvement: This will become a page that displays the votes for each image instead of returning a JSON object
  '''
  return jsonify(votes)

#endregion

#region API

@app.route('/api/vote/dislike', methods=['POST'])
def vote_dislike():
  '''
  Expects a form parameter 'imageUrl' which is the full url of the image to vote on
  Increments the number of dislikes for the image at the given index
  '''
  current_image_url = request.form.get('imageUrl')
  if current_image_url is None:
    return 'No image URL provided', 400
  image = current_image_url.split('/')[-1]
  votes[image]['dislikes'] += 1
  # Save votes to a file
  with open(VOTES_LOCATION, 'w') as file:
    json.dump(votes, file)
  return '', 204


@app.route('/api/vote/like', methods=['POST'])
def vote_like():
  '''
  Expects a form parameter 'imageUrl' which is the full url of the image to vote on
  Increments the number of likes for the image at the given index
  '''
  current_image_url = request.form.get('imageUrl')
  if current_image_url is None:
    return 'No image URL provided', 400
  image = current_image_url.split('/')[-1]
  votes[image]['likes'] += 1
  # Save votes to a file
  with open(VOTES_LOCATION, 'w') as file:
    json.dump(votes, file)
  return '', 204

@app.route('/api/image/new_url', methods=['GET'])
def get_new_image_url():
  '''
  Returns the image URL for a random image
  '''
  image = random.choice(images)
  image_url = f'static/images/{image}'
  return jsonify({'image_url': image_url})

@app.route('/api/refresh', methods=['POST'])
def refresh():
  '''Refreshes the images internally'''
  global images
  images = os.listdir(os.path.join(os.path.dirname(__file__), 'static/images'))
  return '', 204


@app.route('/api/battle/vote', methods=['POST'])
def vote_battle():
  '''
  Expects a form parameter 'imageUrl' which is the full url of the image to vote on
  Increments the number of dislikes for the image at the given index
  '''
  winner_image_url = request.form.get('winnerUrl')
  looser_image_url = request.form.get('looserUrl')
  if winner_image_url is None or looser_image_url is None:
    return 'No image URL provided', 400
  win_image = winner_image_url.split('/')[-1]
  battles[win_image]['wins'] += 1
  loss_image = looser_image_url.split('/')[-1]
  battles[loss_image]['losses'] += 1
  # Save battles to a file
  with open(BATTLES_LOCATION, 'w') as file:
    json.dump(battles, file)
  return '', 204

#endregion

if __name__ == '__main__':
  app.run(host='0.0.0.0')
