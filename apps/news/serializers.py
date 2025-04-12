from rest_framework import serializers
from .models import TheTag, CoTheTag, TinTuc, TrackingXemTin

class TheTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheTag
        fields = '__all__'

class CoTheTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoTheTag
        fields = '__all__'

class TinTucSerializer(serializers.ModelSerializer):
    TAGS = serializers.PrimaryKeyRelatedField(many=True, queryset=TheTag.objects.all())

    class Meta:
        model = TinTuc
        fields = '__all__'

    def create(self, validated_data):
        # Pop the tags data before creating the TinTuc object
        tags_data = validated_data.pop('TAGS', [])
        # Create TinTuc instance
        tintuc = TinTuc.objects.create(**validated_data)
        # Set ManyToMany relation after instance is created
        tintuc.TAGS.set(tags_data)
        return tintuc

    def update(self, instance, validated_data):
        # Pop tags data from validated data (if present)
        tags_data = validated_data.pop('TAGS', None)
        # Update other fields of the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update ManyToMany relationship if 'TAGS' was included in the request data
        if tags_data is not None:
            instance.TAGS.set(tags_data)
        return instance

class TrackingXemTinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingXemTin
        fields = '__all__'
