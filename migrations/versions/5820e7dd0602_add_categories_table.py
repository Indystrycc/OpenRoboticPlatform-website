"""Add categories table

Revision ID: 5820e7dd0602
Revises: 6139f6e9a81a
Create Date: 2023-06-29 00:52:26.957222

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5820e7dd0602"
down_revision = "6139f6e9a81a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic and manually modified ###
    categories_table = op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # insert default categories
    op.bulk_insert(
        categories_table,
        [
            # plates
            {"id": 1, "name": "Plates", "parent_id": None},
            {"id": 2, "name": "Rectangular", "parent_id": 1},
            {"id": 3, "name": "Circular", "parent_id": 1},
            {"id": 4, "name": "Oval", "parent_id": 1},
            {"id": 5, "name": "Special", "parent_id": 1},
            {"id": 6, "name": "Weird", "parent_id": 1},
            # holders
            {"id": 7, "name": "Holders", "parent_id": None},
            {"id": 8, "name": "Motors", "parent_id": 7},
            {"id": 9, "name": "Sensors", "parent_id": 7},
            {"id": 10, "name": "Microcontrollers and SBCs", "parent_id": 7},
            {"id": 11, "name": "Cameras", "parent_id": 7},
            {"id": 12, "name": "Batteries", "parent_id": 7},
            {"id": 13, "name": "Other", "parent_id": 7},
            {"id": 14, "name": "Special", "parent_id": 7},
            # wheels
            {"id": 15, "name": "Wheels", "parent_id": None},
            {"id": 16, "name": "Smooth", "parent_id": 15},
            {"id": 17, "name": "Normal", "parent_id": 15},
            {"id": 18, "name": "Terrain", "parent_id": 15},
            {"id": 19, "name": "Spikes", "parent_id": 15},
            {"id": 20, "name": "Special", "parent_id": 15},
            # connection rods
            {"id": 21, "name": "Connection rods", "parent_id": None},
            {"id": 22, "name": "One hole", "parent_id": 21},
            {"id": 23, "name": "Multi holes", "parent_id": 21},
            {"id": 24, "name": "Special", "parent_id": 21},
        ],
    )
    # update category ids in parts and create the foreign key
    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.execute(
            """
            UPDATE part SET category =
                CASE
                    WHEN category = 1 THEN 1
                    WHEN category = 2 THEN 15
                    WHEN category = 3 THEN 13
                    WHEN category = 4 THEN 9
                    WHEN category = 5 THEN 10
                    WHEN category = 6 THEN 8
                    WHEN category = 7 THEN 11
                END
            """
        )
        batch_op.create_foreign_key(
            "part_fk_category", "category", ["category"], ["id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic and manually adjusted ###
    with op.batch_alter_table("part", schema=None) as batch_op:
        batch_op.drop_constraint("part_fk_category", type_="foreignkey")

    # Restore previous category IDs (default to "Other")
    op.execute(
        """
        UPDATE part SET category =
            CASE
                WHEN category BETWEEN 1 AND 6 THEN 1
                WHEN category BETWEEN 15 AND 20 THEN 2
                WHEN category = 9 THEN 4
                WHEN category = 10 THEN 5
                WHEN category = 8 THEN 6
                WHEN category = 11 THEN 7
                ELSE 3
            END
        """
    )

    op.drop_table("category")
    # ### end Alembic commands ###