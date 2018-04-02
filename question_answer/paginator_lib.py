# функции для пагинации
# вызываются от django.core.paginator.Page

import django.core.paginator

def five_before(page):
    """
    Returns list with the previous page numbers,
    no longer 4. Returns the empty list [] if the page is first.
    """
    if page.number <= 5:
        return [x for x in range(1, page.number)]
    else:
        return [x for x in range(page.number - 5, page.number)]


def five_after(page):
    """
    Returns list with the next page numbers,
    no longer 4. Returns the empty list [] if the page is first.
    """
    if page.paginator.num_pages - page.number <= 5:
        return [x for x in range(page.number + 1, page.paginator.num_pages + 1)]
    else:
        return [x for x in range(page.number + 1, page.number + 5)]

def paginator_wrap(quwery_set, page_number):
    p = django.core.paginator.Paginator(quwery_set, 10)
    # Пагинатор делает 1 запрос в базу и возвращает уже реальный массив, а не QuerySet
    return p.get_page(page_number)
