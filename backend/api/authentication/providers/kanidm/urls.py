from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .views import KanidmOpenIDConnectProvider

urlpatterns = default_urlpatterns(KanidmOpenIDConnectProvider)
