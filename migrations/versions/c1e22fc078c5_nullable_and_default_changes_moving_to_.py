"""Nullable and default changes (moving to declarative SA 2.0)

Revision ID: c1e22fc078c5
Revises: 1d21145a4fde
Create Date: 2023-09-17 00:16:13.546667

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c1e22fc078c5"
down_revision = "1d21145a4fde"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column(
            "name", existing_type=mysql.VARCHAR(length=50), nullable=False
        )

    with op.batch_alter_table("file", schema=None) as batch_op:
        batch_op.alter_column(
            "part_id", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )
        batch_op.alter_column(
            "file_name", existing_type=mysql.VARCHAR(length=100), nullable=False
        )

    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.alter_column(
            "name", existing_type=mysql.VARCHAR(length=200), nullable=False
        )
        batch_op.alter_column(
            "description", existing_type=mysql.VARCHAR(length=5000), nullable=False
        )
        batch_op.alter_column(
            "image", existing_type=mysql.VARCHAR(length=100), nullable=False
        )
        batch_op.alter_column(
            "category", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )
        batch_op.drop_constraint("part_ibfk_1", "foreignkey")
        batch_op.alter_column("user_id", existing_type=sa.UUID(), nullable=False)
        batch_op.create_foreign_key("part_ibfk_1", "user", ["user_id"], ["id"])
        batch_op.alter_column("date", existing_type=mysql.DATETIME(), nullable=False)
        batch_op.alter_column(
            "verified", existing_type=mysql.TINYINT(display_width=1), nullable=False
        )
        batch_op.alter_column(
            "featured", existing_type=mysql.TINYINT(display_width=1), nullable=False
        )
        batch_op.alter_column(
            "public", existing_type=mysql.TINYINT(display_width=1), nullable=False
        )
        batch_op.alter_column(
            "rejected", existing_type=mysql.TINYINT(display_width=1), nullable=False
        )
        batch_op.alter_column(
            "downloads", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )
        batch_op.alter_column(
            "tags", existing_type=mysql.VARCHAR(length=200), nullable=False
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "email", existing_type=mysql.VARCHAR(length=100), nullable=False
        )
        batch_op.alter_column(
            "password", existing_type=mysql.VARCHAR(length=163), nullable=False
        )
        batch_op.alter_column(
            "username", existing_type=mysql.VARCHAR(length=20), nullable=False
        )
        batch_op.alter_column(
            "confirmed", existing_type=mysql.TINYINT(display_width=1), nullable=False
        )
        batch_op.alter_column(
            "is_admin",
            existing_type=mysql.TINYINT(display_width=1),
            nullable=False,
            existing_server_default="0",
        )
        # Set all NULL dates to the earliest date supported by MariaDB
        batch_op.execute(
            "UPDATE user SET date='1001-01-01 00:00:00' WHERE date IS NULL"
        )
        batch_op.alter_column("date", existing_type=mysql.DATETIME(), nullable=False)


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("date", existing_type=mysql.DATETIME(), nullable=True)
        # Restore NULL dates
        batch_op.execute("UPDATE user SET date=NULL WHERE date='1001-01-01 00:00:00'")
        batch_op.alter_column(
            "is_admin",
            existing_type=mysql.TINYINT(display_width=1),
            nullable=True,
            existing_server_default="0",
        )
        batch_op.alter_column(
            "confirmed", existing_type=mysql.TINYINT(display_width=1), nullable=True
        )
        batch_op.alter_column(
            "username", existing_type=mysql.VARCHAR(length=20), nullable=True
        )
        batch_op.alter_column(
            "password", existing_type=mysql.VARCHAR(length=163), nullable=True
        )
        batch_op.alter_column(
            "email", existing_type=mysql.VARCHAR(length=100), nullable=True
        )

    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.alter_column(
            "tags", existing_type=mysql.VARCHAR(length=200), nullable=True
        )
        batch_op.alter_column(
            "downloads", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "rejected", existing_type=mysql.TINYINT(display_width=1), nullable=True
        )
        batch_op.alter_column(
            "public", existing_type=mysql.TINYINT(display_width=1), nullable=True
        )
        batch_op.alter_column(
            "featured", existing_type=mysql.TINYINT(display_width=1), nullable=True
        )
        batch_op.alter_column(
            "verified", existing_type=mysql.TINYINT(display_width=1), nullable=True
        )
        batch_op.alter_column("date", existing_type=mysql.DATETIME(), nullable=True)
        batch_op.drop_constraint("part_ibfk_1", "foreignkey")
        batch_op.alter_column("user_id", existing_type=sa.UUID(), nullable=True)
        batch_op.create_foreign_key("part_ibfk_1", "user", ["user_id"], ["id"])
        batch_op.alter_column(
            "category", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "image", existing_type=mysql.VARCHAR(length=100), nullable=True
        )
        batch_op.alter_column(
            "description", existing_type=mysql.VARCHAR(length=5000), nullable=True
        )
        batch_op.alter_column(
            "name", existing_type=mysql.VARCHAR(length=200), nullable=True
        )

    with op.batch_alter_table("file", schema=None) as batch_op:
        batch_op.alter_column(
            "file_name", existing_type=mysql.VARCHAR(length=100), nullable=True
        )
        batch_op.alter_column(
            "part_id", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )

    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column(
            "name", existing_type=mysql.VARCHAR(length=50), nullable=True
        )
