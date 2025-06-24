from django.shortcuts import render
from django.views import View
from .service.shapes_json_default_parameters_getter import get_shapes_default_parameters

# Create your views here.
class WhiteBoardView(View):
    def get(self, request):
        return render(request, 'whiteboard.html',
                      {"default_shapes_json": get_shapes_default_parameters()})