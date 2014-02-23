from django.views.generic import TemplateView


class BeemoIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):

        context = super(BeemoIndex, self).get_context_data(*args, **kwargs)

        menu_items = [
            {'title': 'home', 'url': '/'},
        ]

        recent_calls = {'title': 'Recent Calls', 'width': 'fullwidth', 'type': 'd3-bar-chart'}
        
        dashboard_items = [recent_calls]

        context['menu_items'] = menu_items if len(menu_items) > 0 else None
        context['dashboard_items'] = dashboard_items if len(dashboard_items) > 0 else None

        return context
