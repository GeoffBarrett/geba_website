from django.core.exceptions import PermissionDenied


def get_client_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


def check_analytics_rights(request):
    if request.user.is_staff or request.user.is_superuser:
        request.can_blog = True
        request.can_view_all = True
        return request

    # return HTTP 403 Back to geba_auth
    raise PermissionDenied
