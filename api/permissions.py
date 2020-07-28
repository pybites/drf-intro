from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class AccountPermissions(permissions.BasePermission):
    """
    Allow for new account creation when logged out
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # only logged out users or super users can create accounts
        if request.method == 'POST':
            return not request.user.is_authenticated or request.user.is_superuser
        # put and delete you need to be logged in
        # get permissions are further locked down in get_queryset (views.py)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (request.user.is_superuser or request.user.is_authenticated
            and obj == request.user):
            return True
        return False
