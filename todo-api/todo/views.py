from django.shortcuts import render
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics

#region function based view

@api_view(['GET', 'POST'])
def all_todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        todo_deserializer = TodoSerializer(data=request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(todo_deserializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#endregion

#region class based view
    
class ManageTodoApiView(APIView):
    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        todo_deserializer = TodoSerializer(data=request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(todo_deserializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    
class TodosDetailApiView(APIView):
    def get_object(self, todo_id: int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#endregion
    
#region generics 
    
class TodoGenericsApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoGenenricsDetailedApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

#endregion