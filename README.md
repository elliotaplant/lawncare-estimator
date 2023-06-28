# README

This is the [Flask](http://flask.pocoo.org/) [quick start](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application) example for [Render](https://render.com).

The app in this repo is deployed at [https://flask.onrender.com](https://flask.onrender.com).

## Deployment

Follow the guide at https://render.com/docs/deploy-flask.

## Getting Started Notes

Code I ran when I set this project up:

```
python3 -m venv venv-lawncare
source venv-lawncare/bin/activate
pip3 install -r requirements.txt
```

To develop locally:
```
gunicorn app:app
```