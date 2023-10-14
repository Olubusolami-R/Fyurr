"""empty message

Revision ID: ac15c871086f
Revises: e8e6411158c4
Create Date: 2022-05-29 14:16:21.658391

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac15c871086f'
down_revision = 'e8e6411158c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('arr', postgresql.ARRAY(sa.SMALLINT()), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###