from src.extensions import db


class FoodLog(db.Model):
    __tablename__ = 'FoodLog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('Food.id'), nullable=False)
    qty = db.Column(db.Float, nullable=False)
    
    date = db.Column(db.Date, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.qty}"