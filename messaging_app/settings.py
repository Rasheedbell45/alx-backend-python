import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'messaging_db'),
        'USER': os.getenv('MYSQL_USER', 'messaging_user'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'your_password'),
        'HOST': 'db',  # Service name from docker-compose
        'PORT': '3306',
    }
}
