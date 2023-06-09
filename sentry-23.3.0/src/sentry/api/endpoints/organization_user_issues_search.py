from rest_framework.request import Request
from rest_framework.response import Response

from sentry import tagstore
from sentry.api.base import EnvironmentMixin, region_silo_endpoint
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models.group import GroupSerializer
from sentry.models import EventUser, Group, OrganizationMemberTeam, Project


@region_silo_endpoint
class OrganizationUserIssuesSearchEndpoint(OrganizationEndpoint, EnvironmentMixin):
    def get(self, request: Request, organization) -> Response:
        email = request.GET.get("email")

        if email is None:
            return Response(status=400)

        limit = int(request.GET.get("limit", 100))

        # limit to only teams user has opted into
        project_ids = list(
            Project.objects.filter(
                teams__in=OrganizationMemberTeam.objects.filter(
                    organizationmember__user_id=request.user.id,
                    organizationmember__organization=organization,
                    is_active=True,
                ).values("team")
            ).values_list("id", flat=True)[:1000]
        )

        event_users = list(EventUser.objects.filter(email=email, project_id__in=project_ids)[:1000])

        if event_users:
            groups = Group.objects.filter(
                id__in=tagstore.get_group_ids_for_users(
                    project_ids=list({e.project_id for e in event_users}),
                    event_users=event_users,
                    limit=limit,
                    tenant_ids={"organization_id": organization.id},
                )
            ).order_by("-last_seen")[:limit]
        else:
            groups = []

        context = serialize(
            list(groups),
            request.user,
            GroupSerializer(environment_func=self._get_environment_func(request, organization.id)),
        )

        return Response(context)
