"""Init

Revision ID: ec4cb5bebddd
Revises: ce2be1d9a47a
Create Date: 2023-12-31 15:03:13.190906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec4cb5bebddd'
down_revision: Union[str, None] = 'ce2be1d9a47a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'refresh_token')
    # ### end Alembic commands ###
