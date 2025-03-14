"""change table posts, add table photos

Revision ID: 1eb2829123e1
Revises: 225a480edb35
Create Date: 2024-12-05 22:16:04.619369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eb2829123e1'
down_revision: Union[str, None] = '225a480edb35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('file_link', sa.String(), nullable=False),
    sa.Column('file_weight', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['users_posts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.alter_column('users_posts', 'desscription',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=2200),
               existing_nullable=True)
    op.drop_column('users_posts', 'file_name')
    op.drop_column('users_posts', 'file_link')
    op.drop_column('users_posts', 'file_weight')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_posts', sa.Column('file_weight', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('users_posts', sa.Column('file_link', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users_posts', sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('users_posts', 'desscription',
               existing_type=sa.String(length=2200),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    op.drop_table('users_photos')
    # ### end Alembic commands ###
