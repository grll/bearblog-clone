import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
