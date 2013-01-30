#########################################
# ford.py v0.1
# Mihir Singh (citruspi)
# Distributed under the MIT license
#########################################

import sys #Used for parsing arguments - build v. run
import yaml #Used for parsing the config.yml file
import markdown #Used for Jinja2's filter
from flask import Flask,render_template # Do you need to ask?
from flask_flatpages import FlatPages #Used to generate posts from markdown
from flask_frozen import Freezer #Used to generate the static site

config = yaml.load(open('config.yaml')) #Load the config

DEBUG = True # For debugging - won't show up on static site
FLATPAGES_EXTENSION = '.md' #Posts are designated by a '.md' extension
FLATPAGES_ROOT = 'posts' #Posts are located in the 'posts' directory

app = Flask(__name__,
            static_folder='themes/'+config['theme']+'/static',
            template_folder='themes/'+config['theme']+'/templates')
"""
Set the location of the static and template
directory to those in the specified theme
directory. Theme specified in config.yaml
"""

app.config.from_object(__name__)
posts = FlatPages(app)
freezer = Freezer(app)

@app.template_filter('markdown')
def md(s):
    """
    Define a 'markdown' filter for use by Jinja2.
    It will be used for generating HTML from markdown
    in the config for use by the template only.
    (Posts themselves will be generated with FlatPages)
    """
    return markdown.markdown(s, extensions=['extra'])

@app.route('/')
def index():
    """
    Render the index.html page - just list posts. Additional
    content (post_blog) can be defined by the theme's template.
    """
    return render_template('index.html', 
                            posts=posts, 
                            config=config)

@app.route('/tag/<string:tag>/')
def tag(tag):
    """
    Render the 'tag' page - list all the posts tagged with
    a certain string. 
    (If a 'tag.html' template is not defined in the theme,
    delete the entire route - attempting to render it will
    cause an error on run.)
    """
    tagged = [p for p in posts if tag in p.meta.get('tags', [])]
    return render_template('tag.html', 
                            posts=tagged, 
                            tag=tag, 
                            config=config)

@app.route('/cat/<string:cat>/')
def cat(cat):
    """
    Render the 'category' page - list all the posts filed under
    a certain category.
    (If a 'cat.html' template is not defined in the theme, 
    delete the entire route - attempting to render it will
    cause an error on run.)
    """
    filed = [p for p in posts if cat in p.meta.get('category')]
    return render_template('cat.html', 
                            posts=filed, 
                            cat=cat, 
                            config=config)

@app.route('/author/<string:author>/')
def author(author):
    """
    Render the 'author' page - list all of the posts authored 
    by a certain author.
    (If an 'author.html' template is not defined in the theme,
    delete the entire route - attempting to render it will
    cause an error on run.)
    """
    authored = [p for p in posts if author in p.meta.get('author')]
    return render_template('author.html', 
                            posts=authored, 
                            author=author, 
                            config=config)

@app.route('/<path:path>/')
def post(path):
    """
    Render a specified post. If it doesn't exist, 404.
    """
    post = posts.get_or_404(path)
    return render_template('page.html', 
                            post=post, 
                            config=config)

@app.route('/404/')
def fourohfour():
    """
    This is for use when generating the static site - the
    errorhandler may not be generated.
    
    This will not automatically work on a production server -
    it has to be combined with Apache, Nginx, etc.
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

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        """
        Present options
        """
        print "python ford.py build\tBuild the static site"
        print "python ford.py serve\tRun the site locally (for debugging)"
    elif len(sys.argv) > 1 and sys.argv[1] == "build":
        """
        Build the static version
        """
        freezer.freeze()
    elif len(sys.argv) > 1 and sys.argv[1] == "serve":
        """
        Serve the site locally - good for debugging.
        """
        app.run(port=8000)
    else:    
        print "Error Code -3492. Universe will now implode."