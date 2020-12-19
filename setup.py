from distutils.core import setup
import py2exe
import os
import pygubu
import importlib
import json
import requests
import func
import anilist_request

setup(console=['main_win.py'])