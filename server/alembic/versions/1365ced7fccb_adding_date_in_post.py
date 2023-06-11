"""adding date in post

Revision ID: 1365ced7fccb
Revises: 2b4733e4a686
Create Date: 2023-06-11 15:12:13.947690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1365ced7fccb'
down_revision = '2b4733e4a686'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('date_added', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs', 'date_added')
    # ### end Alembic commands ###
