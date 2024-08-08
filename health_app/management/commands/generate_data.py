import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from health_app.models import AppleHealthStat
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Dummy data store in sqlite'

    def handle(self, *args, **kwargs):
        # Create users with usernames from user0 to user9
        users = []
        for i in range(0, 10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password'
            )
            users.append(user)

        for user in users:
            # Ensure less than 6 hours of sleep for the current week
            total_sleep_time = 0
            for day_offset in range(7):
                date = timezone.now() - timedelta(days=day_offset)
                sleep_time = random.uniform(0, 3600)  

                total_sleep_time += sleep_time
                step_count = random.randint(0, 5000)
                if day_offset == 0:
                    step_count = 10000  

                AppleHealthStat.objects.create(
                    user=user,
                    dateOfBirth=timezone.make_aware(datetime.now() - timedelta(days=random.randint(7000, 25000))),
                    height=random.randint(150, 200),
                    bodyMass=random.randint(50, 120),
                    bodyFatPercentage=random.randint(10, 40),
                    biologicalSex=random.choice(["male", "female"]),
                    activityMoveMode=random.choice(["activeEnergy", "walk", "run"]),
                    stepCount=step_count,
                    basalEnergyBurned=random.randint(1000, 3000),
                    activeEnergyBurned=random.randint(100, 1000),
                    flightsClimbed=random.randint(0, 20),
                    appleExerciseTime=random.randint(0, 120),
                    appleMoveTime=random.randint(0, 120),
                    appleStandHour=random.randint(0, 24),
                    menstrualFlow=random.choice(["unspecified", "light", "medium", "heavy"]),
                    HKWorkoutTypeIdentifier=random.choice([None, "walking", "running"]),
                    heartRate=random.randint(50, 100),
                    oxygenSaturation=random.randint(90, 100),
                    mindfulSession={},
                    sleepAnalysis=[{"date": date.strftime("%Y-%m-%d %H:%M"), "sleep_time": sleep_time}],
                    created_at=date
                )


            for day_offset in range(7, 14):
                date = timezone.now() - timedelta(days=day_offset)
                sleep_time = random.uniform(2000, 2200)  

                step_count = random.randint(10000, 20000)  

                AppleHealthStat.objects.create(
                    user=user,
                    dateOfBirth=timezone.make_aware(datetime.now() - timedelta(days=random.randint(7000, 25000))),
                    height=random.randint(150, 200),
                    bodyMass=random.randint(50, 120),
                    bodyFatPercentage=random.randint(10, 40),
                    biologicalSex=random.choice(["male", "female"]),
                    activityMoveMode=random.choice(["activeEnergy", "walk", "run"]),
                    stepCount=step_count,
                    basalEnergyBurned=random.randint(1000, 3000),
                    activeEnergyBurned=random.randint(100, 1000),
                    flightsClimbed=random.randint(0, 20),
                    appleExerciseTime=random.randint(0, 120),
                    appleMoveTime=random.randint(0, 120),
                    appleStandHour=random.randint(0, 24),
                    menstrualFlow=random.choice(["unspecified", "light", "medium", "heavy"]),
                    HKWorkoutTypeIdentifier=random.choice([None, "walking", "running"]),
                    heartRate=random.randint(50, 100),
                    oxygenSaturation=random.randint(90, 100),
                    mindfulSession={},
                    sleepAnalysis=[{"date": date.strftime("%Y-%m-%d %H:%M"), "sleep_time": sleep_time}],
                    created_at=date
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated data.'))