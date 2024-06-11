
# common function 07
from homepageapp.models import ModelsNewSQL02Model


def get_latest_vehicle_model_list():
    models = ModelsNewSQL02Model.objects.exclude(model_name__isnull=True).exclude(
        model_name__exact='').all().order_by('model_name')
    model_dict_list = list(models.values('model_id', 'model_name'))
    model_tuple_list = [(model.pk, model.model_name) for model in models]
    return model_tuple_list
    # return JsonResponse(model_dict_list, safe=False)
