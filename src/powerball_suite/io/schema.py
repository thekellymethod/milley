from pydantic import BaseModel, Field
from datetime import date
from typing import List

class DrawRow(BaseModel):
    """
    Represents a single row of Powerball draw data.
    """
    draw_date = Field(..., description="The date of the draw")
    balls: List[int] = Field(..., description="List of drawn numbers") #always 5 numbers, values 1-69 inclusive
    powerball: int = Field(..., description="The Powerball number")
    multiplier: int = Field(..., description="Multiplier for the draw")
    jackpot: float = Field(..., description="Jackpot amount for the draw")

    @property
    def sorted_balls(self) -> List[int]:
        """
        Returns the drawn numbers sorted in ascending order.
        """
        return sorted(self.numbers)