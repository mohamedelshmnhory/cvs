# from django.shortcuts import render
from rest_framework import generics, mixins
# from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status
# from django.http import Http404
# from django.shortcuts import get_object_or_404
# from django.db.models import Q
from api.mixins import UserQuerySetMixin, StaffEditorPermissionMixin
# from api.response import CustomResponse
from .models import Job, JobFilter
from .serializers import JobSerializer


class CustomPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 100


# Create your views here.
class JobListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer
    pagination_class = CustomPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'description']
    filterset_class = JobFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_term = self.request.query_params.get('search', None)
    #     if search_term:
    #         queryset = queryset.exclude(
    #         Q(name__exact=search_term) | Q(description__exact=search_term)
    #         )
    #     return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)  # Add this line
    #     if page is not None:  # Add this line
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return CustomResponse(status=True, data=serializer.data, message='',
    #                           status_code=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         # Save the account and return a success response
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         # Return an error response with the validation messages
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
    #     name = serializer.validated_data.get('name')
    #     description = serializer.validated_data.get('description') or None
    #     if description is None:
    #         description = name
    #     serializer.save(description=description)
    # send a Django signal

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Job.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user)


job_list_create_view = JobListCreateAPIView.as_view()


class JobDetailAPIView(
        # UserQuerySetMixin,
        StaffEditorPermissionMixin,
        generics.UpdateAPIView,
        generics.DestroyAPIView,
        generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # lookup_field = 'pk' ??


job_detail_view = JobDetailAPIView.as_view()


# class JobUpdateAPIView(
#     UserQuerySetMixin,
#     StaffEditorPermissionMixin,
#     generics.UpdateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     lookup_field = 'pk'
#
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if not instance.description:
#             instance.description = instance.name
#             ##
#
#
# job_update_view = JobUpdateAPIView.as_view()


# class JobDestroyAPIView(
#     UserQuerySetMixin,
#     StaffEditorPermissionMixin,
#     generics.DestroyAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     lookup_field = 'pk'
#
#     def perform_destroy(self, instance):
#         # instance
#         super().perform_destroy(instance)
#
#
# job_destroy_view = JobDestroyAPIView.as_view()


# class JobListAPIView(generics.ListAPIView):
#     '''
#     Not gonna use this method
#     '''
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

# job_list_view = JobListAPIView.as_view()


# class JobMixinView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     lookup_field = 'pk'
#
#     def get(self, request, *args, **kwargs):  # HTTP -> get
#         pk = kwargs.get("pk")
#         if pk is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         # serializer.save(user=self.request.user)
#         name = serializer.validated_data.get('name')
#         description = serializer.validated_data.get('description') or None
#         if description is None:
#             description = "this is a single view doing cool stuff"
#         serializer.save(description=description)
#
#     # def post(): #HTTP -> post
#
#
# job_mixin_view = JobMixinView.as_view()


# @api_view(['GET', 'POST'])
# def job_alt_view(request, pk=None, *args, **kwargs):
#     method = request.method
#
#     if method == "GET":
#         if pk is not None:
#             # detail view
#             obj = get_object_or_404(Job, pk=pk)
#             data = JobSerializer(obj, many=False).data
#             return Response(data)
#         # list view
#         queryset = Job.objects.all()
#         data = JobSerializer(queryset, many=True).data
#         return Response(data)
#
#     if method == "POST":
#         # create an item
#         serializer = JobSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             name = serializer.validated_data.get('name')
#             description = serializer.validated_data.get('description') or None
#             if description is None:
#                 description = name
#             serializer.save(description=description)
#             return Response(serializer.data)
#         return Response({"invalid": "not good data"}, status=400)
