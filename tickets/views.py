from django.shortcuts import render
from django.http.response import JsonResponse  
from .models import Guest, Reservation, Movie, Reservation, Post
from rest_framework.decorators import api_view 
from rest_framework import status, filters
from rest_framework.response import Response 
from . serializers import Guestserializer , MovieSerializer, ReservationSerializer,PostSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics,mixins
from rest_framework import viewsets

from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly


#1 without Rest and no model query

def no_rest_no_model(request):

    guests = [
        {
            'id': 1,
            'name': 'omar',
            'mobile': 123143111 ,
        },
        {
            'id': 2,
            'name': 'amr',
            'mobile': 745747 ,
        }
    ]

    return JsonResponse(guests, safe= False)

#2 no_rest_from model

def no_rest_from_model(request):
    data = Guest.objects.all()
    respone = {
        'guests' : list(data.values('name', 'mobile'))
    }
    return JsonResponse(respone)



# List  == Get
# Create == Post

# pk query = Get
# Update == Put
# Delete destroy == Delete


#3  Function based views

# 3.1 GET POST
@api_view(['GET', 'POST'])
def FBV_List(request,):
    # Get
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = Guestserializer(guests, many=True)
        return Response(serializer.data)

    # Post
    elif request.method == 'POST':
        serializer = Guestserializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)



    


# 3.2 Get PUT DELETE

@api_view(['GET','PUT','DELETE'])
def  FBV_Pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Get
    if request.method == 'GET':
        serializer = Guestserializer(guest)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = Guestserializer(guest,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # Delete
    if request.method == 'DELETE':
        guest.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


#4 CBV class based views

# 4.1 List and Create == GET and POST

class CBV_List(APIView):
    # get
    def get(self, request):
        guests =  Guest.objects.all()
        serializer = Guestserializer(guests, many=True)
        return Response(serializer.data)
    
    #post
    def post(self, request):
        serializer = Guestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
        
# 4.2 GET PUT DELETE class based views -- pk

class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        
        except Guest.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = Guestserializer(guest)
        return Response(serializer.data)

    def put(self,request ,pk):
        guest = self.get_object(pk)
        serializer = Guestserializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#5 mixins

# 5.1 mixins list

class mixins_list(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, # write code instead of you
    generics.GenericAPIView  # respone instead of you
):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

# 5.2 get put delete

class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer

    def get(self,request, pk):
        return self.retrieve(request)
    
    def put(self,request, pk):
        return self.update(request)

    def delete(self,request, pk):
        return self.destroy(request)

    
# 6 Generics

# 6.1 get and post
class  generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer 
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
#6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Guest.objects.all()
    serializer_class = Guestserializer 
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    


### I implement the project by viewset


# 7 viewsets

class viewsets_guest(viewsets.ModelViewSet):
    
    queryset = Guest.objects.all()
    serializer_class = Guestserializer 
    

class viewsets__movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets__resrvation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer



# 8 Find movies , انا عملتها فى الطريقة 7 بس انا عايز اكتب الكود

@api_view(['Get'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie = request.data['movie'],
        hall = request.data['hall'],
    )
    serializer = MovieSerializer(movies,many=True)
    return Response(serializer.data)



# 9 create new reservation 

@api_view(['Create'])

def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie =request.data['movie']
    )
    # if the guest is new
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation= Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)



# 10 post author editor

class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer