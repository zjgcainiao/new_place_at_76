from .base import render


def GetHomepageView(request):

    # the list of icons corresponding to the services provided by the shop. Reduce code redundancy
    service_icons = [
        {
            'img_src': 'homepageapp/img/svgs/car-maintenance-icon.svg',
            'alt': 'car car-maintenance-oil-change',
            'title': 'Oil Changes',
        },
        {
            'img_src': 'homepageapp/img/svgs/air-conditioning-icon.svg',
            'alt': 'a/c-system-diagnosis-and-repair',
            'title': 'Air Conditioning Not Cooling & Heating',
        },
        {
            'img_src': 'homepageapp/img/svgs/engine-icon.svg',
            'alt': 'engine',
            'title': 'Engine Repair (w/ service lights on, overheating, etc)',
        },
        {
            'img_src': 'homepageapp/img/svgs/battery-svgrepo-com-icon.svg',
            'alt': 'Family MPV',
            'title': 'Car Battery Service',
        },
        {
            'img_src': 'homepageapp/img/svgs/electrical-service-icon.svg',
            'alt': 'Compact',
            'title': 'Electric Diangosis',
        },
        {
            'img_src': 'homepageapp/img/svgs/brake-icon.svg',
            'alt': 'Convertible',
            'title': 'Brake Replacements',
        },
        {
            'img_src': 'homepageapp/img/svgs/spark-spark-plug-svgrepo-com-icon.svg',
            'alt': 'spark-plug',
            'title': 'Spark Plugs',
        },
        {
            'img_src': 'homepageapp/img/svgs/gear-shift-stick-svgrepo-com-icon.svg',
            'alt': 'transmission',
            'title': 'Transmission Service',
        },
        {
            'img_src': 'homepageapp/img/svgs/windshield-icon.svg',
            'alt': 'Windshield-Wipers',
            'title': 'Windshield Wiper',
        },
        {
            'img_src': 'homepageapp/img/svgs/suspension-icon.svg',
            'alt': 'suspension',
            'title': 'Suspension Service',
        },
    ]

    return render(request, 'homepageapp/20_homepageapp_home.html', {'service_icons': service_icons})
