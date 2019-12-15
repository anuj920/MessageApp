from django.shortcuts import render,redirect
from django import http
from django.views.generic import TemplateView
from normal.models import Message
from normal.forms import MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from  django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OwnMessageList(ListView):
    model = Message
    template_name = 'own_Message_list.html'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by('-added')

class MessageDetailView(DetailView):
    model = Message
    template_name = 'Message_detail.html'

@method_decorator(login_required, name='dispatch')
class CreateMessageView(CreateView):
    redirect_field_name = 'Message_detail.html'
    form_class = MessageForm
    model = Message
    template_name = 'message_form.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MessageUpdateView(UpdateView):
    redirect_field_name = 'Message_detail.html'
    form_class = MessageForm
    model = Message
    template_name = 'message_form.html'

@method_decorator(login_required, name='dispatch')
class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('own_message_list')
    template_name = 'Message_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        # the Message object
        self.object = self.get_object()
        if self.object.user == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden("<h1 style='color:red;text-align:center'>Cannot delete other's Messages</h1>")
