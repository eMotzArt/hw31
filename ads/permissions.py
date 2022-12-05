from rest_framework import permissions

from ads.models import Advertisement
from users.models import User


class IsAuthor(permissions.BasePermission):
    message = "You are not author for this advertisement"

    def has_permission(self, request, view):
        advertisement_id = request.parser_context.get('kwargs').get('pk')
        advertisement = Advertisement.objects.get(id=advertisement_id)
        if request.user.id == advertisement.author_id:
            return True
        return False

class IsModerator(permissions.BasePermission):
    message = "You are not moderator"
    def has_permission(self, request, view):
        if request.user.role == User.MODERATOR:
            return True
        return False

class IsAdmin(permissions.BasePermission):
    message = "You are not administrator"
    def has_permission(self, request, view):
        if request.user.role == User.ADMIN:
            return True
        return False


