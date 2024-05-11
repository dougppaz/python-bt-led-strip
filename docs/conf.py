import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Python LED Strip Bluetooth Controller API'
copyright = '2024, Douglas Paz'
author = 'Douglas Paz'

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
