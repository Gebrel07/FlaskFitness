"""Initial migration

Revision ID: 5b940b692ab3
Revises: 
Create Date: 2023-04-22 16:12:05.535786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b940b692ab3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('brand_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('serving_size', sa.Float(), nullable=False),
    sa.Column('servings_per_container', sa.Float(), nullable=False),
    sa.Column('calories', sa.Float(), nullable=False),
    sa.Column('fat', sa.Float(), nullable=True),
    sa.Column('carbs', sa.Float(), nullable=True),
    sa.Column('prontein', sa.Float(), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('daily_calorie_goal', sa.Float(), nullable=True),
    sa.Column('daily_carb_goal', sa.Float(), nullable=True),
    sa.Column('daily_protein_goal', sa.Float(), nullable=True),
    sa.Column('daily_fat_goal', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('FoodLog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Float(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['Food.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('FoodLog')
    op.drop_table('User')
    op.drop_table('Food')
    # ### end Alembic commands ###
