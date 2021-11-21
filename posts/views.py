from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

from .models import Comment, Post
from .permissions import IsPostOwnerPermission
from .utils import create_comments_tree
from .serializers import PostModelSerializer, CommentSerializer

from rest_framework.viewsets import ModelViewSet

# def index_view(request):
#     comments = Post.objects.first().comments.all()
#     print(comments)
#     result = create_comments_tree(comments)
#     print(result)
#     return render(request, 'index.html', {'comments_tree': result})


class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostModelSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'delete']:
            permission_classes = [IsAuthenticated, IsPostOwnerPermission]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Post.objects.all()


class CommentView(APIView):
    permission_classes = []

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comments_tree = create_comments_tree(post.comments.all())
        return Response(comments_tree)

    def post(self, request, pk):
        try:
            data = request.data
            data['post'] = pk
            comment = CommentSerializer(data=request.data)
            if comment.is_valid():
                comment.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        except AssertionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

