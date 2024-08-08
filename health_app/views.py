from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from openai import OpenAI
import openai
from .models import AppleHealthStat
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q, F
import json
from django.utils import timezone
from django.db.models import Sum, Avg
from datetime import timedelta

class StepComparisonView(APIView):
    def get(self, request):
        today = timezone.now().date()
        one_week_ago = today - timedelta(days=7)
        week_before_last = one_week_ago - timedelta(days=7)

        # Get all users
        users = User.objects.all()
        print(len(users)) # Debugging

        sleep_users = set()
        step_today_users = set()
        step_comparison_users = set()

        for user in users:
            # Condition 1: Users with a week of sleep less than 6 hours
            total_sleep = 0
            sleep_stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
           
            for stat in sleep_stats:
                if stat.sleepAnalysis:
                    for entry in stat.sleepAnalysis:
                        total_sleep += entry['sleep_time']
           
            if total_sleep < (6 * 3600):
                sleep_users.add(user.id)

           

            # Condition 2: Users who have reached 10,000 steps today
            today_stats = AppleHealthStat.objects.filter(user=user, created_at__date=today)
            total_steps_today = today_stats.aggregate(Sum('stepCount'))['stepCount__sum'] or 0
            if total_steps_today >= 10000:
                step_today_users.add(user.id)

          
            # Condition 3: Users who walked 50% less this week compared to the previous week
            last_week_steps = AppleHealthStat.objects.filter(
                user=user, created_at__date__gte=one_week_ago, created_at__date__lt=today
            ).aggregate(Sum('stepCount'))['stepCount__sum'] or 0
            
            week_before_last_steps = AppleHealthStat.objects.filter(
                user=user, created_at__date__gte=week_before_last, created_at__date__lt=one_week_ago
            ).aggregate(Sum('stepCount'))['stepCount__sum'] or 0

            
            if last_week_steps < week_before_last_steps * 0.5:
                step_comparison_users.add(user.id)
    

        # Combine results
        combined_user_ids = sleep_users & step_today_users & step_comparison_users # Intersection of all sets
        combined_users = User.objects.filter(id__in=combined_user_ids)

        responses = []
        for user in combined_users:
            advice = (
                f"Hello, {user.username}. I see that you have been sleeping less than 6 hours in the past week, "
                "reached 10,000 steps today, and walked 50% less this week compared to the previous week. "
                "It's important to maintain a balanced routine. Try to focus on improving your sleep quality, "
                "and gradually increase your physical activity to keep up with your goals."
            )
            responses.append({"user": user.username, "ai_response": advice})

        return Response(responses)
    
class AIResultView(APIView):
    def get(self, request):
        today = timezone.now().date()
        one_week_ago = today - timedelta(days=7)
        week_before_last = one_week_ago - timedelta(days=7)

        # Get all users
        users = User.objects.all()
      

        sleep_users = set()
        step_today_users = set()
        step_comparison_users = set()

        for user in users:
            # Condition 1: Users with a week of sleep less than 6 hours
            total_sleep = 0
            sleep_stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
           
            for stat in sleep_stats:
                if stat.sleepAnalysis:
                    for entry in stat.sleepAnalysis:
                        total_sleep += entry['sleep_time']
           
            if total_sleep < (6 * 3600):
                sleep_users.add(user.id)

           

            # Condition 2: Users who have reached 10,000 steps today
            today_stats = AppleHealthStat.objects.filter(user=user, created_at__date=today)
            total_steps_today = today_stats.aggregate(Sum('stepCount'))['stepCount__sum'] or 0
            if total_steps_today >= 10000:
                step_today_users.add(user.id)

          
            # Condition 3: Users who walked 50% less this week compared to the previous week
            last_week_steps = AppleHealthStat.objects.filter(
                user=user, created_at__date__gte=one_week_ago, created_at__date__lt=today
            ).aggregate(Sum('stepCount'))['stepCount__sum'] or 0
            
            week_before_last_steps = AppleHealthStat.objects.filter(
                user=user, created_at__date__gte=week_before_last, created_at__date__lt=one_week_ago
            ).aggregate(Sum('stepCount'))['stepCount__sum'] or 0

            
            if last_week_steps < week_before_last_steps * 0.5:
                step_comparison_users.add(user.id)


        # Combine results
        combined_user_ids = sleep_users & step_today_users & step_comparison_users # Intersection of all sets
        combined_users = User.objects.filter(id__in=combined_user_ids)

        responses = []
        for user in combined_users:
            # AI generated response
            # Add your OpenAI API key here
            client = OpenAI(api_key="")
            prompt = (
                f"You act as a health advisor for {user.username}. review the health data of the user and provide"
                "personalized advice to help them improve their health and fitness. The user has been sleeping less"
                "return response like: Hello, Anna. I see that you walked 15,000 steps today, which is 4,000 more than yesterday."
                "It's great that you are so active! I noticed that on days when you walk a lot, you sleep 20% better. "
                "Keep it up and continue in the same spirit to reach your goal." 
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens = 210,
                messages=[{
                    "role": "system",
                    "content":  prompt
                }, {
                    "role": "user",
                    "content": f"user : {user.username}, today's step count: {total_steps_today}, last week's step count: {last_week_steps}, week before last's step count: {week_before_last_steps}, total sleep time: {total_sleep}"
                }],
            )

            message_content = None
            choices = next(item for item in response if item[0] == "choices")
            if choices:
                message = next(item for item in choices[1][0] if item[0] == "message")
                if message:
                    content = next(item for item in message[1] if item[0] == "content")
                    if content:
                        message_content = content[1]
        
            responses.append({"user": user.username, "ai_response":  message_content})

        return Response(responses)


