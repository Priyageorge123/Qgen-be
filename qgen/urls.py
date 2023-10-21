from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'questions', views.QuestionViewSet)
# router.register(r'generateQuestion', views.GenerateQuestionViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('generate/', views.question_List),
#     path('api/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
    path('', views.api_root),
    path('questions/', views.QuestionViewSet.as_view(), name="questions"),
    path('questions/<int:pk>/', views.QuestionDetails.as_view(),
         name="singleQuestion"),
    path('generateQuestions/', views.GenerateQuestionViewSet.as_view(),
         name="generateQuestions"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
