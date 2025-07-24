MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'chats.middleware.CombinedMiddleware',               # Logs and time-based restriction
    'chats.middleware.OffensiveLanguageMiddleware',      # Chat message rate-limiting
    'chats.middleware.RolepermissionMiddleware',         # Role-based access control

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
