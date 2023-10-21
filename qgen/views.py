
# Create your views here.
import re
from .serializers import QuestionSerializer, GenerateQuestionSerializer
from .models import Question
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import random
from .utils import getLevel 


@api_view(['GET', 'POST', 'PUT'])
def api_root(request, format=None):
    return Response({
        'All_Questions': reverse('questions', request=request, format=format),
        'Generate_Questions': reverse('generateQuestions', request=request, format=format)
    })


class QuestionViewSet(APIView):
    """
    List all questions, or create a new snippet.
    """

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        level=getLevel(request.data["question_text"])
        data=request.data
        data['level']=level
        print(data)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# individual question


class QuestionDetails(APIView):
    """
    Retrieve, update or delete a questions instance.
    """

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        questions = self.get_object(pk)
        serializer = QuestionSerializer(questions)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        questions = self.get_object(pk)
        serializer = QuestionSerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        questions = self.get_object(pk)
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenerateQuestionViewSet(APIView):
    """
    List all questionss, or create a new questions.
    """

    def post(self, request, format=None):
        questions = Question.objects.all().values()
        modules=request.data['modules']
        module_data={}
       
        for i in modules:
            module_data[i]=list(Question.objects.all().filter(module=i).values())
        
        ids_taken=[]

        partA=[]
        mod1_comp=random.sample(list(filter(lambda x:x['level']=="Comprehension",module_data[modules[0]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod1_comp)))

        mod2_comp=random.sample(list(filter(lambda x:x['level']=="Comprehension" and x['mark']=="3" and (x['id'] not in ids_taken),module_data[modules[1]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod2_comp)))

        mod1_appl=random.sample(list(filter(lambda x:x['level']=="Application" and x['mark']=="3" and (x['id'] not in ids_taken),module_data[modules[0]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod1_appl)))

        mod2_appl=random.sample(list(filter(lambda x:x['level']=="Application" and x['mark']=="3" and (x['id'] not in ids_taken),module_data[modules[1]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod2_appl)))

        partA=mod1_comp+mod2_comp+mod1_appl+mod2_appl


        partB=[]
        mod1_comp=random.sample(list(filter(lambda x:x['level']=="Comprehension" and x['mark']=="4" and (x['id'] not in ids_taken),module_data[modules[0]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod1_comp)))
        mod1_app=random.sample(list(filter(lambda x:x['level']=="Application" and x['mark']=="4" and (x['id'] not in ids_taken),module_data[modules[0]])),1)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod1_app)))
        mod2_app=random.sample(list(filter(lambda x:x['level']=="Application" and x['mark']=="4" and (x['id'] not in ids_taken),module_data[modules[1]])),2)
        ids_taken=ids_taken+list(map(lambda x:x['id'],list(mod2_app)))
        
        partB=mod1_comp+mod1_app+mod2_app


        
        partC=list(filter(lambda x:x['level']=="Analysis" and x['mark']=="2" and (x['module']==modules[0] or x['module']==modules[1]) and (x['id'] not in ids_taken) ,questions))
        if(len(partC)>0):
            partC=random.sample(partC,1)
        else:
            partC=list(filter(lambda x:x['level']=="Application" and x['mark']=="2" and (x['module']==modules[0] or x['module']==modules[1]) and (x['id'] not in ids_taken) ,questions))
            if (len(partC)>0):
                partC=random.sample(partC,1)

        results={}
        results['partA']=partA
        results['partB']=partB
        results['partC']=partC

        # serializer = GenerateQuestionSerializer(results, many=True)
        return Response(results)

# modules=[1,2]
# module_data={
#     1:[{id:1.qns:"abc"},{id:1.qns:"abc"},{id:1.qns:"abc"}],
#     2:[{id:1.qns:"abc"},{id:1.qns:"abc"},{id:1.qns:"abc"}],
# }
# module_data[modules[0]]=[{id:1.qns:"abc"},{id:1.qns:"abc"},{id:1.qns:"abc"}]