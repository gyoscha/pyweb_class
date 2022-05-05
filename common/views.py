from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        hello = """<h1>Hello, World</h1>"""

        return HttpResponse(hello)


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'common/index.html')
