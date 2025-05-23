"""add send_time to message table

Revision ID: c0aefa797a6f
Revises: 51dcc1f5dddf
Create Date: 2025-04-03 21:07:50.266317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0aefa797a6f'
down_revision: Union[str, None] = '51dcc1f5dddf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('send_time', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    op.create_unique_constraint(None, 'messages', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='unique')
    op.drop_column('messages', 'send_time')
    # ### end Alembic commands ###
