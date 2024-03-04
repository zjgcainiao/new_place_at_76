from .base import render, OpenAIModel


def list_openai_models(request):
    models = OpenAIModel.objects.all()
    return render(request, 'list_models.html', {'models': models})
