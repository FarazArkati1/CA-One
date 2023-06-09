from django.conf.urls import url

from .webhooks import GithubIntegrationsWebhookEndpoint, GithubWebhookEndpoint

urlpatterns = [
    url(
        r"^organizations/(?P<organization_id>[^\/]+)/webhook/$",
        GithubWebhookEndpoint.as_view(),
    ),
    url(
        r"^installations/webhook/$",
        GithubIntegrationsWebhookEndpoint.as_view(),
    ),
]
