# py-workshop

## Setting up virtual environment

Command to be executed : bash setup_venv.sh

## Configuring facebook application

### FACEBOOK

    go to https://developers.facebook.com
    my apps -> create new app
    fill displayname input field `app name` then click on create app id
    settings --> add platform
    fill website input field as `http://localhost:8000` then save
    copy, APP ID and APP SECRET

    open mm/user/settings.py
    
    SOCIAL_AUTH_FACEBOOK_KEY = 'APP ID'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'APP SECRET'

### GOOGLE

    go to console.developers.google.com
    click on enable apis and service
    type google plus 
    click enable
    credentials -> oauth consent screen
    Authorized JavaScript origins = http://localhost:8000
    Authorized redirect URIs = http://localhost:8000/oauth/complete/google-oauth2/
    copy Client ID, Client secret
    
    open mm/user/settings.py
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'Client ID'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Client secret'

## Migration

    Creating application specific database changes.

    ./manage.py migrate

## Run application

    ./manage.py runserver

    connect browser to http://localhost:8000
