from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Order, Review, Service


@login_required
def customer_request(request):
    if Group.objects.get(user=request.user).name != "customer":
        return HttpResponse("Permission denied")
    if request.method == 'POST':
        return _handle_customer_post(request)
    elif request.method == 'GET':
        return _handle_customer_get(request)
    return render(request, "customer/index.html")


def _handle_customer_get(request):
    page = request.GET.get("page")
    if page:
        if page == "new_order":
            return render(request, "customer/new_order.html", {'services': Service.objects.all()})
        elif page == "current_order":
            return render(request, "customer/current_order.html", {"order": _get_current_order(request)})
        elif page == "history_order":
            return render(request, "customer/history_order.html", {"orders": _get_history_order(request)})
        elif page == "review_order":
            return _review_order_page(request)
    return render(request, "customer/index.html")


def _handle_customer_post(request):
    task = request.POST.get("task")
    if task == "new_order":
        return _new_order(request)
    elif task == "cancel_order":
        return _cancel_current_order(request)
    elif task == "get_current_order":
        return _get_current_order(request)
    elif task == "get_history_order":
        return _get_history_order(request)
    elif task == "finish_order":
        return _finish_order(request)
    elif task == "review_order":
        return _review_order(request)
    else:
        return HttpResponse("Invalid task")


def _new_order(request):
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    date = request.POST.get("date")
    start = request.POST.get("start")
    end = request.POST.get("end")
    services = request.POST.getlist("services")
    remark = request.POST.get("remark", "")
    current_order = _get_current_order(request)
    if current_order:
        return HttpResponse("You have an unfinished order: " + str(current_order.id))

    if not address or not phone or not date or not start or not end or not services:
        return HttpResponse("Invalid input")

    if not phone.isdigit() or len(phone) != 11:
        return HttpResponse("Invalid phone number")

    if remark and len(remark) > 200:
        return HttpResponse("Remark too long")

    for service in services:
        if not Service.objects.filter(name=service).exists():
            return HttpResponse("Service " + service + " does not exist")

    order = Order.objects.create(
        address=address,
        customer=request.user,
        phone=phone,
        start_time=date + " " + start,
        end_time=date + " " + end,
        services=services,
        remark=remark
    )

    order.customer.customer_info.order_count += 1
    order.customer.customer_info.save()

    return redirect("./?page=current_order")


def _cancel_current_order(request):
    current_order = _get_current_order(request)
    if not current_order:
        return HttpResponse("No order to cancel")
    if current_order.status != 0:
        return HttpResponse("Order cannot be canceled")
    current_order.delete()
    return redirect("./")


def _get_current_order(request) -> Order | None:
    try:
        return Order.objects.get(customer=request.user, status__lt=2)
    except Order.DoesNotExist:
        return None


def _get_history_order(request) -> list[Order] | None:
    orders = request.user.customer_orders.filter(status=2).order_by('-id')[:20]
    return orders if orders else None


def _finish_order(request):
    current_order = _get_current_order(request)
    if not current_order:
        return HttpResponse("No order to finish")
    if current_order.status != 1:
        return HttpResponse("Order cannot be finished")
    current_order.status = 2
    current_order.save()

    current_order.customer.customer_info.order_success_count += 1
    current_order.customer.customer_info.save()

    Review.objects.create(order=current_order)
    current_order.worker.worker_info.finish_order()

    return redirect("./?page=review_order&order_id=" + str(current_order.id) + "&next=./?page=current_order")


def _review_order_page(request):
    order_id = request.GET.get("order_id")
    next_url = request.GET.get("next_url", "./")
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist")
    if order.status != 2:
        return HttpResponse("Order is not finished")
    return render(request, "customer/review_order.html", {"order": order, "next_url": next_url})


def _review_order(request):
    order_id = request.POST.get("order_id")
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist")
    attitude_score = float(request.POST.get("attitude_score", -1))
    quality_score = float(request.POST.get("quality_score", -1))
    overall_score = float(request.POST.get("overall_score", -1))
    comment = request.POST.get("comment")
    if attitude_score < 0 or quality_score < 0 or overall_score < 0:
        return HttpResponse("Invalid score")

    review = order.review
    order.worker.worker_info.change_score(attitude_score, quality_score, overall_score, review.attitude_score,
                                          review.quality_score, review.overall_score)
    review.attitude_score = attitude_score
    review.quality_score = quality_score
    review.overall_score = overall_score
    review.comment = comment
    review.save()

    return redirect(request.POST.get("next", "./"))
