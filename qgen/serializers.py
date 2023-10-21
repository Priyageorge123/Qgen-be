from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'question_text',
            'level',
            'module',
            'mark',
            'created_at',
            'updated_at'
        )


class GenerateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'question_text',
            'level',
            'module',
            'mark',
        )

    def generate(self, data):
        data = super(QuestionSerializer, self).to_representation(data)
        return data
