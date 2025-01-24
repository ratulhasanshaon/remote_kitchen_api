from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response

from base.models import Restaurant, Menu, MenuItem, UserProfile
from base.serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer 
from rest_framework import status
from ..permissions import IsEmployeeUser, IsOwnerUser


# All Restaurants and Menus by search
@api_view(['GET'])
def getRestaurants(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    restaurants = Restaurant.objects.filter(name__icontains=query)
   
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response({'restaurants': serializer.data})


# Get Restaurant and Menus by id
@api_view(['GET'])
def getRestaurant(request, pk):
    restaurant = Restaurant.objects.get(_id=pk)
    serializer = RestaurantSerializer(restaurant, many=False) 
    return Response(serializer.data)

# Get Restaurant for Admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getRestaurantByOwner(request):
    user = request.user
    restaurant = Restaurant.objects.filter(owner=user)
    serializer = RestaurantSerializer(restaurant, many=True) 
    return Response(serializer.data)

# Add Restaurant by owner user
@api_view(['POST'])
@permission_classes([IsOwnerUser])
def createRestaurant(request):
    data = request.data
    user = request.user
    restaurant = Restaurant.objects.create(
        owner = user,
        name = data['name'],
        details = data['details'],
        location = data['location'],
        description = data['description']
    )
    serializer = RestaurantSerializer(restaurant, many=False) 
    return Response(serializer.data)

# Update Restaurant by owner user
@api_view(['PUT'])
@permission_classes([IsOwnerUser])
def updateRestaurant(request, pk):
    data = request.data
    restaurant = Restaurant.objects.get(_id=pk)
    owner_restaurant = request.user.userprofile.restaurant

    if restaurant == owner_restaurant:

        restaurant.name = data['name']
        restaurant.details = data['details']
        restaurant.location = data['location']
        restaurant.description = data['description']

        restaurant.save()
        
        serializer = RestaurantSerializer(restaurant, many=False) 
        return Response(serializer.data)
    else:
        return Response({'detail': 'Restaurant not found associated with user profile.'}, status=400)



# for Uploding restaurant images
@api_view(['POST'])
def uploadImage(request):
    data = request.data
    
    restaurant_id = data['restaurant_id']
    restaurant = Restaurant.objects.get(_id=restaurant_id)
    restaurant.image = request.FILES.get('image')
    restaurant.save()

    return Response('Image was uploaded')


# To get all the available menus by keyword for users
@api_view(['GET'])
def getAllMenus(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    menus = Menu.objects.filter(name__icontains=query)
    serializer = MenuSerializer(menus, many=True)
    return Response({'menus': serializer.data})
    

# To get all the menus for associate employee and user
@api_view(['GET'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def getRestaurantMenus(request):
    try:
        user_profile = request.user.userprofile 
        if user_profile.restaurant:
            restaurant = user_profile.restaurant
            serializer = RestaurantSerializer(restaurant, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'No restaurant found associated with user profile.'}, status=400)
    except UserProfile.DoesNotExist:
        return Response({'detail': 'User profile not found.'}, status=404)


# add new menu for restaurant by employee and user
@api_view(['POST'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def createMenu(request):
    try:
        data = request.data
        user = request.user.id
        user_profile = request.user.userprofile
        restaurant = user_profile.restaurant
        data['restaurant'] = restaurant._id
        data['createdBy'] = user

        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except UserProfile.DoesNotExist:
        return Response({'detail': 'User profile not found.'}, status=404)


# update new menu for restaurant by employee and user
@api_view(['PUT'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def updateMenu(request, pk):
    data = request.data
    menu = Menu.objects.get(_id=pk)

    menu.name = data['name'],
    menu.details = data['details']
    menu.save()
    
    serializer = MenuSerializer(menu, many=False) 
    return Response(serializer.data)


# add new menu items for restaurant by employee and user
@api_view(['POST'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def createMenuItem(request, menu_id):
    try:
        menu_id = int(menu_id)
        menu = Menu.objects.get(_id=menu_id)
        
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.restaurant != menu.restaurant:
            return Response({'detail': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        existing_item = MenuItem.objects.filter(menu=menu, name=request.data.get('name'))
        if existing_item.exists():
            return Response({'detail': 'Menu Item with the same name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        data['menu'] = menu._id 
        data['createdBy'] = request.user.id
        serializer = MenuItemSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Menu.DoesNotExist:
        return Response({'detail': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)
 
# update new menu items for restaurant by employee and user 
@api_view(['PUT'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def updateMenuItem(request, menu_id, item_id):
    try:
        menu_id = int(menu_id)
        item_id = int(item_id)
        menu = Menu.objects.get(_id=menu_id)

        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.restaurant != menu.restaurant:
            return Response({'detail': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)

        item = MenuItem.objects.get(_id=item_id, menu=menu)

        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Menu.DoesNotExist:
        return Response({'detail': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)