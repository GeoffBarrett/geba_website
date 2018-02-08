from django.core.exceptions import PermissionDenied


def check_project_rights(request):
    if request.user.is_staff or request.user.is_superuser:
        request.can_project = True
        request.can_view_all = True
        return request

    # return HTTP 403 Back to user
    raise PermissionDenied
