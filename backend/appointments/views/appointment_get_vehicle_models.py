
from.base import JsonResponse, ModelsNewSQL02Model

def appointment_get_vehicle_models(request, make_id):
    models = ModelsNewSQL02Model.objects.filter(
        make_id=make_id).all().order_by('model_name')
    model_dict_list = list(models.values('model_id', 'model_name'))
    model_tuple_list = [(model.pk, model.model_name) for model in models]
    # return JsonResponse(model_tuple_list, safe=False)
    return JsonResponse(model_dict_list, safe=False)