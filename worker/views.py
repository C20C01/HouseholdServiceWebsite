from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Order


@login_required
def worker_request(request):
    if Group.objects.get(user=request.user).name != "worker":
        return HttpResponse("Permission denied")
    if request.method == 'POST':
        return _handle_worker_post(request)
    current_order = _get_current_order(request)
    if current_order:
        return render(request, "worker/index.html", {"current_order": current_order})
    return render(request, "worker/index.html", {"unaccepted_orders": _get_unaccepted_orders(request)})


def _handle_worker_post(request):
    task = request.POST.get("task")
    if task == "accept_order":
        return _accept_order(request)
    return HttpResponse("Invalid task")


def _get_current_order(request) -> Order | None:
    try:
        return Order.objects.get(worker=request.user, status=1)
    except Order.DoesNotExist:
        return None


def _get_unaccepted_orders(request) -> list[Order] | None:
    orders = Order.objects.filter(status=0).order_by("start_time")
    return orders if orders else None


def _accept_order(request):
    order_id = request.POST.get("order_id")
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found")
    if order.worker is not None:
        return HttpResponse("Order already accepted")
    order.worker = request.user
    order.status = 1
    order.save()
    return redirect(".", {"current_order": order})
