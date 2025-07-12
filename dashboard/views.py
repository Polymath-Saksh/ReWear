from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserProfileSerializer
from items.serializers import ItemSerializer
from swaps.serializers import SwapSerializer

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        user_items = request.user.items.all()
        user_swaps_requested = request.user.swaps_requested.all()
        user_swaps_received = request.user.swaps_received.all()

        profile_data = UserProfileSerializer(user_profile).data
        items_data = ItemSerializer(user_items, many=True).data
        swaps_requested_data = SwapSerializer(user_swaps_requested, many=True).data
        swaps_received_data = SwapSerializer(user_swaps_received, many=True).data

        return Response({
            "profile": profile_data,
            "items": items_data,
            "swaps_requested": swaps_requested_data,
            "swaps_received": swaps_received_data,
        })
