"""add description column to users_profiles table

Revision ID: f79384e75e88
Revises: 0571ffb5b653
Create Date: 2024-10-31 14:14:34.536406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f79384e75e88'
down_revision: Union[str, None] = '0571ffb5b653'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_profiles', sa.Column('description', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_profiles', 'description')
    # ### end Alembic commands ###
