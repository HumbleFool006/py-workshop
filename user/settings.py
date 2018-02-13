"""
  Login module setings
"""
LOGIN_REDIRECT_URL = 'post_list'
LOGIN_URL = '/login/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '303674303490835'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '94b65d4d2dd254db0a4a4d9f1d162ee5'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email'
}
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'user.utils.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1076263671109-t6g8gq2mqi3vp94hbjr5cuckv0guu2g2.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'IhhZHefSRBPDnvQBC7g_OVen'
