"""empty message

Revision ID: 80af19486a4b
Revises: 1f163f172003
Create Date: 2022-07-11 16:03:29.874685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80af19486a4b'
down_revision = '1f163f172003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temporary_table',
    sa.Column('temp_id', sa.Integer(), nullable=False),
    sa.Column('temp_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('temp_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temporary_table')
    # ### end Alembic commands ###
