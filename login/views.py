from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login/index.html')
