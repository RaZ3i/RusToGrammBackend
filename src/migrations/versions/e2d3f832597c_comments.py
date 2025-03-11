"""comments

Revision ID: e2d3f832597c
Revises: 7487afa35027
Create Date: 2025-02-20 14:55:45.421374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2d3f832597c'
down_revision: Union[str, None] = '7487afa35027'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_text', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['users_posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users_profiles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_comments')
    # ### end Alembic commands ###
