from distutils.core import setup

long_description = \
'''ford.py is a static site generator written in Python.

Documentation and usage can be found on the ford.py_ page on Github.

.. _ford.py: http://github.com/citruspi/ford.py
'''

setup(
    name='ford.py',
    version='0.3.6',
    author='Mihir Singh',
    author_email='me@mihirsingh.com',
    url='http://pypi.python.org/pypi/ford.py/',
    license='MIT License',
    description='(Yet Another) Static Site Generator in Python..',
    long_description=long_description,
    scripts=['scripts/ford.py',],
    install_requires=[
                        'Flask',
                        'Flask-FlatPages',
                        'Frozen-Flask',
                        'Jinja2',
                        'Markdown',
                        'PyYAML',
                        'Pygments',
                        'Werkzeug',
                        'wsgiref'
                     ]
)