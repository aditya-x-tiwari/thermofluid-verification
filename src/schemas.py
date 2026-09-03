from typing import Any, Literal
from pydantic import BaseModel, Field


class Axis(BaseModel):
    variable: str
    label: str
    scale: Literal["linear", "log", "unknown"] = "linear"
    unit: str | None = None


class Condition(BaseModel):
    name: str
    value: Any
    unit: str | None = None


class ReferenceSeries(BaseModel):
    name: str
    description: str | None = None
    data_source: Literal[
        "paper_table",
        "paper_curve",
        "digitized",
        "unknown"
    ] = "unknown"


class FigureSpec(BaseModel):
    figure_id: str
    page: int | None = None

    title: str | None = None
    caption: str | None = None

    purpose: Literal[
        "validation",
        "result",
        "comparison",
        "unknown"
    ]

    plot_type: Literal[
        "line",
        "scatter",
        "contour",
        "surface",
        "streamline",
        "heatline",
        "vector",
        "profile",
        "unknown"
    ]

    x: Axis | None = None
    y: Axis | None = None
    z: Axis | None = None

    fields_required: list[str] = Field(default_factory=list)

    conditions: list[Condition] = Field(default_factory=list)

    reference_series: list[ReferenceSeries] = Field(default_factory=list)

    notes: list[str] = Field(default_factory=list)


class PaperSpec(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None

    research_topic: str | None = None

    validation_figures: list[FigureSpec] = Field(default_factory=list)

    global_variables: list[str] = Field(default_factory=list)

    global_notes: list[str] = Field(default_factory=list)