MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.NoSelfLinksMiddleware',
)

INSTALLED_APPS = (
    'simpleopenid',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'simpleopenid.auth.backends.OpenIDBackend',
)

# Set to True if you know what are you doing.
SIMPLEOPENID_FORCE_PRETTY_FORM = False

