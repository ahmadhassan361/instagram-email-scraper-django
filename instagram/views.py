from django.shortcuts import render, redirect
from .models import ProcessController
import time
from django.contrib.auth import authenticate, login
from .tasks import run_background_task
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                "index"
            )  # Replace 'home' with the URL name of your home page
        else:
            return redirect("login")

    return render(
        request, "login.html"
    )  # Replace 'login.html' with the path to your login template


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        if username is not None:
            pc = ProcessController(username=username, file="")
            pc.save()
            pc.file = f"{username}-{pc.pk}.csv"
            pc.save()
            run_background_task(pc.pk)

    process = ProcessController.objects.order_by("-created_date").all().first()
    context = {"process": None}
    print(process)
    if process:
        context["process"] = process

    processes = ProcessController.objects.order_by("-created_date").all()
    context["processes"] = processes
    return render(request, "index.html", context=context)


@login_required(login_url="login")
def stop(request, stop_id):
    try:
        if stop_id is not None:
            pr = ProcessController.objects.get(id=stop_id)
            pr.isStop = True
            pr.isRuning = False
            pr.isComplete = True
            pr.save()
        return redirect("index")
    except Exception as e:
        return redirect("index")
