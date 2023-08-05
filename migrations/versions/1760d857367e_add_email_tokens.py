"""Add email tokens

Revision ID: 1760d857367e
Revises: 97e7bd98496d
Create Date: 2023-08-02 03:33:30.251394

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1760d857367e"
down_revision = "97e7bd98496d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "email_token",
        sa.Column("token", sa.BINARY(length=32), nullable=False),
        sa.Column(
            "token_type",
            sa.Enum("mail_confirmation", "password_reset", name="tokentype"),
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token"),
    )
    with op.batch_alter_table("view") as batch_op:
        batch_op.drop_constraint("view_ibfk_2", "foreignkey")
        batch_op.create_foreign_key(
            "view_ibfk_2", "user", ["user_id"], ["id"], ondelete="SET NULL"
        )
    # Delete old unused tokens after 5 days
    op.execute(
        """
        CREATE EVENT removeOldTokens
        ON SCHEDULE EVERY 1 DAY
        DO
        DELETE FROM email_token
        WHERE TIMESTAMPDIFF(DAY, email_token.created_on, NOW()) >= 5;
        """
    )
    # Delete accounts without a confirmed email after a month
    op.execute(
        """
        CREATE EVENT removeUnconfirmedAccounts
        ON SCHEDULE EVERY 1 DAY
        DO
        DELETE FROM user
        WHERE user.confirmed = FALSE AND TIMESTAMPDIFF(MONTH, user.date, NOW()) >= 1;
        """
    )


def downgrade():
    op.execute("DROP EVENT removeUnconfirmedAccounts")
    op.execute("DROP EVENT removeOldTokens")
    with op.batch_alter_table("view") as batch_op:
        batch_op.drop_constraint("view_ibfk_2", "foreignkey")
        batch_op.create_foreign_key("view_ibfk_2", "user", ["user_id"], ["id"])
    op.drop_table("email_token")
