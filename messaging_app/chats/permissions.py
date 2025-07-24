from rest_framework import permissions

class IsAuthenticatedParticipant(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are
    participants of the conversation to access or modify messages.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow GET, POST for participants only
        if request.method in permissions.SAFE_METHODS + ("POST",):
            return request.user == obj.sender or request.user == obj.receiver

        # Allow PUT, PATCH, DELETE only if user is participant
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user == obj.sender or request.user == obj.receiver

        return False
