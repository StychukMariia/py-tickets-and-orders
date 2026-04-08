from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    order = Order.objects.create(username=username)
    if date:
        order.created_at = date
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(username=username)
    return Order.objects.all()
