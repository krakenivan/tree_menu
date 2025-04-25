from django import template
from django.urls import resolve, Resolver404

from ..models import MenuItem

register = template.Library()


@register.inclusion_tag("core/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context["request"]
    current_url = request.path_info

    try:
        resolved_url = resolve(current_url)
        resolved_url_name = resolved_url.url_name
    except Resolver404:
        resolved_url_name = None

    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related("parent")
    # жадная загрузка данных всего меню
    menu_tree = build_menu_tree(menu_items)
    active_items = mark_active_items(menu_tree, current_url, resolved_url_name)
    expanded_items = mark_expanded_items(active_items)

    for item in menu_items:
        item.is_active = item in active_items
        item.is_expanded = item in expanded_items
        item.should_display = (
            item.parent is None
            or item.parent in expanded_items
            or item.parent in active_items
        )

    return {
        "menu_items": menu_items,
        "menu_tree": menu_tree,
        "current_url": current_url,
    }


def build_menu_tree(items):
    """Формирование дерева"""
    tree = []
    item_dict = {
        item.id: item for item in items
    }  # словарь для доступа к элементу по id гарантирую отсутствие доп. запросов к БД
    for item in items:
        if item.parent is None:  # родителя нет
            tree.append(item)
        else:
            parent = item_dict.get(item.parent.id)
            if parent:
                if not hasattr(parent, "child"):
                    parent.child = []  # список с дочерними элементами
                parent.child.append(item)

    return tree


def mark_active_items(tree, current_url, resolved_url_name, active_items=None):
    """Определение активного пункта"""
    if active_items is None:
        active_items = set()
    for item in tree:
        item_url = item.get_absolute_url()

        if item_url == current_url or (
            item.named_url and item.named_url == resolved_url_name
        ):
            active_items.add(item)

        if hasattr(item, "children"):
            mark_active_items(
                item.children.all(), current_url, resolved_url_name, active_items
            )

    return active_items


def mark_expanded_items(items, expanded_items=None):
    """Определение раскрытых пунктов"""
    if expanded_items is None:
        expanded_items = set()
    for item in items:
        if item.parent:
            mark_expanded_items((item.parent,), expanded_items)  # рекурсивный обход предков
        expanded_items.add(item)

    return expanded_items
