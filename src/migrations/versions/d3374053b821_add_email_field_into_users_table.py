"""add email field into users table

Revision ID: d3374053b821
Revises: fd1aad6e26fd
Create Date: 2024-10-29 20:00:15.890281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3374053b821'
down_revision: Union[str, None] = 'fd1aad6e26fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['id'])
    op.create_unique_constraint(None, 'users_profiles', ['id'])
    op.create_unique_constraint(None, 'users_protect', ['id'])
    op.create_unique_constraint(None, 'users_refresh_tokens', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_refresh_tokens', type_='unique')
    op.drop_constraint(None, 'users_protect', type_='unique')
    op.drop_constraint(None, 'users_profiles', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###