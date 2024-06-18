# IMAGE SWIPER

A mini tool to host your images on a website to be swiped to right (like) or left (dislike).

## Why?

With todays Cameras or fancy AI models you are able to produce an enormous amount of pictures or images.  
Who has time to whatch them all an rate them? I say everyone with a smartphone who likes doom-scrolling.  
Let AI generate a bunch of images, store them in `backend/api/static/images` and fire up this small tool in your local network and visit the site with your smartphone to start swiping your own images and discover the real diamonds!

## How?

0. Leave a star on the repository.
1. Clone repository or download it.
2. Add your images to the folder `backend/api/static/images`.
3. Install Python.
4. Install Poetry (eg `pip install poetry`).
5. Navigate your console to `backend` and run `poetry install`.
6. Run `poetry run python api/app.py`.

Above list is a suggestion. Feel free to use a different option to configure your python.

## What else?

Might be worth mentioning or just way too obvious, but showing images on smartphones heavily favors vertical images, while computers favor horizontal images.  
You might want to incorporate this already in your image generation...

## Security

Currently there is no differentiation between swipers and admins possible. Everyone has the same right to swipe, see the amount of votes and refresh the image library.

It might be recommended to host this in a local environment or comment out / remove certain pages and api calls.
