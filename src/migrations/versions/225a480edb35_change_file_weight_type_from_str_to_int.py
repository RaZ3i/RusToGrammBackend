"""change file_weight type from str to int

Revision ID: 225a480edb35
Revises: ddf7b1f76a1f
Create Date: 2024-12-05 20:53:08.550565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '225a480edb35'
down_revision: Union[str, None] = 'ddf7b1f76a1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_posts', 'file_weight',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Integer(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_posts', 'file_weight',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###