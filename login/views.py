from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login/index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse(request.POST, json_dumps_params={'indent': 4})
