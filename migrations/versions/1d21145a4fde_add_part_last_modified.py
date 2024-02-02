"""Add part.last_modified

Revision ID: 1d21145a4fde
Revises: 1760d857367e
Create Date: 2023-09-15 01:23:55.059799

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1d21145a4fde"
down_revision = "1760d857367e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.add_column(sa.Column("last_modified", sa.DateTime(), nullable=True))

    # There is no trigger on part update, because views are stored in the same table
    # and the modification time would be executed on every view count update.


def downgrade():
    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.drop_column("last_modified")
