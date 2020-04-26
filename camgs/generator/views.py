from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .forms import CustomUserCreationForm, CompositionEditForm, NoteEditForm
from generator.models import Composition, NoteObject


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class CompositionCreateView(CreateView):
    model = Composition
    template_name = 'create.html'
    fields = ['title', 'composer', 'tempo', 'meter']
    success_url = reverse_lazy('compositions')


class CompositionListView(ListView):
    model = Composition
    template_name = 'compositions.html'
    context_object_name = 'compositions'

    def get_queryset(self):
        return Composition.objects.filter(user=self.request.user)


class CompositionEditView(UpdateView):
    model = Composition
    form_class = CompositionEditForm
    template_name = 'edit.html'
    success_url = reverse_lazy('compositions')

    def generator_view(self, **kwargs):
        composition = super().get_context_data(**kwargs)
        return composition


class NoteCreateView(CreateView):
    model = NoteObject
    template_name = 'entry.html'
    fields = ['order', 'pitch', 'duration', 'accidental']
    success_url = reverse_lazy('compositions')

    def get_context_data(self, **kwargs):
        kwargs['notes'] = NoteObject.objects.filter(
            composition=self.kwargs['composition'])
        return super(NoteCreateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.composition = Composition.objects.values_list(
            'id').filter(pk=kwargs['composition'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.composition_id = self.composition
        return super().form_valid(form)


class NoteEditView(UpdateView):
    model = NoteObject
    form_class = NoteEditForm
    template_name = 'noteedit.html'
    success_url = reverse_lazy('noteedit')
