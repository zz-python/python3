from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyModelForm
from django.views.decorators.csrf import csrf_exempt
from .models import MyModel
from django.http import JsonResponse

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
