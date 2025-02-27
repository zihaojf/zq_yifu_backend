from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import MoveRecord
from .serializers import MoveRecordSerializer


class MoveRecordViewSet(viewsets.ModelViewSet):
    queryset = MoveRecord.objects.all()
    serializer_class = MoveRecordSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["move_user"] = self.request.user.id
        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        user = request.user
        move_records = MoveRecord.objects.filter(move_user=user)

        paired_records = []
        unpaired_records = []

        for record in move_records:
            # 如果是初始空闲状态，直接添加到未配对记录
            if record.is_initial:
                unpaired_records.append(
                    {
                        "move_record": MoveRecordSerializer(record).data,
                        "message": "初始空闲状态，无需挪车",
                    }
                )
                continue

            # 查找成对的记录
            paired_record = MoveRecord.objects.filter(
                moved_user=record.move_user,
                move_vehicle_id=record.move_vehicle_id,
                move_time__gt=record.move_time,  # 确保被挪车记录发生在主动挪车之后
            ).first()

            if paired_record:
                paired_records.append(
                    {
                        "move_record": MoveRecordSerializer(record).data,
                        "paired_record": MoveRecordSerializer(
                            paired_record
                        ).data,
                    }
                )
            else:
                unpaired_records.append(
                    {
                        "move_record": MoveRecordSerializer(record).data,
                        "message": "未找到对应的挪车记录",
                    }
                )

        response_data = {
            "paired_records": paired_records,
            "unpaired_records": unpaired_records,
        }

        return Response(response_data, status=status.HTTP_200_OK)
