from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Restaurant, Order, OrderItem, DeliveryAddress, Menu, MenuItem, UserProfile


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','_id', 'username', 'email', 'name', 'isAdmin']


    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff    

    
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','user','user_type', 'restaurant']

    def get_id(self, obj):
        return obj.id
    

 
class UserSerializerWithToken(UserSerializer):

    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class RestaurantSerializer(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_menus(self, obj):
        menus = obj.menu_set.all()
        serializer = MenuSerializer(menus, many=True)
        return serializer.data


class MenuSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
    
    def get_menu_items(self, obj):
        menu_items = obj.menuitem_set.filter(isAvailable=True)
        serializer = MenuItemSerializer(menu_items, many=True)
        return serializer.data


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    deliveryAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_deliveryAddress(self, obj):
        try:
            address = DeliveryAddressSerializer(obj.deliveryAddress, many=False).data
        except:
            address = False
        return address


    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data