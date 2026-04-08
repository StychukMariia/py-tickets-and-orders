from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order(user=user)
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session__id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
