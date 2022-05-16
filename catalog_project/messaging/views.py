from .forms import MessageForm
from django.views import View
from .models import Message
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from notifications.signals import notify


# Lists all conversations that the user had
class ConvoList(ListView):
    model = Message
    template_name = 'inbox.html'
    context_object_name = 'convos'

    # Gets all converations based on sender and reciever
    def get_queryset(self):
        # Gets all conversations where the user is the sender or receiver
        convos = super().get_queryset()
        convos = convos.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

        # Checks for doubles in sender/receiver
        for convo in convos:
            if ((convo.receiver == self.request.user) and
                    convos.filter(sender=convo.receiver, receiver=convo.sender).exists()):
                convos = convos.filter(~Q(sender=convo.receiver, receiver=convo.sender))

        # Filter by distinct
        convos = convos.order_by('receiver', '-timestamp').distinct('receiver').union(convos.order_by('sender', '-timestamp').distinct('sender'))

        return convos


# Creates a conversation with the user
class CreateConvo(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['receiver']
    template_name = 'create_convo.html'

    # Redirects the user based on if the conversation exists
    def form_valid(self, form):
        # Sends user to inbox if the convo exists
        if Message.objects.filter(
                Q(sender=self.request.user, receiver=form.instance.receiver) | Q(receiver=self.request.user,
                                                                                 sender=form.instance.receiver)).exists():
            return redirect('inbox')
        else:
            # Creates a new conversation
            form.instance.sender = self.request.user
            return super().form_valid(form)


# Gets a list of messages sent or recieved by the user, with the target user in mind
class MessageList(UserPassesTestMixin, ListView):
    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'

    # Checks if the requester pk is one of the sender or reciever pks
    def test_func(self):
        user_receiver = User.objects.get(pk=self.kwargs['pkr'])
        user_sender = User.objects.get(pk=self.kwargs['pks'])

        return self.request.user == user_sender or self.request.user == user_receiver

    # Gets all messages where the user is the reciever or sender
    def get_queryset(self, *args, **kwargs):
        # Same thing for the correspondee
        user_receiver = User.objects.get(pk=self.kwargs['pkr'])
        user_sender = User.objects.get(pk=self.kwargs['pks'])
        convos = super(MessageList, self).get_queryset()
        convos = convos.filter(
            Q(sender=user_sender, receiver=user_receiver) | Q(receiver=user_sender, sender=user_receiver))

        return convos


# Sends a message to a user
class CreateMessage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        # Checks if the message is valid
        if form.is_valid():
            data = Message()
            data.content = form.cleaned_data['content']
            # Send the message based on whos the sender or reciever
            if self.request.user == User.objects.get(pk=self.kwargs['pkr']):
                data.sender = self.request.user
                data.receiver = User.objects.get(pk=self.kwargs['pks'])
            else:
                data.sender = self.request.user
                data.receiver = User.objects.get(pk=self.kwargs['pkr'])
            # Create and send the message
            notify.send(data.sender, recipient=data.receiver, verb='Message', description=data.content)
            data.save()
            return redirect('messages', pkr=self.kwargs['pkr'], pks=self.kwargs['pks'])
        else:
            return redirect('messages', pkr=self.kwargs['pkr'], pks=self.kwargs['pks'])
