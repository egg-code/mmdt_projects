from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# Create a class for the table capital_weather
class Capital_Weather(Base):
    __tablename__ = "capital_weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    Capital: Mapped[str] = mapped_column(nullable=False)
    Country: Mapped[str] = mapped_column(nullable=False)
    Country_Population: Mapped[int] = mapped_column()
    Capital_lat: Mapped[float] = mapped_column()
    Capital_long: Mapped[float] = mapped_column()
    Capital_Weather: Mapped[str] = mapped_column()
    Capital_Min_Temp: Mapped[float] = mapped_column()
    Capital_Max_Temp: Mapped[float] = mapped_column()
    