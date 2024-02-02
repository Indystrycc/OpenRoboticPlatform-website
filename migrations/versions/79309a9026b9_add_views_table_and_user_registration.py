"""Add views table and user registration

Revision ID: 79309a9026b9
Revises: 5820e7dd0602
Create Date: 2023-07-26 15:51:51.637710

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79309a9026b9"
down_revision = "5820e7dd0602"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "view",
        sa.Column("view_event_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("ip", sa.String(length=45), nullable=True),
        sa.Column("part_id", sa.Integer(), nullable=False),
        sa.Column("event_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["part_id"],
            ["part.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("view_event_id"),
    )
    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.add_column(sa.Column("views", sa.Integer(), nullable=False))

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("date", sa.DateTime(), nullable=True))

    op.execute(
        """
        SET GLOBAL event_scheduler = ON;
        CREATE EVENT clearOldViews
        ON SCHEDULE EVERY 1 DAY
        DO
        UPDATE view SET ip=NULL, user_id=NULL
        WHERE TIMESTAMPDIFF(HOUR, view.event_date, NOW()) > 3;
        """
    )


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("date")

    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.drop_column("views")

    op.drop_table("view")
    op.execute(
        """
        DROP EVENT clearOldViews;
        SET GLOBAL event_scheduler = OFF;
        """
    )
