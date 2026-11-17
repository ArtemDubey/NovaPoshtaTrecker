from django.shortcuts import render
from django.http import Http404

PARCELS = [
    {
        "track_number": "UA1234567890",
        "sender": "Олександр",
        "receiver": "Марія",
        "weight": "2.5 кг",
        "type": "Побутові речі",
        "origin": "Київ",
        "destination": "Львів",
        "status": "В дорозі"
    },
    {
        "track_number": "UA8765432109",
        "sender": "Іван",
        "receiver": "Ольга",
        "weight": "0.5 кг",
        "type": "Крихке",
        "origin": "Харків",
        "destination": "Одеса",
        "status": "Прибула в депо"
    },
    {
        "track_number": "UA1122334455",
        "sender": "Андрій",
        "receiver": "Дмитро",
        "weight": "12.0 кг",
        "type": "Електроніка",
        "origin": "Дніпро",
        "destination": "Київ",
        "status": "Отримана"
    },
    {
        "track_number": "UA5566778899",
        "sender": "Софія",
        "receiver": "Катерина",
        "weight": "1.2 кг",
        "type": "Документи",
        "origin": "Львів",
        "destination": "Івано-Франківськ",
        "status": "В депо міста відправника"
    },
    {
        "track_number": "UA9988776655",
        "sender": "Максим",
        "receiver": "Віктор",
        "weight": "5.4 кг",
        "type": "Побутові речі",
        "origin": "Запоріжжя",
        "destination": "Тернопіль",
        "status": "В дорозі"
    },
]

def home_view(request):
    return render(request, 'Trecker/home.html')

def parcel_list_view(request):
    return render(request, 'Trecker/parcel_list.html', {'parcels': PARCELS})

def parcel_detail_view(request, track_number):
    parcel = next((p for p in PARCELS if p['track_number'] == track_number), None)
    if not parcel:
        raise Http404("Посилку не знайдено")
    return render(request, 'Trecker/parcel_detail.html', {'parcel': parcel})

def search_view(request):
    track_number = request.GET.get('track', '')
    parcel = next((p for p in PARCELS if p['track_number'] == track_number), None)
    return render(request, 'Trecker/search_parcel.html', {'parcel': parcel})