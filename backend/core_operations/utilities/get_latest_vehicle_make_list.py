
from homepageapp.models import MakesNewSQL02Model
# common function 06


def get_latest_vehicle_make_list():
    # Get a distinct list of makes
    # makes = MakesNewSQL02Model.objects.values_list('make_name', flat=True)

    # makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(make_name__exact='').values_list('make_name', flat=True)

    makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(
        make_name__exact='').all().order_by('make_name')

    make_dict_list = list(makes.values('make_id', 'make_name'))
    make_tuple_list = [(make.pk, make.make_name) for make in makes]

    # Create a list of tuples for the choices, removing duplicates using set() and sort the result
    # models = ModelsNewSQL02Model.objects.filter(make_id=make_id)
    return make_tuple_list
