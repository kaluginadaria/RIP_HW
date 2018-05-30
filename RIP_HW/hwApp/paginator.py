from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(data, page):
    paginator = Paginator(data, 3)
    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)
    return paginator
