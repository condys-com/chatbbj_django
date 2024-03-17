from pathlib import Path

from django.http import HttpResponse, Http404
from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from .serializers import UserSerializer

from .serializers import ChatHistorySerializer

from django.http import JsonResponse
from .models import ChatHistory


def get_chat_history(request, username=None):
    # 直接查询所有聊天记录并按创建时间升序排序
    chat_history = ChatHistory.objects.filter(user=username).order_by('created_at')

    # 将查询结果转换为字典列表
    data = list(chat_history.values('user', 'message', 'response', 'created_at'))

    # 返回JSON响应
    return JsonResponse(data, safe=False)


class ChatHistoryView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ChatHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Chat history saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        content = {
            'user_id': request.user.id,  # 用户的 ID
            'username': request.user.username,  # 用户的用户名
            'text': 'Hello, %s!' % request.user.username,  # 用户的文本
            # 你可以添加更多信息
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


def download_file(request):
    file_path = Path(settings.MEDIA_ROOT) / 'zh_core_web_trf-3.7.2-py3-none-any.whl'  # 使用 Path 构造文件路径
    if file_path.exists():
        with file_path.open('rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{file_path.name}"'
            return response
    else:
        raise Http404("文件未找到")
