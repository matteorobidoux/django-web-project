from .forms import MessageForm
from django.dispatch import receiver
from django.views import View
from .models import Message
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse,request
from django.template import loader
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.signals import notify

class ConvoList(ListView):
    model = Message
    template_name = 'inbox.html'
    context_object_name = 'convos'

    def get_queryset(self):
        convos = super(ConvoList, self).get_queryset()
        convos = convos.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        convos = convos.filter(content="")
        return convos

class CreateConvo(LoginRequiredMixin ,CreateView):
    model = Message
    fields = ['receiver']
    template_name = 'create_convo.html'
    
    def form_valid(self, form):
        if Message.objects.filter(Q(sender=self.request.user, receiver=form.instance.receiver) | Q(receiver=self.request.user, sender=form.instance.receiver)).exists():
            return redirect('inbox')
        else:
            form.instance.sender = self.request.user
            return super().form_valid(form)

class MessageList(ListView):
    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'

    def get_queryset(self, *args, **kwargs):
        user_receiver = User.objects.get(pk=self.kwargs['pkr'])
        user_sender = User.objects.get(pk=self.kwargs['pks'])
        convos = super(MessageList, self).get_queryset()
        convos = convos.filter(Q(sender=user_sender, receiver=user_receiver) | Q(receiver=user_sender, sender = user_receiver))
        return convos

class CreateMessage(View):
    def post(self, request, *args, **kwargs):
            form = MessageForm(request.POST)
            if form.is_valid():
                data = Message()
                data.content = form.cleaned_data['content']
                if self.request.user == User.objects.get(pk=self.kwargs['pkr']):
                    data.sender = self.request.user
                    data.receiver = User.objects.get(pk=self.kwargs['pks'])
                else:
                    data.sender = self.request.user
                    data.receiver = User.objects.get(pk=self.kwargs['pkr'])
                notify.send(data.sender, recipient=data.receiver, verb='Message', description=data.content)
                data.save()
                return redirect('messages', pkr=self.kwargs['pkr'], pks=self.kwargs['pks'])
            else:
                return redirect('messages', pkr=self.kwargs['pkr'], pks=self.kwargs['pks'])