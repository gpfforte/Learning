"""First Migration

Revision ID: e421aea74d76
Revises: 
Create Date: 2022-04-02 23:08:31.282484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e421aea74d76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    op.drop_table('user_account')
    # ### end Alembic commands ###