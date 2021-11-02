
from rest_framework import status
from rest_framework.test import APITestCase
import json

class GetLocationDetails(APITestCase):
    def test_get_location_details_to_fetch_from_Nominatim(self):
        data = {'lat':-34.4391708,'lon':-58.7064573}
        response = self.client.get('/getlocation', data, format='json')
        json_res = json.loads(response.content)
        self.assertEqual(json_res["name"], "YPF, Autopista Pedro Eugenio Aramburu, El Triángulo, Partido de Malvinas Argentinas, 1.619, Argentina")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_location_details_to_fetch_from_DB_chache(self):
        data = {'lat':-34.4391708,'lon':-58.7064573}
        self.client.get('/getlocation', data, format='json')
        response = self.client.get('/getlocation', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
