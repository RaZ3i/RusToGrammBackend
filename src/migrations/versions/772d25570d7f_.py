"""empty message

Revision ID: 772d25570d7f
Revises: 0c9473e52f6d
Create Date: 2024-11-12 20:23:06.870207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '772d25570d7f'
down_revision: Union[str, None] = '0c9473e52f6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_subscribers', ['id'])
    op.drop_constraint('user_subscribers_user_id_fkey', 'user_subscribers', type_='foreignkey')
    op.create_foreign_key(None, 'user_subscribers', 'users_profiles', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'user_subscribes', ['id'])
    op.drop_constraint('user_subscribes_user_id_fkey', 'user_subscribes', type_='foreignkey')
    op.create_foreign_key(None, 'user_subscribes', 'users_profiles', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_subscribes', type_='foreignkey')
    op.create_foreign_key('user_subscribes_user_id_fkey', 'user_subscribes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user_subscribes', type_='unique')
    op.drop_constraint(None, 'user_subscribers', type_='foreignkey')
    op.create_foreign_key('user_subscribers_user_id_fkey', 'user_subscribers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user_subscribers', type_='unique')
    # ### end Alembic commands ###
