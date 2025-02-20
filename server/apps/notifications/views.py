from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notifications
from .serializers import NotificationsSerializer, ReadNotificationsSerializer


class NotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Notifications.objects.filter(
            Q(send_user=user) | Q(receive_user=user)
        ).order_by("-send_time")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["send_user"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=ReadNotificationsSerializer,
    )
    def read(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        opposite_user = serializer.validated_data.get("opposite_user")
        current_user = request.user.id
        if opposite_user == current_user:
            return Response(
                {"detail": "不能对自身进行操作"}, status=status.HTTP_400_BAD_REQUEST
            )
        print(current_user, opposite_user)
        updated_count = Notifications.objects.filter(
            Q(send_user=current_user, receive_user=opposite_user)
            | Q(send_user=opposite_user, receive_user=current_user),
            read_status="unread",
        ).update(read_status="read")

        return Response(
            {"detail": f"已经将{updated_count}条消息标记为已读"}, status=status.HTTP_200_OK
        )
