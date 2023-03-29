from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models.tables import Order
# from .game.unit_factory import UnitFactory


# Create your views here.
# @csrf_exempt
def index(request):
    # order = Order.objects.get(pk=1)
    # army = UnitFactory.build_unit(order)
    # army.move()

    # return HttpResponse(army.location)
    return ''



