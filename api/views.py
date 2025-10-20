from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.db.models import Sum

from .models import User, WubiDict, WubiCategory, WubiWord
from .serializers import UserSerializer, WubiDictSerializer, WubiCategorySerializer, WubiWordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .token_utils import TokenUtils

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token = TokenUtils.generate_token(user.id)
            serializer = UserSerializer(user)
            data = serializer.data
            data['uid'] = user.id
            data['password'] = token

            # Aggregate word count from all user's dictionaries
            word_count_result = WubiDict.objects.filter(user=user).aggregate(total_word_count=Sum('word_count'))
            total_word_count = word_count_result['total_word_count'] or 0

            # Get the last sync time from the most recently updated dictionary
            latest_dict = WubiDict.objects.filter(user=user).order_by('-date_update').first()
            last_sync_time_dt = latest_dict.date_update if latest_dict else None
            last_sync_time_str = last_sync_time_dt.strftime('%Y-%m-%d %H:%M:%S') if last_sync_time_dt else None


            data['word_count'] = total_word_count
            data['last_sync_time'] = last_sync_time_str
            data['sync_count'] = 1

            data['username'] = data.get('email', '')
            data['nickname'] = data.get('email', '')
            response_data = {
                "success": True,
                "data": data,
                "message": "登录成功"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class WubiDictPullView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        if not title:
            return Response({"message": "Title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wubi_dict = WubiDict.objects.get(user=request.user, title=title)
            serializer = WubiDictSerializer(wubi_dict)
            response_data = {
                "success": True,
                "data": serializer.data,
                "message": "请求成功"
            }
            return Response(response_data)
        except WubiDict.DoesNotExist:
            response_data = {
                "success": True,
                "data": None,
                "message": "WubiDict not found"
            }
            return Response(response_data, status=status.HTTP_200_OK)

class WubiDictPushView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        title = request.data.get('title')
        if not title:
            return Response({"message": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        defaults = {
            'content': request.data.get('content'),
            'content_size': request.data.get('contentSize'),
            'word_count': request.data.get('wordCount'),
            'comment': request.data.get('comment', '')
        }
        
        # Filter out None values to avoid accidentally nulling fields
        defaults = {k: v for k, v in defaults.items() if v is not None}

        wubi_dict, created = WubiDict.objects.update_or_create(
            user=request.user,
            title=title,
            defaults=defaults
        )

        # After creating/updating, serialize the result to return consistent camelCase
        serializer = WubiDictSerializer(wubi_dict)
        data = serializer.data
        # 手动用 'T' 和 'Z' 覆盖 date_update 字段，确保是严格的 ISO 8601 格式
        data['date_update'] = wubi_dict.date_update.strftime('%Y-%m-%dT%H:%M:%SZ')

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        response_data = {
            "success": True,
            "data": data,
            "message": "上传成功"
        }
        return Response(response_data, status=status_code)


class WubiDictCheckBackupExistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_name = request.data.get('fileName') or request.query_params.get('fileName')
        if not file_name:
            return Response({"message": "fileName parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wubi_dict = WubiDict.objects.get(user=request.user, title=file_name)
            serializer = WubiDictSerializer(wubi_dict)
            data = serializer.data
            # 手动用 'T' 和 'Z' 覆盖 date_update 字段，确保是严格的 ISO 8601 格式
            data['date_update'] = wubi_dict.date_update.strftime('%Y-%m-%dT%H:%M:%SZ')
            data['word_count'] = wubi_dict.word_count  # 确保返回 word_count

            response_data = {
                "success": True,
                "data": data,
                "message": "Backup found."
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except WubiDict.DoesNotExist:
            default_data = {
                "id": None,
                "title": file_name,
                "content": "",
                "content_size": 0,
                "word_count": 0,
                "date_init": None,
                "date_update": None,  # This will become null in JSON
                "comment": "",
                "sync_count": 0,
                "user": request.user.id
            }
            response_data = {
                "success": True,
                "data": default_data,
                "message": "Backup not found."
            }
            return Response(response_data, status=status.HTTP_200_OK)


class WubiCategoryListView(generics.ListAPIView):
    queryset = WubiCategory.objects.all()
    serializer_class = WubiCategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'data': serializer.data,
            'message': 'Categories retrieved successfully.'
        }
        return Response(response_data)

class WubiCategoryCreateView(generics.CreateAPIView):
    queryset = WubiCategory.objects.all()
    serializer_class = WubiCategorySerializer
    permission_classes = [IsAdminUser]

class WubiCategoryUpdateView(generics.UpdateAPIView):
    queryset = WubiCategory.objects.all()
    serializer_class = WubiCategorySerializer
    permission_classes = [IsAdminUser]

class WubiCategoryDestroyView(generics.DestroyAPIView):
    queryset = WubiCategory.objects.all()
    serializer_class = WubiCategorySerializer
    permission_classes = [IsAdminUser]

class WubiWordListView(generics.ListAPIView):
    queryset = WubiWord.objects.all()
    serializer_class = WubiWordSerializer
    permission_classes = [IsAuthenticated]

class WubiWordCreateView(generics.CreateAPIView):
    queryset = WubiWord.objects.all()
    serializer_class = WubiWordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_init=self.request.user, user_modify=self.request.user)

class WubiWordUpdateView(generics.UpdateAPIView):
    queryset = WubiWord.objects.all()
    serializer_class = WubiWordSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user_modify=self.request.user)

class WubiWordDestroyView(generics.DestroyAPIView):
    queryset = WubiWord.objects.all()
    serializer_class = WubiWordSerializer
    permission_classes = [IsAuthenticated]