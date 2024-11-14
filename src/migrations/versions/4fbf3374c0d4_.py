"""empty message

Revision ID: 4fbf3374c0d4
Revises: 5037ea819d2c
Create Date: 2024-11-14 19:11:05.076985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fbf3374c0d4'
down_revision: Union[str, None] = '5037ea819d2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_subscribers_user_id_fkey', 'user_subscribers', type_='foreignkey')
    op.create_foreign_key(None, 'user_subscribers', 'users_profiles', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('user_subscribes_user_id_fkey', 'user_subscribes', type_='foreignkey')
    op.create_foreign_key(None, 'user_subscribes', 'users_profiles', ['id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_subscribes', type_='foreignkey')
    op.create_foreign_key('user_subscribes_user_id_fkey', 'user_subscribes', 'users_profiles', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user_subscribers', type_='foreignkey')
    op.create_foreign_key('user_subscribers_user_id_fkey', 'user_subscribers', 'users_profiles', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
