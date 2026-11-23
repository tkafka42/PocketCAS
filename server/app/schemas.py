"""Ein- und Ausgabeformate der API (JSON in camelCase)."""

import uuid
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

InputSource = Literal["keypad", "camera", "drawing", "voice", "angle", "gps", "motion"]
ShortText = Annotated[str, Field(max_length=1000)]


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class LoginRequest(ApiModel):
    password: str = Field(min_length=1, max_length=256)


class SessionStatus(ApiModel):
    authenticated: bool


class CalcOptions(ApiModel):
    mode: Literal["auto", "exact", "approx"] = "auto"
    angle: Literal["rad", "deg", "grad"] = "rad"
    complex_format: Literal["real", "rectangular", "polar"] = "real"
    letters_are_constants: bool = False


class EvaluationRequest(ApiModel):
    expression: str = Field(min_length=1, max_length=4000)
    command: str | None = Field(default=None, max_length=40)
    arguments: list[ShortText] = Field(default_factory=list, max_length=8)
    # Frühere Definitionen (z. B. Define f(x)=x^2), der Server bleibt dadurch zustandslos.
    context: list[Annotated[str, Field(max_length=4000)]] = Field(default_factory=list, max_length=50)
    options: CalcOptions = Field(default_factory=CalcOptions)


class EvaluationResponse(ApiModel):
    source: str
    status: Literal["solved", "no_solution"]
    text: str
    latex: str | None = None
    decimal: str | None = None
    table: list[tuple[str, str]] | None = None
    output: list[str] = Field(default_factory=list)
    drawing: list[Any] = Field(default_factory=list)


class CommandInfo(ApiModel):
    name: str
    signature: str
    summary: str
    aliases: list[str]
    category: str
    offline: bool
    no_parentheses: bool


class TaskFields(ApiModel):
    input_source: InputSource
    raw_recognition: str | None = Field(default=None, max_length=10000)
    expression: str = Field(min_length=1, max_length=4000)
    command: str | None = Field(default=None, max_length=40)
    arguments: list[ShortText] = Field(default_factory=list, max_length=8)
    result_text: str | None = Field(default=None, max_length=100000)
    result_latex: str | None = Field(default=None, max_length=100000)
    result_decimal: str | None = Field(default=None, max_length=10000)
    measurements: dict[str, Any] | None = None


class TaskCreate(TaskFields):
    id: uuid.UUID
    created_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None


class TaskUpdate(TaskFields):
    updated_at: AwareDatetime
    recalculate: bool = False


class TaskRead(TaskFields):
    id: uuid.UUID
    has_image: bool
    created_at: datetime
    updated_at: datetime
