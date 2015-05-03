import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from travelgraph import app

# Routing for all pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/login')
@app.route('/signup')
@app.route('/all_questions')
@app.route('/all_tags')
@app.route('/question')
@app.route('/ques/<ques_id>')
@app.route('/blog')
@app.route('/tag/<tag>')
def basic_pages(*args, **kwargs):
        return make_response(open('travelgraph/templates/index.html').read())

