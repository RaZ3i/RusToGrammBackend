"""change post_id from integer type to string

Revision ID: 630bd3dc1337
Revises: af2e2273187f
Create Date: 2024-12-05 19:52:22.222786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '630bd3dc1337'
down_revision: Union[str, None] = 'af2e2273187f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_posts', 'post_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    op.create_unique_constraint(None, 'users_posts', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_posts', type_='unique')
    op.alter_column('users_posts', 'post_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
