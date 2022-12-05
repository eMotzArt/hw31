from rest_framework import permissions

from selections.models import Collection


class IsCollectionOwner(permissions.BasePermission):
    message = "You are not an owner"

    def has_permission(self, request, view):
        collection_id = request.parser_context.get('kwargs').get('pk')
        collection = Collection.objects.get(id=collection_id)
        if request.user.id == collection.owner_id:
            return True
        return False
