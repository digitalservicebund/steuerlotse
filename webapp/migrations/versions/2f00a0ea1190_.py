"""empty message

Revision ID: 2f00a0ea1190
Revises: 
Create Date: 2021-04-01 10:51:48.889545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f00a0ea1190'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idnr_hashed', sa.String(), nullable=False),
    sa.Column('dob_hashed', sa.String(), nullable=False),
    sa.Column('elster_request_id', sa.String(), nullable=False),
    sa.Column('unlock_code_hashed', sa.String(), nullable=True),
    sa.Column('pdf', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('idnr_hashed')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###