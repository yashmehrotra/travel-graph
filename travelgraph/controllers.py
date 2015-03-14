import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from travelgraph import app

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/login')
@app.route('/blog')
def basic_pages(**kwargs):
        return make_response(open('travelgraph/templates/index.html').read())
