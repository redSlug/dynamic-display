"""Add author field to messages

Revision ID: deee3df6a2e7
Revises: d936dbdd0863
Create Date: 2018-06-18 13:01:00.014104

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "deee3df6a2e7"
down_revision = "d936dbdd0863"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("messages", sa.Column("author", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("messages", "author")
    # ### end Alembic commands ###
