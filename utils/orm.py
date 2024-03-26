from django.db.models import Count, Min, Q, Value, Sum, Max
from django.db.models.functions import Concat

from pages.models import UserMessage


# is used to specify if post have attached image, if do then, get how many,
# and then get first image path.
# Chceck if post is not deleted
def get_post(querryset, **conditions):
    query = querryset.objects

    if "deleted" in conditions:
        deleted_query = conditions.get("deleted")
    else:
        deleted_query = False

    if "id" in conditions:
        try:
            query = querryset.objects.filter(id=conditions.get("id"))
        except:
            return None

    if "owner_id" in conditions:
        try:
            query = querryset.objects.filter(owner_id=conditions.get("owner_id"))
        except:
            return None

    result = (
        query.annotate(
            image_first=Min("postimage__image"),
            username=Concat("owner__username", Value("")),
            reactions=Sum("reaction__reaction"),
        )
        .values(
            "added",
            "content",
            "description",
            "id",
            "image_first",
            "owner_id",
            "postimage",
            "reactions",
            "username",
        )
        .order_by("-added")
        .filter(deleted=deleted_query)
    )
    return result


def get_user_info(queryset, pk):
    queryset = (
        queryset.objects.filter(id=pk, deleted=False)
        .annotate(
            post_count=Count("post", filter=Q(post__owner_id=pk, post__deleted=False))
        )
        .first()
    )
    return queryset


def get_messages_headers(pk):
    queryset = UserMessage.objects.filter(from_user_id=pk) | UserMessage.objects.filter(
        to_user_id=pk
    )
    queryset = (
        queryset.values("from_user_id", "to_user_id")
        .order_by("-sent")
        .annotate(sent=Max("sent"))
    ).values("from_user_id", "to_user_id", "message", "sent")

    print(dir(queryset))
    print(queryset)
    return queryset
