



import pandas as pd


from typing import List, Literal
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


# -----------------------------
# 1. Load CSV
# -----------------------------

data = pd.read_csv("data.csv")

raw_training_data = data.to_csv(index=False)


# -----------------------------
# 2. Define structured output
# -----------------------------

SessionType = Literal[
    "push",
    "pull",
    "legs"
]


class DetectedExercise(BaseModel):
    exercise_id: str = Field(
        description="Canonical snake_case ID, for example bench_press, back_squat, deadlift"
    )
    canonical_name: str = Field(
        description="Clean human-readable exercise name, for example Bench Press"
    )
    raw_names_detected: List[str] = Field(
        description="All raw names or aliases found in the CSV for this exercise"
    )
    likely_session_type: SessionType = Field(
        description="Most likely session type where this exercise appears"
    )
    track_for_progress: bool = Field(
        description="True only for bench_press, back_squat, or deadlift"
    )


class ExerciseExtractionResult(BaseModel):
    athlete_id: str
    exercises: List[DetectedExercise]


# -----------------------------
# 3. Define prompt
# -----------------------------

prompt_detect_exercises = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a workout data normalization agent.

Your task is to read raw training data from a CSV and extract only the exercise names.

Instructions:
1. Find all exercises in the full dataset.
2. Group obvious aliases together.
   Example: "Bench", "Bench Press", "Barbell Bench" should become bench_press.
3. Generate a canonical snake_case exercise_id.
4. Generate a clean canonical_name.
5. Detect the likely session type: push, pull, legs, upper, lower, full_body, or unknown.
6. Set track_for_progress=true only for:
   - bench_press
   - back_squat
   - deadlift

Do not extract dates yet.
Do not extract sets yet.
Do not extract reps or weight yet.
Only return the exercise dictionary.
"""
    ),
    (
        "human",
        """
Athlete ID: {athlete_id}

Raw training data:
{raw_training_data}
"""
    )
])


# -----------------------------
# 4. Create model
# -----------------------------

model = ChatOllama(
    model="llama2:7b-chat",  # Replace with the exact name from `ollama list`
    temperature=0
)


# -----------------------------
# 5. Force structured output
# -----------------------------

structured_model = model.with_structured_output(ExerciseExtractionResult)


# -----------------------------
# 6. Build chain
# -----------------------------

chain = prompt_detect_exercises | structured_model


# -----------------------------
# 7. Invoke chain
# -----------------------------

result = chain.invoke({
    "athlete_id": "benjamin",
    "raw_training_data": raw_training_data
})


# -----------------------------
# 8. Use result as a class object
# -----------------------------

print(type(result))
print(result)