from flask_login import UserMixin

from src.extensions import bcrypt, db


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    sex = db.Column(db.Integer, nullable=False) # M:1, F:2 
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    daily_calorie_goal = db.Column(db.Float, nullable=False)
    
    # macro nutrients
    daily_carb_goal = db.Column(db.Float, nullable=False)
    daily_protein_goal = db.Column(db.Float, nullable=False)
    daily_fat_goal = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
    
    @classmethod
    def create_user(
        self,
        username: str,
        password: str
    ):
        pwd_hash = bcrypt.generate_password_hash(password=password)

        user = self(
            username=username,
            password=pwd_hash
        )

        db.session.add(user)
        db.session.commit()
        return None
    
    @classmethod
    def validate_login(
        self,
        username: str,
        password: str
    ) -> bool:
        user: self = (
            db.session.query(self)
            .filter(self.username == username)
            .first()
        )

        if not user:
            return False
        
        validated = bcrypt.check_password_hash(
            pw_hash=user.password,
            password=password
        )

        return validated

