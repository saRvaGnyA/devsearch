from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from .forms import ProjectForm
from .models import Project

# Create your views here.

projectsList = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'Fully functional ecommerce website'
    },
    {
        'id': '2',
        'title': 'Portfolio Website',
        'description': 'A personal website to write articles and display work'
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'An open source project built by the community'
    }
]


def projects(request):
    msg = "Welcome to the Projects page!"
    number = 9
    projectsToPass = Project.objects.all()
    context = {"message": msg, "no": number, "projects": projectsToPass}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    # obj = None
    # for i in projectsList:
    #     if i['id'] == pk:
    #         obj = i
    obj = Project.objects.get(id=pk)
    context = {'project': obj}
    return render(request, 'projects/single-project.html', context)


def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {"form": form}
    return render(request, 'projects/project_form.html', context)


def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {"form": form}
    return render(request, 'projects/project_form.html', context)


def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {"object": project}
    return render(request, 'projects/delete_template.html', context)
