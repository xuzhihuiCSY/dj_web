from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
import json
import urllib.request
from django.core.files.storage import FileSystemStorage
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from myapp.models import Room, Message

from .models import Task

# Create your views here.
def index(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'login':
            # your sign in logic goes here
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('L')
            else:
                messages.info(request,'Credentials Invalid')
                return redirect('index')
        elif request.POST.get('submit') == 'signUp':
            # your sign up
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email Used')
                    return redirect('index')
                elif User.objects.filter(username=username).exists():
                    messages.info(request,'Username Used')
                    return redirect('index')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    auth.login(request,user)
                    return redirect('L')
            else:
                messages.info(request,'Password Not the Same')
                return redirect('index')
    else:
        return render(request,'index.html')
        
def L(request):
    return render(request,'L.html')

def music(request):
    return render(request,'music.html')

def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
        json_data = json.loads(res)
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp'])+' kelvin',
            "pressure": str(json_data['main']['pressure'])+' hPa',
            "humidity": str(json_data['main']['humidity']),
            "weather": str(json_data['weather'][0]['main']),
            "id": str(json_data['weather'][0]['id']),
            "feels_like": str(json_data['main']['feels_like'])+' kelvin',
            "cod": str(json_data['cod']),
        }

    else:
        city = ''
        data = {}
    return render(request, 'weather.html', {'city': city, 'data': data})

class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'myapp/task.html'

class TaskCreate(CreateView):
    model = Task
    fields = {'title','description','complete'}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = {'title','description','complete'}
    success_url = reverse_lazy('tasks')

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

def home(request):
    return render(request,'home.html')

def room(request,room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request,'room.html',{
        'username':username,
        'room':room,
        'room_details':room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
       return redirect('/room/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/room/'+room+'/?username='+username)

def send(request):
    message=request.POST['message']
    username=request.POST['username']
    room_id=request.POST['room_id']

    new_message = Message.objects.create(value=message,user=username,room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def portfolio(request):
    return render(request,'Portfolio.html')

def game(request):
    return render(request,'game.html')

def watch(request):
    return render(request,'Watch.html')

def fighter(request):
    return render(request,'game/fight.html')

def shot(request):
    return render(request,'game/shot.html')

def ni(request):
    return render(request,'game/ni.html')

def snake(request):
    return render(request,'game/Snake.html')

def tower(request):
    return render(request,'game/tower.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['File']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def M_C_Game(request):
    return render(request,'game/M_C_Game.html')

def flip(request):
    return render(request,'flip.html')
