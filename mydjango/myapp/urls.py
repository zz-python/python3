from django.urls import path
from .views import hello_view,create_model,model_list_json

urlpatterns = [
    # http://127.0.0.1:8000/myapp/hello/
    path('hello/', hello_view, name='hello'),
    # http://127.0.0.1:8000/myapp/create_model/
    path('create_model/', create_model, name='create_model'),
    # http://127.0.0.1:8000/myapp/model_list_json/
    path('model_list_json/', model_list_json, name='model_list_json'),
]
