#########################################
# ford.py v0.3.1
# Mihir Singh (citruspi)
# Distributed under the MIT license
#########################################

import os
import sys #Used for parsing arguments - build v. run
import yaml #Used for parsing the config.yml file
import markdown #Used for Jinja2's filter
from flask import Flask,render_template # Do you need to ask?
from flask_flatpages import FlatPages #Used to generate posts from markdown
from flask_frozen import Freezer #Used to generate the static site

config = yaml.load(open('content/config.yaml')) #Load the config

DEBUG = True # For debugging - won't show up on static site
FLATPAGES_EXTENSION = '.md' #Posts are designated by a '.md' extension
FLATPAGES_ROOT = 'content' #Posts are located in the 'content' directory

app = Flask(__name__,
            static_folder='themes/'+config['theme']+'/static',
            template_folder='themes/'+config['theme']+'/templates')
"""
Set the location of the static and template
directory to those in the specified theme
directory. Theme specified in config.yaml
"""

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
                            pages=pages,
                            config=config)

if os.path.exists('themes/'+config['theme']+'/templates/tag.html'):

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

if os.path.exists('themes/'+config['theme']+'/templates/cat.html'):
    
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

if os.path.exists('themes/'+config['theme']+'/templates/author.html'):

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

if os.path.exists('themes/'+config['theme']+'/templates/404.html'):

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

    print sys.argv

    if len(sys.argv) == 3 and os.path.isdir(sys.argv[2]) and os.path.exists(sys.argv[2]+'/config.yaml'):

        if sys.argv[1] == ("-h" or "--help" or "help" or "h"):
            """
            Present options
            """
            print "python ford.py build <folder_name>\tBuild the static site"
            print "python ford.py serve <folder_name>\tRun the site locally (for debugging)"
        elif sys.argv[1] == "build":
            """
            Build the static version
            """
            freezer.freeze()
        elif sys.argv[1] == "serve":
            """
            Serve the site locally - good for debugging.
            """
            app.run(port=8000)

        else:
            print "\nError Code -3492. Universe will now implode.\n"
            print "Just kidding. But if you need help, try python ford.py -h"

    else:    
        print "Error Code -3492. Universe will now implode.\n"
        print "Just kidding. But if you need help, try python ford.py -h"
