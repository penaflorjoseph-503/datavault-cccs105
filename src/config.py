"""
config.py - Application configuration
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production-please')

    # MySQL / XAMPP settings — edit these to match your setup
    MYSQL_HOST     = os.environ.get('MYSQL_HOST',     'localhost')
    MYSQL_PORT     = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER     = os.environ.get('MYSQL_USER',     'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')        # XAMPP default is empty
    MYSQL_DB       = os.environ.get('MYSQL_DB',       'CCCS105')

    # Number of rows per page
    PER_PAGE = 10
