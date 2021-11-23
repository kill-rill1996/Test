from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

from .models import Comment, Post
from .permissions import IsPostOwnerPermission, IsCommentOwnerPermissionOrReadOnly
from .utils import create_comments_tree
from .serializers import PostModelSerializer, CommentSerializer, CommentCreateSerializer

from rest_framework.viewsets import ModelViewSet


class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostModelSerializer
    # permission_classes = []

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        comments = Comment.objects.filter(post=pk)
        comments_tree = create_comments_tree(comments)
        return Response(comments_tree)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            # chek if parent in request
            if serializer.data.get('parent'):
                # get post
                try:
                    post = Post.objects.get(id=serializer.data['post'])
                except Post.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                try:
                    # get parent and check its in that post
                    parent = Comment.objects.get(id=serializer.data['parent'])
                    post_comments = post.comments.all()
                    if parent not in post_comments:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    comment = Comment.objects.create(
                        post=post,
                        user=request.user,
                        text=serializer.data['text'],
                        is_child=serializer.data['is_child'],
                        parent=parent
                    )
                    comment.save()
                except Comment.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            # not parent in request
            else:
                try:
                    post = Post.objects.get(id=serializer.data['post'])
                except Post.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                comment = Comment.objects.create(
                    post=post,
                    user=request.user,
                    text=serializer.data['text'],
                    is_child=serializer.data['is_child']
                )
                comment.save()
            return Response(status=status.HTTP_201_CREATED)


class CommentMixinsView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsCommentOwnerPermissionOrReadOnly]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
