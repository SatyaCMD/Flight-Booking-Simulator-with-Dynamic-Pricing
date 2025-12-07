import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from flights.views import FlightListView, FlightSearchView
from flights.repositories import FlightRepository

def test_api():
    factory = APIRequestFactory()
    
    print("Testing Flight List API...")
    view = FlightListView.as_view()
    request = factory.get('/api/flights/')
    response = view(request)
    print(f"Status Code: {response.status_code}")
    print(f"Data Count: {len(response.data)}")
    assert response.status_code == 200
    assert len(response.data) > 0

    print("\nTesting Flight Search API...")
    repo = FlightRepository()
    flight = repo.find_all()[0]
    
    search_view = FlightSearchView.as_view()
    url = f'/api/flights/search/?origin={flight.origin}&destination={flight.destination}&date={flight.departure_time.strftime("%Y-%m-%d")}'
    print(f"Searching: {url}")
    request = factory.get(url)
    response = search_view(request)
    print(f"Status Code: {response.status_code}")
    print(f"Data Count: {len(response.data)}")
    assert response.status_code == 200
    assert len(response.data) > 0
    
    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    test_api()
