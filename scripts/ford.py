#!/usr/bin/env python


__title__ = 'ford.py'
__version__ = '0.3.6'
__author__ = 'Mihir Singh (citruspi)'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Mihir Singh <me@mihirsingh.com>'


import os
import yaml
import markdown
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import argparse
from string import capwords


parser = argparse.ArgumentParser(description="ford.py builds on top of Flask to generate static blogs.", epilog='\n')
parser.add_argument("-m", choices=['build', 'serve'], dest="method", help="\tEither 'build' or 'serve' the content.", required=True)
parser.add_argument("-s", dest="source", help="\tPath to the content directory", required=True)

args = parser.parse_args()

source = os.getcwd()+'/'+args.source
method = args.method

config = yaml.load(open(source+'/config.yaml'))  # Load the config

DEBUG = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = source
FREEZER_DESTINATION = os.getcwd()+'/build'

app = Flask(__name__,
            static_folder=source+'/themes/' + config['theme'] + '/static',
            template_folder=source+'/themes/' + config['theme'] + '/templates')

app.config.from_object(__name__)

content = FlatPages(app)
freezer = Freezer(app)

pages = [c for c in content if (c.meta.get('type') == "page" and  # Filter out pages
                                c.meta.get('hidden') == None)]

posts = [c for c in content if (c.meta.get('type') == "post" and  # Filter out posts
                                c.meta.get('hidden') == None)]


@app.template_filter('markdown')
def md(s):
    """
    Define a 'markdown' filter for use by Jinja2.
    """
    return markdown.markdown(s, extensions=['extra'])


@app.template_filter('title')
def title(s):
    """
    Properly capitalize titles (for posts and pages).
    """
    return capwords(s)


@app.route('/')
def index():
    """
    Render the index.html page - just list posts. Additional
    content can be defined by the theme's template.
    """
    return render_template('index.html',
                           posts=posts,
                           pages=pages,
                           config=config)

if os.path.exists(source+'/themes/' + config['theme'] + '/templates/tag.html'):

    @app.route('/tag/<string:tag>/')
    def tag(tag):
        """
        Render the 'tag' page - list all the posts tagged with
        a certain string.
        """
        tagged = [p for p in posts if tag in p.meta.get('tags', [])]
        return render_template('tag.html',
                               posts=tagged,
                               tag=tag,
                               config=config)

if os.path.exists(source+'/themes/' + config['theme'] + '/templates/cat.html'):

    @app.route('/cat/<string:cat>/')
    def cat(cat):
        """
        Render the 'category' page - list all the posts filed under
        a certain category.
        """
        filed = [p for p in posts if cat in p.meta.get('category')]
        return render_template('cat.html',
                               posts=filed,
                               cat=cat,
                               config=config)

if os.path.exists(source+'/themes/' + config['theme'] + '/templates/author.html'):

    @app.route('/author/<string:author>/')
    def author(author):
        """
        Render the 'author' page - list all of the posts authored
        by a certain author.
        """
        authored = [p for p in posts if author in p.meta.get('author')]
        return render_template('author.html',
                               posts=authored,
                               author=author,
                               config=config)


@app.route('/<path:path>/')
def show(path):
    """
    Render a specified post. If it doesn't exist, 404.
    """
    c = content.get_or_404(path)

    if c.meta.get('type') == 'page':
        return render_template('page.html',
                               page=c,
                               pages=pages,
                               posts=posts,
                               config=config)
    else:
        return render_template('post.html',
                               post=c,
                               pages=pages,
                               posts=posts,
                               config=config)

if os.path.exists('themes/' + config['theme'] + '/templates/404.html'):

    @app.route('/404/')
    def fourohfour():
        """
        This is for use when generating the static site - the
        errorhandler may not be generated.

        This will not automatically work on a production server -
        it has to be defined in Apache, Nginx, etc.
        """
        return render_template('404.html',
                               config=config)

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Handle 404's when serving the site.
        """
        return render_template('404.html',
                               config=config)


@app.after_request
def after_request(response):
    response.headers.add('Built-With', 'ford.py')
    return response


if method == 'build':

    freezer.freeze()

elif method == 'serve':

    app.run(port=8000)
