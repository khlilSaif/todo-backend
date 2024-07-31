"""hello last db migration

Revision ID: 52a3fe69c3da
Revises: 3c9898d0b522
Create Date: 2024-07-24 08:27:21.130655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52a3fe69c3da'
down_revision: Union[str, None] = '3c9898d0b522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('blocked_task', sa.Integer(), nullable=True))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_foreign_key(None, 'users', 'task', ['blocked_task'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'blocked_task')
    # ### end Alembic commands ###