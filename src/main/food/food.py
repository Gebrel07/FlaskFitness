from datetime import datetime

from src.extensions import db


class Food(db.Model):
    __tablename__ = 'Food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    serving_size = db.Column(db.Float, nullable=False)
    servings_per_container = db.Column(db.Float, nullable=False)

    calories = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    prontein = db.Column(db.Float)

    date_added = db.Column(db.Date, nullable=False)
    date_edited = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

    @classmethod
    def add_food(
        self,
        name: str,
        brand_name: str,
        description: str,
        serving_size: float,
        serving_size_unit: str,
        servings_per_container: float,
        calories: float,
        fat: float,
        carbs: float,
        prontein: float
    ):
        f = self(
            name=name,
            brand_name=brand_name,
            description=description,
            serving_size=serving_size,
            serving_size_unit=serving_size_unit,
            servings_per_container=servings_per_container,
            calories=calories,
            fat=fat,
            carbs=carbs,
            prontein=prontein,
            date_added=datetime.now().date()
        )

        db.session.add(f)
        db.session.commit()
        return None

    @classmethod
    def edit_food(
        self,
        id: int,
        name: str,
        brand_name: str,
        description: str,
        serving_size: float,
        serving_size_unit: str,
        servings_per_container: float,
        calories: float,
        fat: float,
        carbs: float,
        prontein: float
    ):
        f: self = self.query.get(id)

        f.name=name
        f.brand_name=brand_name
        f.description=description
        f.serving_size=serving_size
        f.serving_size_unit=serving_size_unit
        f.servings_per_container=servings_per_container
        f.calories=calories
        f.fat=fat
        f.carbs=carbs
        f.prontein=prontein
        f.date_edited=datetime.now().date()

        db.session.commit()
        return None
