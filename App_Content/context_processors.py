from App_Content.models import Category


def extras(request):
    cat_menu_list = Category.objects.all()
    return {'cat_menu_list': cat_menu_list}
