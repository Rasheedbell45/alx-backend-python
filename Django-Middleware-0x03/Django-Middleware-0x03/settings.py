MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Custom middleware
    'chats.middleware.CombinedMiddleware',               # Logs and time-based restriction
    'chats.middleware.OffensiveLanguageMiddleware',      # Chat message rate-limiting
    'chats.middleware.RolePermissionMiddleware',         # Role-based access control

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
