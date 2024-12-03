from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Almacenamiento, DatosClima, Presa

# Vista para mostrar los datos de las tablas
def mostrar_datos(request):
    # Obtener la opción seleccionada por el usuario, por defecto mostrar 'almacenamiento'
    data_type = request.GET.get('data_type', 'almacenamiento')  # 'almacenamiento' es el valor predeterminado
    
    # Dependiendo de la opción seleccionada, cargar los datos correspondientes
    if data_type == 'almacenamiento':
        almacenamiento_data = Almacenamiento.objects.all()
        datos_clima_data = DatosClima.objects.none()
        presas_data = Presa.objects.none()
    elif data_type == 'clima':
        almacenamiento_data = Almacenamiento.objects.none()
        datos_clima_data = DatosClima.objects.all()
        presas_data = Presa.objects.none()
    elif data_type == 'presas':
        almacenamiento_data = Almacenamiento.objects.none()
        datos_clima_data = DatosClima.objects.none()
        presas_data = Presa.objects.all()
    
    # Paginación: 10 elementos por página (ajustar según sea necesario)
    almacenamiento_paginator = Paginator(almacenamiento_data, 10)
    datos_clima_paginator = Paginator(datos_clima_data, 10)
    presas_paginator = Paginator(presas_data, 10)

    # Obtener el número de página de la solicitud
    page_almacenamiento = request.GET.get('page_almacenamiento')
    page_datos_clima = request.GET.get('page_datos_clima')
    page_presas = request.GET.get('page_presas')

    # Obtener la página actual de los datos
    almacenamiento_data = almacenamiento_paginator.get_page(page_almacenamiento)
    datos_clima_data = datos_clima_paginator.get_page(page_datos_clima)
    presas_data = presas_paginator.get_page(page_presas)

    context = {
        'almacenamiento_data': almacenamiento_data,
        'datos_clima_data': datos_clima_data,
        'presas_data': presas_data,
        'data_type': data_type,
    }

    return render(request, 'mostrar_datos.html', context)
