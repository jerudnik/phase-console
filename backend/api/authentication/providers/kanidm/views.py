import os
from urllib.parse import urljoin, urlparse
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.socialaccount import providers
from api.authentication.adapters.generic.provider import GenericOpenIDConnectProvider
from api.authentication.adapters.generic.views import GenericOpenIDConnectAdapter

# Kanidm OIDC discovery is per-client: KANIDM_URL is the per-client issuer base,
# e.g. https://auth.example.com/oauth2/openid/<client_id>
KANIDM_URL = os.getenv("KANIDM_URL", "")

OIDC_DISCOVERY_URL = urljoin(
    KANIDM_URL + "/",
    ".well-known/openid-configuration",
)


def _issuer_relative(path):
    # userinfo + JWKS live under the per-client issuer base
    return urljoin(KANIDM_URL + "/", path)


def _host_root(path):
    # token + authorize live at the Kanidm host root, not under the issuer base
    if not KANIDM_URL:
        return ""
    parsed = urlparse(KANIDM_URL)
    return f"{parsed.scheme}://{parsed.netloc}{path}"


class KanidmOpenIDConnectProvider(GenericOpenIDConnectProvider):
    id = "kanidm"
    name = "Kanidm OIDC"


class KanidmOpenIDConnectAdapter(GenericOpenIDConnectAdapter):
    provider_id = KanidmOpenIDConnectProvider.id
    oidc_config_url = OIDC_DISCOVERY_URL
    # Fallback only — the adapter prefers the OIDC discovery document. Kanidm
    # serves token/authorize at the host root and userinfo/JWKS under the
    # per-client issuer base.
    default_config = {
        "access_token_url": _host_root("/oauth2/token"),
        "authorize_url": _host_root("/ui/oauth2"),
        "profile_url": _issuer_relative("userinfo"),
        "jwks_url": _issuer_relative("public_key.jwk"),
        "issuer": KANIDM_URL,
    }


oauth2_login = OAuth2LoginView.adapter_view(KanidmOpenIDConnectAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(KanidmOpenIDConnectAdapter)

# Register the provider
providers.registry.register(KanidmOpenIDConnectProvider)

provider_classes = [KanidmOpenIDConnectProvider]
