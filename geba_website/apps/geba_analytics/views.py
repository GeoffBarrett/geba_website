from django.shortcuts import render
from .models import ObjectViewed
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .utils import check_analytics_rights

# Create your views here.

''''''


class AnalyticsView(View):
    template_name = 'geba_analytics/analytics.html'

    def get(self, request, *args, **kwargs):
        request = check_analytics_rights(request)

        return render(request, self.template_name)


class AnalyticsData(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        viewed_today = ObjectViewed.objects.today()

        anonymous_views = viewed_today.filter(user=None).count()

        data = {
            'labels': ['Viewed Today', 'Anonymous Views'],
            'analytics_data': [viewed_today.count(), anonymous_views]
        }

        return Response(data)



