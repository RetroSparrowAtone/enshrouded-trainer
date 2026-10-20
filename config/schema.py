"""Pydantic config schema for enshrouded-trainer."""
from __future__ import annotations

from pydantic import BaseModel, Field


class EspConfig(BaseModel):
    enabled: bool = False
    show_names: bool = True
    box_color: str = "#00FF88"


class AimbotConfig(BaseModel):
    enabled: bool = False
    fov_degrees: float = Field(default=8.0, ge=1.0, le=90.0)
    smoothing: float = Field(default=0.35, ge=0.0, le=1.0)
    target_bone: str = "head"


class TrainerConfig(BaseModel):
    esp: EspConfig = EspConfig()
    aimbot: AimbotConfig = AimbotConfig()
    hotkey_prefix: str = "f"
    log_level: str = "INFO"