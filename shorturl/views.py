import environ

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated


from .forms import LongUrlForm, UrlInfoForm
from .models import Url
from .serializers import UrlSerializer

env = environ.Env()
environ.Env.read_env()


def permission_denied_handler(request):
    return HttpResponse("You have no permissions")


@login_required
@never_cache
def index(request):
    if request.method == "POST":
        form = LongUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.user = request.user
            url.save()
            code = Url.objects.get(id=url.id)
            print("code: ", code)
            return render(request, "index.html", {"form": form, "code": code, "domain": env("DOMAIN")}, status=201)
    else:
        form = LongUrlForm()

    return render(request, "index.html", {"form": form, "code": None, "domain": ""}, status=302)


@login_required
@never_cache
def detail(request):
    if request.method == "GET":
        code = request.GET.get("code", None)
        url = Url.objects.filter(code=code)
        if url:
            url = url.first()
            is_find = True
            form = UrlInfoForm(request.POST or None, instance=url, editable=False)
        else:
            is_find = False
            form = UrlInfoForm(request.POST or None)
        context = {"is_find": is_find, "info_form": form}
        data = {
            "show": render_to_string(
                "show.html", context=context
            )
        }
        return JsonResponse(data)
    

@login_required
def edit(request, pk):
    url = get_object_or_404(Url, id=pk, user=request.user)
    form = UrlInfoForm(request.POST or None, instance=url, editable=True)

    if form.is_valid():
        form.save()

        return redirect("shorturl:list")
    
    return render(request, "edit.html", {"form": form})


@login_required
def delete(request, pk):
    url = get_object_or_404(Url, id=pk, user=request.user)
    url.delete()

    return redirect("shorturl:list")


@login_required
def list(request):
    if request.method == "GET":
        urls = Url.objects.filter(user=request.user)
        return render(request, "list.html", {"urls": urls})



def redirct_url(request, code):
    url = Url.objects.filter(code=code).first()

    if not url:
        return render(request, "error_page.html", status=404)

    return redirect(url.url, permanent=True, status=301)


class IndexAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer,]
    permission_classes = [IsAuthenticated,]
    serializer_class = UrlSerializer
    queryset = Url.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)

        if request.accepted_renderer.format == "html":
            form = LongUrlForm
            return Response({"form": form, "code": None, "domain": ""}, template_name="index.html", status=201)

        serializer = UrlSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UrlSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
