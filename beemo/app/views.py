from django.views.generic import TemplateView


# Setup menu items
menu_items = [
    {'title': 'home', 'url': '/'},
]

# Setup dashboard items
dashboard_items = [

]
    


class BeemoIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BeemoIndex, self).get_context_data(*args, **kwargs)

        context['menu_items'] = menu_items if len(menu_items) > 0 else None
        context['dashboard_items'] = dashboard_items if len(dashboard_items) > 0 else None

        return context