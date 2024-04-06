from datetime import datetime

from django.db.models import (
    Count,
    Min,
    Q,
    F,
    Value,
    Sum,
    OuterRef,
    Subquery,
    DurationField,
    ExpressionWrapper,
    DateTimeField,
    Case,
    When,
    BooleanField,
)
from django.db.models.functions import Concat

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
    latest_message_subquery = (
        UserMessage.objects.filter(room_id=OuterRef("id"))
        .order_by("-sent")
        .values("message")[:1]
    )

    queryset = (
        ChatRoom.objects.filter(Q(first_owner_id=pk) | Q(second_owner_id=pk))
        .annotate(
            latest_message_sent=Subquery(
                UserMessage.objects.filter(room_id=OuterRef("id"))
                .order_by("-sent")
                .values("sent")[:1],
                output_field=DateTimeField(),
            ),
            time_since=ExpressionWrapper(
                datetime.now() - F("latest_message_sent"),
                output_field=DurationField(),
            ),
            latest_message=Subquery(latest_message_subquery),
            should_return=Case(
                When(
                    Q(first_owner_id=pk)
                    & Q(latest_message_sent__lte=F("first_owner_deleted_time")),
                    then=False,
                ),
                When(
                    Q(second_owner_id=pk)
                    & Q(latest_message_sent__lte=F("second_owner_deleted_time")),
                    then=False,
                ),
                default=True,
                output_field=BooleanField(),
            ),
        )
        .filter(should_return=True)
        .order_by("-latest_message_sent")
    ).values(
        "should_return",
        "first_owner__username",
        "first_owner_id",
        "second_owner__username",
        "second_owner_id",
        "id",
        "latest_message",
        "latest_message_sent",
        "time_since",
    )
    print(queryset)
    return queryset


def get_messages_from_chat(request_user, second_user):
    queryset_rooms = (
        ChatRoom.objects.filter(
            first_owner_id=request_user, second_owner_id=second_user
        )
        | ChatRoom.objects.filter(first_owner_id=second_user, second_owner=request_user)
    ).first()

    # if one user deleted chat, then dont show old messages
    if f"{queryset_rooms.first_owner_id}" == request_user:
        queryset_messages = queryset_rooms.usermessage_set.filter(
            sent__gte=queryset_rooms.first_owner_deleted_time
        )
    elif f"{queryset_rooms.second_owner_id}" == request_user:
        queryset_messages = queryset_rooms.usermessage_set.filter(
            sent__gte=queryset_rooms.second_owner_deleted_time
        )
    else:
        queryset_messages = queryset_rooms.usermessage_set.all()

    return queryset_messages
