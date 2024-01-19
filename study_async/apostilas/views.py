from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import Apostila, ViewApostila


def adicionar_apostilas(request):
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)
        # TODO: Criar as tags

        return render(
            request,
            'apostilas/adicionar_apostilas.html',
            {'apostilas': apostilas},
        )

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        apostila.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/apostilas/adicionar_apostilas/')


def apostila(request, id):
    apostila = Apostila.objects.get(id=id)
    views_totais = ViewApostila.objects.filter(
        apostila__user=request.user
    ).count()
    views_unicas = (
        ViewApostila.objects.filter(apostila=apostila)
        .values('ip')
        .distinct()
        .count()
    )

    view = ViewApostila(ip=request.META['REMOTE_ADDR'], apostila=apostila)
    view.save()

    return render(
        request,
        'apostilas/apostila.html',
        {
            'apostila': apostila,
            'views_unicas': views_unicas,
            'views_totais': views_totais,
        },
    )
