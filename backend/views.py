from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def backend_request(request):
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    if request.method == 'GET':
        return _handle_backend_get(request)

    return render(request, "backend/index.html")


def _handle_backend_get(request):
    page = request.GET.get('page')
    if page:
        if page == 'customers':
            customers = User.objects.filter(groups__name='customer').select_related('customer_info')
            return render(request, "backend/customers.html", {'customers': customers})

        if page == 'workers':
            workers = User.objects.filter(groups__name='worker').select_related('worker_info')
            infos = []
            for worker in workers:
                infos.append([worker, worker.worker_orders.filter(status=1).exists()])
            return render(request, "backend/workers.html", {'infos': infos})

        if page == 'orders':
            from core.models import Order
            orders = Order.objects.all().select_related('review')
            return render(request, "backend/orders.html", {'orders': orders})

    return render(request, "backend/index.html")
