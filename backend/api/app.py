import os
import random
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import json

app = Flask(__name__)

# Dictionary to store votes for each image
votes = defaultdict(lambda: {'likes': 0, 'dislikes': 0})

if os.path.exists('votes.json'):
  with open('votes.json', 'r') as file:
    votes = json.load(file)

# List of image URLs
images = os.listdir(os.path.join(os.path.dirname(__file__), 'static/images'))
random.shuffle(images)


@app.route('/', methods=['GET'])
def home():
  '''Returns the home page of the app'''
  return render_template('index.html')

@app.route('/refresh', methods=['GET'])
def refresh_site():
  '''Returns the refresh page of the app'''
  return render_template('refresh.html')

@app.route('/votes', methods=['GET'])
def get_votes():
  '''Returns the votes for each image as a JSON object'''
  return jsonify(votes)

@app.route('/api/vote/dislike', methods=['POST'])
def vote_dislike():
  '''
  Expects a query parameter 'imageIndex' which is the index of the image to vote on
  Increments the number of dislikes for the image at the given index
  '''
  current_image_index = request.args.get('imageIndex')
  image = images[current_image_index]
  votes[image]['dislikes'] += 1
  # Save votes to a file
  with open('votes.json', 'w') as file:
    json.dump(votes, file)
  return '', 200


@app.route('/api/vote/like', methods=['POST'])
def vote_like():
  '''
  Expects a query parameter 'imageIndex' which is the index of the image to vote on
  Increments the number of likes for the image at the given index
  '''
  current_image_index = request.args.get('imageIndex')
  image = images[current_image_index]
  votes[image]['likes'] += 1
  # Save votes to a file
  with open('votes.json', 'w') as file:
    json.dump(votes, file)
  return '', 200

@app.route('/api/image/tag', methods=['GET'])
def get_image_tag():
  '''
  Expects a query parameter 'imageIndex' which is the index of the image to display
  Returns the image tag for the current image
  '''
  image_index = request.args.get('imageIndex')
  image_url = f'static/images/{images[int(image_index)]}'
  return f'<img id="image" src="{image_url}" alt="Image">'


@app.route('/api/image/new_index', methods=['GET'])
def get_image_index():
  '''
  Returns html input element with name 'image-index' and value as the random index
  '''
  return f'<input type="text" id="image-index" value="{random.randint(0, len(images) - 1)}">'

@app.route('/api/refresh', methods=['POST'])
def refresh():
  '''Refreshes the images internally'''
  global images
  images = os.listdir(os.path.join(os.path.dirname(__file__), 'static/images'))
  random.shuffle(images)
  return '', 200


if __name__ == '__main__':
  app.run(host='0.0.0.0')
