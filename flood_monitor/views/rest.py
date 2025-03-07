import datetime

import pytz
import requests
import pandas as pd

from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from RealTimeFloodMonitoring.constants import API_MEASUREMENT_STATIONS_URL
from flood_monitor.serializers import ReadingSerializer, StationSerializer


class FloodMonitorDataViewset(ViewSet):

    @staticmethod
    def _request_api_data(api_endpoint: str, **params: dict) -> dict:
        """
        Sends a GET request to provided API endpoint, if successful returns requested data as a dictionary.
        """
        headers = {'Accept': 'application/json'}
        response = requests.get(api_endpoint, headers=headers, timeout=10, params=params)

        # Raise error if response is bad
        response.raise_for_status()

        return response.json()

    @staticmethod
    def _format_date_for_request(dt_date: datetime.datetime) -> str:
        """
        Converts date object to string with format "YYYY-MM-DD" as required by readings API request params.
        """
        return dt_date.strftime('%Y-%m-%d')

    @staticmethod
    def _validate_response_data(response, data_field):
        """
        Validates that provided data field exists in the response data
        """
        return data_field in response.keys()

    @action(detail=False, methods=['get'], url_name='list_stations')
    def list_stations(self, request):
        """
        API endpoint to request all measurement stations from the Flood Monitoring API - returns response data with
        format {id: <station reference ID>, value: <station name>}.
        """
        # Request all active measurement stations
        api_endpoint = f'{API_MEASUREMENT_STATIONS_URL}?&status=Active'
        response = self._request_api_data(api_endpoint)

        # Transform response data into list of dictionaries {measurement station ID: measurement station name}
        data_field = 'items'
        if not self._validate_response_data(response, data_field):
            response_data = {'error': f'Unexpected API response format, missing "{data_field}"'}
            return Response(response_data, status=status.HTTP_502_BAD_GATEWAY)
        measurement_stations = response.get(data_field)

        # Format as {id: <station reference>, value: <station name>} to be used by a combo filter in the frontend,
        # remove any data with invalid types (must be str).
        measurement_station_names = [
            {'id': station.get('stationReference'), 'value': station.get('label')}
            for station in measurement_stations if isinstance(station.get('label'), str)
        ]
        # Sort alphabetically on station name
        measurement_station_names = sorted(measurement_station_names, key=lambda station: station['value'])

        # Serialize + return response
        serializer = StationSerializer(measurement_station_names, many=True)
        return Response({'data': serializer.data})

    def list(self, request):
        """
        API endpoint to request flood monitor readings from the last 24 hours for an individual measurement station.
        """
        request_station_id = 'station_id'
        measurement_station_id = request.GET.get('station_id')
        if not measurement_station_id:
            msg = f'Missing required parameter: "{request_station_id}"'
            return HttpResponseBadRequest(msg)

        # Request all readings for given station in the last 24 hours
        datetime_now = datetime.datetime.now()
        datetime_24_hr_ago = datetime_now - datetime.timedelta(days=1)
        date_yesterday = self._format_date_for_request(datetime_24_hr_ago)
        api_endpoint = f'{API_MEASUREMENT_STATIONS_URL}/{measurement_station_id}/readings?_view=full'
        params = {'since': date_yesterday}
        response = self._request_api_data(api_endpoint, **params)

        # Transform response data
        data_field = 'items'
        if not self._validate_response_data(response, data_field):
            response_data = {'error': f'Unexpected API response format, missing "{data_field}"'}
            return Response(response_data, status=status.HTTP_502_BAD_GATEWAY)
        measurement_station_readings = response.get('items')
        measurement_station_readings = [
            {'datetime': pd.to_datetime(d.get('dateTime')),
             'measure_type': f'{d.get('measure').get('parameter').capitalize()} ({d.get('measure').get('unitName')})',
             'value': d.get('value')}
            for d in measurement_station_readings
        ]
        # Filter for last 24 hours as of request time
        measurement_station_readings = [
            d for d in measurement_station_readings if d['datetime'] >= pytz.UTC.localize(datetime_24_hr_ago)
        ]

        # Sort oldest to newest readings
        measurement_station_readings = sorted(measurement_station_readings, key=lambda reading: reading['datetime'])

        # Serialize + return response
        serializer = ReadingSerializer(measurement_station_readings, many=True)
        return Response({'data': serializer.data})
