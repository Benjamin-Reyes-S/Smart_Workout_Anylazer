



import pandas as pd


from typing import List, Literal
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


# -----------------------------
# 1. Load CSV
# -----------------------------

from pathlib import Path


# -----------------------------
# 2. Define structured output
# -----------------------------

"""
SessionType = Literal[
    "push",
    "pull",
    "legs",
    "upper",
    "lower",
    "full_body",
    "unknown"
]
"""

class DetectedExercise(BaseModel):
    canonical_name: str = Field(
        description="Clean human-readable exercise name, for example Bench Press"
    )
    raw_names_detected: List[str] = Field(
        description="All raw names or aliases found in the data file for this exercise"
    )
    track_for_progress: bool = Field(
        description="True only for bench_press, back_squat, or deadlift"
    )


class ExerciseExtractionResult(BaseModel):
    exercises: List[DetectedExercise]


# -----------------------------
# 3. Define prompt
# -----------------------------

prompt_detect_exercises = ChatPromptTemplate.from_messages([
        (
            "system",
            """
    You are a workout data normalization agent.

    Your task is to read raw training data and extract only the exercise names from all workout sessions.

    Instructions:
    1. Find all exercises in the provided training data.
    2. Group obvious aliases together but separate if the equipment differs.
    3. Generate a clean canonical_name.
    4. Do not extract dates.
    5. Do not extract sets.
    6. Do not extract reps.
    7. Do not extract weight.
    8. Do not invent exercises.
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
    model="llama3.1:8b",
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

# Load raw training data from CSV
raw_training_data = Path("data.csv").read_text(encoding="utf-8")

result = chain.invoke({
    "athlete_id": "benjamin",
    "raw_training_data": raw_training_data
})


# -----------------------------
# 8. Use result as a class object
# -----------------------------

print(result.model_dump_json(indent=2))
