from rest_framework import serializers


class StationSerializer(serializers.Serializer):
    id = serializers.CharField()
    value = serializers.CharField()


class ReadingSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    measure_type = serializers.CharField()
    value = serializers.FloatField()
