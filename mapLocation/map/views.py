from django.shortcuts import render,redirect
import folium
import geocoder
from .models import Search
from .forms import SearchForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SearchForm()


    address = Search.objects.all().last()
    location = geocoder.osm(address)
    
    if location is not None:
        lat = location.latlng[0]
        lng = location.latlng[1]
        country = location.country
    else:
        lat = 0  # Varsayılan bir değer veya hata durumu için bir değer atayabilirsiniz.
        lng = 0
        country = "Bilinmiyor"
    
    m = folium.Map(location=[38, 35], zoom_start=6)
    folium.Marker([38, 35], tooltip='click for more', popup=address).add_to(m)
    folium.Marker([lat, lng], tooltip='click for more', popup=country).add_to(m)
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }

    return render(request, 'index.html', context)