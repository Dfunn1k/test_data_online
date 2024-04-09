from .database import base
from sqlalchemy import Column, Integer, TIMESTAMP, Float
from sqlalchemy.orm import relationship


class Data(base):
    __tablename__ = "datos"

    id = Column(Integer, primary_key=True)
    Simulation_Examples_Functions_Sine1_NUMERICID = Column(Integer)
    Simulation_Examples_Functions_Sine1_QUALITY = Column(Integer)
    Simulation_Examples_Functions_Sine1_TIMESTAMP = Column(TIMESTAMP)
    Simulation_Examples_Functions_Sine1_VALUE = Column(Float)
