"""empty message

Revision ID: 4fe952272be0
Revises: 97e1acdf2df3
Create Date: 2022-05-29 21:38:14.682871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fe952272be0'
down_revision = '97e1acdf2df3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'website_link')
    op.drop_column('artists', 'website_link')
    # ### end Alembic commands ###
