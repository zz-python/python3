from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyModelForm
from django.views.decorators.csrf import csrf_exempt
from .models import MyModel
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def hello_view(request):
    return HttpResponse("Hello, Django!")

@csrf_exempt
def create_model(request):
    # 如果是 POST 请求，处理表单提交
    form = MyModelForm(request.POST)
    form.save()    
    return HttpResponse("saved!")

def model_list_json(request):
    models = MyModel.objects.all()
    data = [model.to_dict() for model in models]
    return JsonResponse(data, safe=False)    

class YourApiView(APIView):
    @swagger_auto_schema(
        operation_description="接口说明，权限说明",
        responses={
            200: "Success response description",
            400: "Bad request description",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'key1': openapi.Schema(type=openapi.TYPE_STRING, description='参数说明'),
                'key2': openapi.Schema(type=openapi.TYPE_INTEGER, description='参数2说明'),
            }
        )
    )
    # def post(self, request, *args, **kwargs):
        # Your view logic here
        # return Response(data={'message': 'Success'}, status=status.HTTP_200_OK)  
    def get(self, request, *args, **kwargs):
        # Your view logic here
        return Response(data={'message': 'Success'}, status=status.HTTP_200_OK)