from django.shortcuts import render
from datetime import datetime
from zoneinfo import ZoneInfo

def index(request):
    date = datetime.now()
    paris_now = datetime.now(ZoneInfo("Europe/Paris"))
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    prenom = "Sleaum"
    context = {"date":date, 
               "prenom":prenom, 
               "nasdaq_time":ny_now.strftime("%H:%M:%S"), 
               "euronext_time":paris_now.strftime("%H:%M:%S")
    }
    return render(request, "overfolio/index.html", context)

