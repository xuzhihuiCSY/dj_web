from django.urls import URLPattern, path
from . import views
from .views import TaskCreate, TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('L',views.L,name='L'),
    path('weather',views.weather,name='weather'),
    path('game',views.game,name='game'),
    path('watch',views.watch,name='watch'),
    path('fight',views.fighter,name='fight'),
    path('shot',views.shot,name='shot'),
    path('ni',views.ni,name='ni'),
    path('snake',views.snake,name='snake'),
    path('tower',views.tower,name='tower'),
    path('music',views.music,name='music'),
    path('portfolio',views.portfolio,name='portfolio'),
    # path('',TaskList.as_view(),name='tasks'),
    path('tasks',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
    path('home',views.home,name='home'),
    path('room/<str:room>/',views.room,name='room'),
    path('checkview',views.checkview,name='checkview'),
    path('send',views.send,name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('upload/',views.upload,name='upload'),
    path('M_C_Game',views.M_C_Game,name='M_C_Game'),
    path('flip',views.flip,name='flip'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)