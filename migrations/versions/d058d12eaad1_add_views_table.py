"""add views table

Revision ID: d058d12eaad1
Revises: 5820e7dd0602
Create Date: 2023-07-24 13:51:30.053530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d058d12eaad1"
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
        sa.Column("event_date", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("view_event_id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["part_id"],
            ["part.id"],
        ),
    )

    op.add_column("part", sa.Column("views", sa.Integer(), nullable=False, default=0))
    op.add_column(
        "user",
        sa.Column("date", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        """
        SET GLOBAL event_scheduler = OFF;
        CREATE EVENT clearOldViews
        ON SCHEDULE EVERY 1 DAY
        DO
        UPDATE view SET ip=Null, user_id=Null
        WHERE TIMESTAMPDIFF(HOUR, view.event_date, NOW()) > 3;
        """
    )


def downgrade():
    op.drop_table("view")
    op.drop_column("part", "views")
    op.drop_column("user", "date")
    op.execute("drop event clearOldViews")
