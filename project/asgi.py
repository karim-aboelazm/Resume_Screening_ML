"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_asgi_application()
