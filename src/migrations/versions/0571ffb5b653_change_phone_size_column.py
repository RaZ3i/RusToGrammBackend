"""change phone size column

Revision ID: 0571ffb5b653
Revises: d3374053b821
Create Date: 2024-10-31 13:13:07.216170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0571ffb5b653'
down_revision: Union[str, None] = 'd3374053b821'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=11),
               type_=sa.String(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=11),
               existing_nullable=False)
    # ### end Alembic commands ###