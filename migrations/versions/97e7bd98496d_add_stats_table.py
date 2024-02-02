"""add stats table

Revision ID: 97e7bd98496d
Revises: 79309a9026b9
Create Date: 2023-07-29 10:49:10.560728

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97e7bd98496d"
down_revision = "79309a9026b9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total_users", sa.Integer(), nullable=True),
        sa.Column("total_verified_users", sa.Integer(), nullable=True),
        sa.Column("total_parts", sa.Integer(), nullable=True),
        sa.Column("total_verified_parts", sa.Integer(), nullable=True),
        sa.Column("total_featured_parts", sa.Integer(), nullable=True),
        sa.Column("total_rejected_parts", sa.Integer(), nullable=True),
        sa.Column("total_files", sa.Integer(), nullable=True),
        sa.Column("total_views", sa.Integer(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        """
        CREATE EVENT updateStats
        ON SCHEDULE EVERY 5 MINUTE
        DO
        INSERT INTO stats (
            id,
            total_users,
            total_verified_users,
            total_parts,
            total_verified_parts,
            total_featured_parts,
            total_rejected_parts,
            total_files,
            total_views,
            date
        )
        SELECT
            1,
            COUNT(DISTINCT user.id),
            COUNT(DISTINCT CASE WHEN user.confirmed = true THEN user.id END),
            COUNT(DISTINCT part.id),
            COUNT(DISTINCT CASE WHEN part.verified = true THEN part.id END),
            COUNT(DISTINCT CASE WHEN part.featured = true THEN part.id END),
            COUNT(DISTINCT CASE WHEN part.rejected = true THEN part.id END),
            COUNT(DISTINCT file.id),
            SUM(part.views),
            NOW()
        FROM
            user
            LEFT JOIN part ON user.id = part.user_id
            LEFT JOIN file ON part.id = file.part_id
        ON DUPLICATE KEY UPDATE
            total_users = VALUES(total_users),
            total_verified_users = VALUES(total_verified_users),
            total_parts = VALUES(total_parts),
            total_verified_parts = VALUES(total_verified_parts),
            total_featured_parts = VALUES(total_featured_parts),
            total_rejected_parts = VALUES(total_rejected_parts),
            total_files = VALUES(total_files),
            total_views = VALUES(total_views),
            date = NOW()
    """
    )

    op.execute(
        """
        CREATE EVENT saveStats
        ON SCHEDULE EVERY 1 DAY
        STARTS CONCAT(CURRENT_DATE(), ' 23:59:00')
        DO
        INSERT INTO stats (
            total_users,
            total_verified_users,
            total_parts,
            total_verified_parts,
            total_featured_parts,
            total_rejected_parts,
            total_files,
            total_views,
            date
        )
        SELECT
            total_users,
            total_verified_users,
            total_parts,
            total_verified_parts,
            total_featured_parts,
            total_rejected_parts,
            total_files,
            total_views,
            NOW()
        FROM
            stats
        WHERE
            id = 1;
        """
    )


def downgrade():
    op.drop_table("stats")
    op.execute("DROP EVENT updateStats")
    op.execute("DROP EVENT saveStats")
