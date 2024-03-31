from django.db.models import Count, Min, Q, Value, Sum, OuterRef, Subquery
from django.db.models.functions import Concat, Coalesce

from pages.models import ChatRoom, UserMessage


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
            reactions=Sum("reaction__reaction", default=0),
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


def get_messages_headers(user):
    # get last message from every room
    last_messages_subquery = UserMessage.objects.filter(
        room_id=OuterRef("id")
    ).order_by("-sent")
    last_message = last_messages_subquery.values("message")[:1]

    # Teraz zastosuj to podzapytanie do Twojego głównego zapytania
    # queryset = ChatRoom.objects.filter(first_owner_id=user) | ChatRoom.objects.filter(
    #     second_owner_id=user
    # ).annotate(last_message=Subquery(last_message)).values("last_message").filter(
    #     last_message__isnull=False
    # )
    values_tuple = (
        "first_owner",
        "id",
        "last_message",
        "second_owner",
    )
    queryset = (
        ChatRoom.objects.filter(first_owner_id=user)
        .annotate(
            last_message=Subquery(last_message),
            second_owner_username=Coalesce(
                Concat("second_owner__username", Value("")), ""
            ),
            first_owner_username=Coalesce(
                Concat("first_owner__username", Value("")), ""
            ),
        )
        .filter(last_message__isnull=False)
        .values(
            "first_owner_username",
            "second_owner_username",
            "first_owner",
            "id",
            "last_message",
            "second_owner",
        )
    ).union(
        ChatRoom.objects.filter(second_owner_id=user)
        .annotate(
            last_message=Subquery(last_message),
            second_owner_username=Coalesce(
                Concat("second_owner__username", Value("")), ""
            ),
            first_owner_username=Coalesce(
                Concat("first_owner__username", Value("")), ""
            ),
        )
        .filter(last_message__isnull=False)
        .values(
            "first_owner_username",
            "second_owner_username",
            "first_owner",
            "id",
            "last_message",
            "second_owner",
        )
    )

    return queryset

    # queryset = (
    #     queryset.annotate(
    #         first_username=Concat("usermessage__first_owner", Value("")),
    #         second_username=Concat("usermessage__second_owner", Value("")),
    #         time_since=ExpressionWrapper(
    #             datetime.now() - F("sent"), output_field=DurationField()
    #         ),
    #     )
    #     .values(
    #         "time_since",
    #         "message",
    #         "sent",
    #         "from_username",
    #         "to_username",
    #     )
    #     .distinct()
    # )


def get_messages_from_chat(request_user, second_user):
    queryset = (
        ChatRoom.objects.filter(first_owner_id=request_user, second_owner=second_user)
        | ChatRoom.objects.filter(first_owner_id=second_user, second_owner=request_user)
    ).first()

    queryset_res = queryset.usermessage_set.all()

    return queryset_res
