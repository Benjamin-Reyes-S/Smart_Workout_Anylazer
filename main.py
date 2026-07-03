from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END

class WorkoutState(TypedDict): 
    raw_path: str
    canonical_path: str | None
    metrics: dict[str, Any] | None
    plots: list[str]
    issues: list[str]

def normalize_workouts(state: WorkoutState) -> WorkoutState:
    raw_path = state["raw_path"]

    # TODO:
    # 1. Load CSV/Excel/JSON
    # 2. Detect columns
    # 3. Map exercise names
    # 4. Validate schema
    # 5. Save canonical CSV/Parquet

    return {
        **state,   # ** dictionary unpacking operator
        "canonical_path": "data/canonical/workouts.csv",
        "issues": []
    }


"""
def analyze_metrics(state: WorkoutState) -> WorkoutState:
    canonical_path = state["canonical_path"]

    # TODO:
    # - weekly volume
    # - estimated 1RM
    # - exercise PRs
    # - progression slope
    # - plateau detection

    metrics = {
        "weekly_volume_kg": {},
        "estimated_1rm": {},
        "plateaus": []
    }

    return {
        **state,
        "metrics": metrics
    }

def generate_plots(state: WorkoutState) -> WorkoutState:
    # TODO:
    # - matplotlib/plotly charts
    # - save PNG/HTML files

    return {
        **state,
        "plots": ["plots/bench_press_progress.png"]
    }

""" 

# Architecture of the Graph 
builder = StateGraph(WorkoutState)

builder.add_node("normalize", normalize_workouts)

#builder.add_node("analyze", analyze_metrics)
#builder.add_node("plot", generate_plots)

builder.add_edge(START, "normalize")
builder.add_edge("normalize", "analyze")
#builder.add_edge("analyze", "plot")
builder.add_edge("normalize", END)

graph = builder.compile()

result = graph.invoke({
    "raw_path": "data/raw/workouts.csv",
    "canonical_path": None,
    "metrics": None,
    "plots": [],
    "issues": []
})

print(result)