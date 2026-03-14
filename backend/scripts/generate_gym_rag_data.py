# generate_gym_rag_data.py
import json
from datetime import date, timedelta
from pathlib import Path
import random

START_DATE = date(2026, 1, 1)
DAYS = 500
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

def day_of_week(d: date):
    return d.strftime("%A")

def phase_for_day(day_index: int):
    if day_index < 60:
        return "strength"
    if day_index < 90:
        return "plateau"
    if day_index < 105:
        return "deload"
    if day_index < 135:
        return "injury"
    return "recovery"

def is_rest_day(d: date):
    return d.weekday() == 6  # Sunday

# -----------------------------
# MEALS
# -----------------------------
def generate_meals_for_day(d: date, phase: str):
    meals = []

    if phase == "strength":
        qualities = ["good", "good", "average"]
    elif phase == "plateau":
        qualities = ["good", "average", "average", "bad"]
    elif phase == "deload":
        qualities = ["good", "average"]
    elif phase == "injury":
        qualities = ["average", "bad", "bad"]
    else:
        qualities = ["good", "average", "good"]

    meal_types = ["breakfast", "lunch", "dinner"]

    for meal_type in meal_types:
        quality = random.choice(qualities)

        if quality == "good":
            calories = random.randint(550, 850)
            protein = random.randint(35, 60)
            carbs = random.randint(50, 100)
            fat = random.randint(10, 25)
            desc = "Clean, high-protein meal with complex carbs."
        elif quality == "average":
            calories = random.randint(450, 700)
            protein = random.randint(20, 40)
            carbs = random.randint(50, 90)
            fat = random.randint(15, 30)
            desc = "Decent meal with some processed ingredients."
        else:
            calories = random.randint(800, 1500)
            protein = random.randint(10, 35)
            carbs = random.randint(80, 180)
            fat = random.randint(30, 70)
            desc = "Highly processed, low-quality meal."

        meals.append({
            "user_id": 1,
            "date": str(d),
            "name": meal_type.capitalize(),
            "description": desc,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "notes": f"{quality.capitalize()} {meal_type} during {phase} phase.",
            "metadata": {
                "quality": quality,
                "meal_type": meal_type,
                "phase": phase,
                "day_of_week": day_of_week(d)
            }
        })

    return meals

# -----------------------------
# WORKOUTS
# -----------------------------

WORKOUT_SPLIT = {
    "Monday": "chest",
    "Tuesday": "back",
    "Wednesday": "legs",
    "Thursday": "chest",
    "Friday": "back",
    "Saturday": "cardio",
    "Sunday": "rest"
}

CHEST_MOVES = [
    ("Bench Press", 5, 5),
    ("Incline Dumbbell Press", 4, 8),
    ("Chest Flys", 3, 12)
]

BACK_MOVES = [
    ("Deadlift", 5, 3),
    ("Barbell Row", 4, 8),
    ("Lat Pulldown", 3, 12)
]

LEG_MOVES = [
    ("Squat", 5, 5),
    ("Leg Press", 4, 10),
    ("Romanian Deadlift", 3, 8)
]

CARDIO_MOVES = [
    "30‑minute run",
    "20‑minute cycling session",
    "15‑minute rowing session"
]

def adjust_weight(prev, phase):
    if phase == "strength":
        return prev + random.randint(0, 5)
    if phase == "plateau":
        return prev + random.randint(-2, 1)
    if phase == "deload":
        return prev - random.randint(10, 20)
    if phase == "injury":
        return prev - random.randint(15, 30)
    if phase == "recovery":
        return prev + random.randint(1, 4)
    return prev

def generate_workout_for_day(d: date, day_index: int, prev_weights: dict):
    phase = phase_for_day(day_index)
    dow = day_of_week(d)
    workout_type = WORKOUT_SPLIT[dow]

    # REST DAY
    if workout_type == "rest":
        return {
            "user_id": 1,
            "date": str(d),
            "workout_text": "Rest day",
            "energy_level": random.randint(5, 7),
            "notes": "Recovery day, no lifting.",
            "metadata": {
                "phase": "rest",
                "day_of_week": dow,
                "is_rest_day": True,
                "quality": "neutral",
                "focus": "recovery",
                "movements": []
            }
        }, prev_weights

    # CARDIO DAY
    if workout_type == "cardio":
        movement = random.choice(CARDIO_MOVES)
        energy = random.randint(5, 8)
        quality = "good" if energy >= 7 else "average"

        return {
            "user_id": 1,
            "date": str(d),
            "workout_text": f"Cardio session: {movement}.",
            "energy_level": energy,
            "notes": "Cardio conditioning day.",
            "metadata": {
                "phase": phase,
                "day_of_week": dow,
                "is_rest_day": False,
                "quality": quality,
                "focus": "cardio",
                "movements": [movement]
            }
        }, prev_weights

    # LIFTING DAYS
    if workout_type == "chest":
        moves = CHEST_MOVES
        focus = "chest"
    elif workout_type == "back":
        moves = BACK_MOVES
        focus = "back"
    else:
        moves = LEG_MOVES
        focus = "legs"

    movement_texts = []
    movement_metadata = []

    for name, sets, reps in moves:
        prev = prev_weights.get(name, 135)
        new_weight = adjust_weight(prev, phase)
        new_weight = max(45, new_weight)

        movement_texts.append(f"{name}: {sets}x{reps} at {new_weight} lbs")
        movement_metadata.append({
            "movement": name,
            "sets": sets,
            "reps": reps,
            "weight": new_weight
        })

        prev_weights[name] = new_weight

    workout_text = "; ".join(movement_texts)
    energy = random.randint(5, 9)
    quality = "good" if energy >= 7 else "average" if energy >= 5 else "bad"

    workout = {
        "user_id": 1,
        "date": str(d),
        "workout_text": workout_text,
        "energy_level": energy,
        "notes": f"{focus.capitalize()} day training during {phase} phase.",
        "metadata": {
            "phase": phase,
            "day_of_week": dow,
            "is_rest_day": False,
            "quality": quality,
            "focus": focus,
            "movements": movement_metadata
        }
    }

    return workout, prev_weights

# -----------------------------
# MAIN
# -----------------------------
def main():
    workouts = []
    meals = []

    prev_weights = {}

    for i in range(DAYS):
        d = START_DATE + timedelta(days=i)
        phase = phase_for_day(i)

        meals.extend(generate_meals_for_day(d, phase))

        workout, prev_weights = generate_workout_for_day(d, i, prev_weights)
        workouts.append(workout)

    with open(OUTPUT_DIR / "workouts.json", "w", encoding="utf-8") as f:
        json.dump(workouts, f, indent=2)

    with open(OUTPUT_DIR / "meals.json", "w", encoding="utf-8") as f:
        json.dump(meals, f, indent=2)

    print(f"Generated {len(workouts)} workouts and {len(meals)} meals.")

if __name__ == "__main__":
    main()
