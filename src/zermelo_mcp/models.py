"""Data models and date/time helpers for Zermelo API."""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field

# Zermelo is used by Dutch schools: dates and times without an explicit offset are local school time.
SCHOOL_TZ = ZoneInfo("Europe/Amsterdam")


def _local_midnight(day: date) -> datetime:
    return datetime.combine(day, time.min).replace(tzinfo=SCHOOL_TZ)


def parse_to_timestamp(value: Union[int, float, str, datetime, date]) -> int:
    """Convert flexible date/time inputs (UNIX timestamp, ISO string, 'YYYY-MM-DD', 'today', 'tomorrow') to UNIX timestamp in seconds.

    Dates and times without a UTC offset are interpreted as Dutch local time (Europe/Amsterdam).
    """
    if isinstance(value, (int, float)):
        return int(value)
    
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=SCHOOL_TZ)
        return int(value.timestamp())
    
    if isinstance(value, date):
        return int(_local_midnight(value).timestamp())
    
    if isinstance(value, str):
        val_str = value.strip().lower()
        now = datetime.now(SCHOOL_TZ)
        today = now.date()
        
        if val_str == "today":
            return int(_local_midnight(today).timestamp())
        if val_str == "tomorrow":
            return int(_local_midnight(today + timedelta(days=1)).timestamp())
        if val_str == "yesterday":
            return int(_local_midnight(today - timedelta(days=1)).timestamp())
        if val_str in ("now", "current"):
            return int(now.timestamp())
        
        # Check integer string
        if val_str.lstrip("-").isdigit():
            return int(val_str)
        
        # Try parsing ISO datetime format
        for fmt in (
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d-%m-%Y",
        ):
            try:
                dt = datetime.strptime(val_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=SCHOOL_TZ)
                return int(dt.timestamp())
            except ValueError:
                continue
                
    raise ValueError(f"Could not parse timestamp value: {value}")


class AppointmentCreate(BaseModel):
    """Schema for creating a Zermelo appointment."""
    start: int = Field(..., description="Start timestamp in seconds")
    end: int = Field(..., description="End timestamp in seconds")
    startTimeSlot: Optional[int] = Field(None, description="Start timeslot number")
    endTimeSlot: Optional[int] = Field(None, description="End timeslot number")
    subjects: List[str] = Field(default_factory=list, description="Subject codes (e.g. ['wisa'])")
    teachers: List[str] = Field(default_factory=list, description="Teacher codes (e.g. ['abc'])")
    groups: List[str] = Field(default_factory=list, description="Group codes (e.g. ['h4a'])")
    locations: List[str] = Field(default_factory=list, description="Location codes (e.g. ['101'])")
    type: str = Field("lesson", description="Type of appointment: lesson, exam, activity, etc.")
    remark: Optional[str] = Field("", description="Remark or note for the appointment")
    valid: bool = Field(True, description="Whether the appointment is valid")

    def to_api_dict(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data


class AnnouncementCreate(BaseModel):
    """Schema for creating a school announcement."""
    title: str = Field(..., description="Title of the announcement")
    text: str = Field(..., description="Body text of the announcement")
    start: int = Field(..., description="Start timestamp in seconds")
    end: int = Field(..., description="End timestamp in seconds")
    forStudents: bool = Field(True, description="Visible for students")
    forEmployees: bool = Field(True, description="Visible for employees")

    def to_api_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)
