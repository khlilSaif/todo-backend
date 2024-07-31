"""hello last db migration

Revision ID: 9d385e6ed24d
Revises: 01499b102082
Create Date: 2024-07-24 08:28:03.717630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d385e6ed24d'
down_revision: Union[str, None] = '01499b102082'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('blocked_task', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'task', ['blocked_task'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'blocked_task')
    # ### end Alembic commands ###
