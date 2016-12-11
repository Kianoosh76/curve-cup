from django.db.models.aggregates import Sum
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import DetailView

from groups.models import Group, Score


class GroupsView(DetailView):
    queryset = Group.objects
    context_object_name = 'current_group'
    template_name = 'groups/index.html'

    def get_object(self, queryset=None):
        pk = self.request.GET.get('group', None)
        if pk is not None:
            return Group.objects.get(pk=int(pk))
        else:
            return Group.objects.first()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['groups'] = self.get_queryset()
        context['players'] = context['current_group'].players.annotate(
            total_score=Sum('scores__score')).extra(order_by=('-total_score',))
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden()
        group = request.POST['group']
        players = Group.objects.get(pk=int(group)).players.all()
        for player in players:
            new_score = request.POST.get(str(player.pk))
            if new_score:
                Score.objects.create(score=int(new_score), player=player)
        return redirect('/?group=' + group)
