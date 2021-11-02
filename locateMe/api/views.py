import json
import pytz
import datetime as dt
from django.shortcuts import render
from rest_framework import status
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LocationDetails

def location_info(lat,lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    print("Calling Nominatim")
    response = requests.get(url)
    json_res = json.loads(response.content)
    response = json_res.get("display_name","No Details found")
    return response

class GetLocationAPIView(APIView):

    def get(self, request, format=None):
        utc=pytz.UTC
        response_dict = {"name":None}

        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        if lat is None:
            response = {"lat": "Parameter is missing"}
            return Response(response, status=404)
        if lon is None:
            response = {"lon": "Parameter is missing"}
            return Response(response, status=404)
  
        current_date = dt.datetime.now().replace(tzinfo=utc)
        existing_place = LocationDetails.objects.filter(lat=lat,lon=lon).first()
        
        if existing_place is None: #for non existing place
            
            name = location_info(lat,lon)
            LocationDetails.objects.create(lat=lat,lon=lon,date=current_date,name = name)
            response_dict["name"] = name
            
        else: #for existing place
            difference = round((current_date - existing_place.date).total_seconds()) * 0.000277778
            if difference > 24:
                response_dict["name"]= location_info(lat,lon)
                LocationDetails.objects.filter(lat=lat,lon=lon).update(date=current_date)
            else:
                print("Fetching from DB cache")
                response_dict["name"] = existing_place.name 

        return Response(response_dict,status=status.HTTP_200_OK)
