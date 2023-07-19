from dataclasses import dataclass
from datetime import date


@dataclass
class Cards:
    id: int
    project_id: int
    collected: bool
    pomo_count: int
    price_per_hour: float | None
    total_price: float | None
    created_at: date


@dataclass
class Project:
    id: int
    name: str
    price_per_hour: float | None
    salary_collected: float | None
    pending_salary: float | None
    total_money: float | None
    cards: list[Cards]
