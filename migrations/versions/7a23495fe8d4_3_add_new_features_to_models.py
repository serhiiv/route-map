"""3 Add new features to models

Revision ID: 7a23495fe8d4
Revises: 2e1706e0c022
Create Date: 2019-01-03 12:28:42.415571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a23495fe8d4'
down_revision = '2e1706e0c022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice', sa.Column('city', sa.String(length=40), nullable=True))
    op.add_column('invoice', sa.Column('city_lat', sa.Float(), nullable=True))
    op.add_column('invoice', sa.Column('city_lon', sa.Float(), nullable=True))
    op.add_column('invoice', sa.Column('client_name', sa.String(length=250), nullable=True))
    op.add_column('invoice', sa.Column('client_nickname', sa.String(length=32), nullable=True))
    op.add_column('invoice', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('invoice', sa.Column('lat', sa.Float(), nullable=True))
    op.add_column('invoice', sa.Column('lon', sa.Float(), nullable=True))
    op.add_column('invoice', sa.Column('volume', sa.Float(), nullable=True))
    op.add_column('route', sa.Column('car', sa.String(length=50), nullable=True))
    op.add_column('route', sa.Column('car_volume', sa.Float(), nullable=True))
    op.add_column('route', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('route', 'date')
    op.drop_column('route', 'car_volume')
    op.drop_column('route', 'car')
    op.drop_column('invoice', 'volume')
    op.drop_column('invoice', 'lon')
    op.drop_column('invoice', 'lat')
    op.drop_column('invoice', 'date')
    op.drop_column('invoice', 'client_nickname')
    op.drop_column('invoice', 'client_name')
    op.drop_column('invoice', 'city_lon')
    op.drop_column('invoice', 'city_lat')
    op.drop_column('invoice', 'city')
    # ### end Alembic commands ###
