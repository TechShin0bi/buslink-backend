from rest_framework import serializers
from fleet.models import Bus, BusFeature
from agencies.serializers import AgencyBranchListSerializer
from agencies.models import AgencyBranch


class BusSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    agency_branches = AgencyBranchListSerializer(many=True, read_only=True)
    agency_branch_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AgencyBranch.objects.all(),
        write_only=True,
        source="agency_branches",
    )
    features_list = serializers.ListField(
        child=serializers.ChoiceField(choices=BusFeature.choices),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Bus
        fields = [
            "id",
            "matriculation_code",
            "registration_number",
            "category",
            "category_display",
            "features",
            "features_list",
            "total_seats",
            "rows",
            "columns",
            "back_seat_count",
            "has_ac",
            "has_tv",
            "has_wifi",
            "has_toilet",
            "manufacture_year",
            "last_maintenance_date",
            "next_maintenance_date",
            "insurance_expiry",
            "is_available",
            "created_at",
            "updated_at",
            "agency_branches",
            "agency_branch_ids",
        ]
        read_only_fields = ("created_at", "updated_at", "features")

    def validate(self, data):
        # Validate seat configuration
        rows = data.get("rows", self.instance.rows if self.instance else None)
        columns = data.get("columns", self.instance.columns if self.instance else None)
        back_seat_count = data.get(
            "back_seat_count", self.instance.back_seat_count if self.instance else 0
        )
        total_seats = data.get(
            "total_seats", self.instance.total_seats if self.instance else None
        )

        if rows and columns:
            calculated_seats = (rows - 1) * columns + (back_seat_count or 0)
            if total_seats and calculated_seats != total_seats:
                data["total_seats"] = calculated_seats

        return data

    def create(self, validated_data):
        features = validated_data.pop("features_list", [])
        bus = super().create(validated_data)
        if features:
            bus.features = features
            bus.save()
        return bus

    def update(self, instance, validated_data):
        features = validated_data.pop("features_list", None)
        if features is not None:
            instance.features = features
        return super().update(instance, validated_data)


class BusListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display")
    agency_branches = AgencyBranchListSerializer(many=True)
    features_list = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = [
            "id",
            "matriculation_code",
            "registration_number",
            "category",
            "category_display",
            "features_list",
            "total_seats",
            "is_available",
        ]

    def get_features_list(self, obj):
        return [
            dict(BusFeature.choices).get(feature, feature)
            for feature in (obj.features or [])
        ]
