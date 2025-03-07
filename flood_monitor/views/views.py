from django.shortcuts import render
from django.views import View


class FloodMonitorView(View):
    template_name = 'flood_monitor.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to this view
        """
        return render(request, self.template_name)
