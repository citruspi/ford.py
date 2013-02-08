## ford.py, (Yet Another) Static Blog Generator in Python

### Introduction

`ford.py` is based on the principle that we shouldn't

> reinvent the wheel.

So, it makes use of existing code libraries, in this case `flask` and flask extensions, to both serve and build static versions of websites while maintaining a small footprint.

*Note: As of this moment, ford.py only works with "posts", not "pages." So really, it's limited to blogs.*

### For Zeus' sake, WHY ANOTHER STATIC SITE GENERATOR?

For a few reasons actually. Compared to other solutions, `ford.py` is tiny. The project folder (including the default theme) is ~164 KB. `ford.py` itself is 8 KB. And, that's not 8 KB of pure code. As per `pylint`:

##### Raw Metrics of ford.py

|type      |number |%     |
|:---------|:------|:-----|
|code      |69     |48.59 |
|docstring |54     |38.03 |
|comment   |5      |3.52  |
|empty     |14     |9.86  |

So, less than 4 KB of code. That's pretty small for a static site generator. 

In addition, it uses popular packages and modules, so the code is _familiar_. For that reason, its easily extendable. But, more on that later.

### Quickstart

So, you're interested in using `ford.py`, huh? Well, let's get started!

Here are a few steps to get you on the way:

1. Clone the project:

	Github:

		$ git clone http://github.com/citruspi/ford.py.git

	Bitbucket:

		$ git clone http://bitbucket.org/citruspi/ford.py.git

2. Install requirements/dependencies:

		$ cd ford.py
		$ pip install -r requirements.txt

3. Take her for a spin:

		$ python ford.py serve

Now, if you open `127.0.0.1:8000` in your browser, you should be greeted with something like:

![](http://i.imgur.com/uiMBP8r.png)

If that's what you have, you're golden.

### Options

There are two ways to use `ford.py`:

	$ python ford.py serve

\- or -

	$ python ford.py build

`Serve` will serve the blog locally, for debugging. `Build` will generate a static version in a `build` folder.

### Posts

`ford.py` looks for content, or rather posts, in the `posts` directory. Posts should written in `Markdown` and end in `.md` extensions.

__Any files which do not have an `.md` extension will not be recognized as posts. This is actually useful - save a file with another extension to save it as a draft.__

The layout for a post should look like this:

	title: hello world 
	date: 2013-01-27 
	tags: [hello, stuff] 
	author: mark twain 
	category: general

	And then the body of the post here.....

Every post should have basic meta like `title`, `date`, etc. Users (you?) can add on any tags you want to the meta. 

So, you could add 

	sticky: False

to posts you want. 

Writing a food blog? Add 

	ingredients: [flour, milk, sugar]

to the meta.

__All tags are handled by the theme templates - some templates may ignore extra tags, some may ignore the basic tags, and some may require extra tags. `ford.py` simply provides the meta and body to the templates.__

### Themes

`ford.py` can use different themes - you have to provide them. A default theme, a port of orderedlist's minimal, is provided with the `ford.py` source.

Additional themes can be created by anybody easily.

All themes __must__ be placed in the `themes` directory. Each theme should have a `templates` and `static` directory - even if they are empty. In addition, they must contain certain files (even if they are blank):

	* 404.html
	* author.html
	* cat.html
	* index.html
	* page.html
	* tag.html

The `minimal` theme directory looks like this:

	$ ls -al themes/minimal/templates

	-rw-r--r--   1 mihir  staff   238 Jan 27 18:02 404.html
    -rw-r--r--   1 mihir  staff   225 Jan 28 23:22 _list.html
    -rw-r--r--   1 mihir  staff   203 Jan 28 23:22 author.html
    -rw-r--r--   1 mihir  staff  2224 Jan 29 21:52 base.html
    -rw-r--r--   1 mihir  staff   200 Jan 28 23:23 cat.html
    -rw-r--r--   1 mihir  staff   455 Jan 28 23:23 index.html
    -rw-r--r--   1 mihir  staff  2717 Jan 28 23:27 page.html
    -rw-r--r--   1 mihir  staff   195 Jan 28 21:02 tag.html

Themes __must__ be templated with `Jinja2`.

Take a look at the minimal theme for an idea on how themes work.

### config.yaml

The `config.yaml` requires one thing only - `theme`. Everything else included is used by the theme itself and not `ford.py` and should be defined in the theme's description.

The `minimal` theme asks for:

	* title
	* about //description
	* post_blog //what should come after the web blog on the index
	* footer 
	* gauges_id // for gaug.es analytics
	* disqus_id // for disqus commenting system

For a valid `config.yaml` for the `minimal` theme, take a look at the one included in this repository.

### Additional Information

As of now, there are three things which you should be aware of.

1. Upon installation, __Markdown extra__ features like __tables__ will not render.

	The problem lies in that `Flask-FlatPages` does not pass `extras` to the `Markdown` package by default.

	The solution is to modify your installation of `Flask-FlatPages`. You have to change lines 34-40 of `__init__.py`.

	Change:

		try:
        	import pygments
    	except ImportError:
	        extensions = []
	    else:
    	    extensions = ['codehilite']
    	return markdown.markdown(text, extensions)

	To:

		extensions = ['extra']
    
    	try:
        	import pygments
    	except ImportError:
       		pass
    	else:
        	extensions.append('codehilite')
        
    	return markdown.markdown(text, extensions)

	And save!

2. The URL's in the static version of the blog will be absolute, not relative. 

	So, if you just double-click `index.html` in the `build` directory, the page will show up without CSS, JS, etc.

	The static site __must__ be served by an HTTP server.

3. When the blog is being `served locally` for debugging, 404's will automatically load the `404.html` page. The static site will not. You will have to set the error page in your HTTP server (Nginx, Apache, etc.) configuration.

	For example, in my Nginx config, I had to add 

		error_page 404 /404;

	to the server.

### Extending

As mentioned previously, `ford.py` is written on top of `flask` and other flask extensions. 

Take a look at the source for the `ford.py` file, you'll find it familiar. You should be able to extend it as easily as any other `flask` project.

### Credits

_If you contribute, just add your name here and submit a pull request._

Authors/Contributors:

* Mihir Singh

Shout out to [@remino](https://github.com/remino). 

### Contributing

Any contribution is welcome. Just submit a pull request. ;)

### License

`ford.py` is distributed under the MIT License:

	Copyright © 2012 Mihir Singh <me@mihirsingh.com>

	Permission is hereby granted, free of charge, to any person obtaining a copy of 
	this software and associated documentation files (the “Software”), to deal in 
	the Software without restriction, including without limitation the rights to 
	use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
	the Software, and to permit persons to whom the Software is furnished to do 
	so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all 
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY 
	KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
	WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
	PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
	DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
	CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
	IN THE SOFTWARE.
