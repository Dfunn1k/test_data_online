from pydantic import BaseModel
from datetime import datetime


class Data(BaseModel):
    # id: int
    # Simulation_Examples_Functions_Sine1_NUMERICID: int
    # Simulation_Examples_Functions_Sine1_QUALITY: int
    Simulation_Examples_Functions_Sine1_TIMESTAMP: datetime
    Simulation_Examples_Functions_Sine1_VALUE: float


