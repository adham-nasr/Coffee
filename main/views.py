from django.shortcuts import render,redirect

from django.views import View
from .models import DayStats
from .services import Extract,Store,QueryManager
# Create your views here.

class HomeView(View):

    def get(self,request):
        
        q = DayStats.objects.all()
        
        return render(request,'main/index.html',{"data":q})

class StatsView(View):

    def get(self,request):
        
        print(request.GET)
        year = 2025
        if 'year' in request.GET:
            year = int(request.GET['year'])
        q = QueryManager.run(year)
        # print(q)
        return render(request,'main/monthly.html',{"data":q})
    
class ReloadView(View):
    
    def get(self, request):

        extract = Extract()
        extract.run()

        store = Store(extract)
        store.run()   
        
        return redirect("/")     

