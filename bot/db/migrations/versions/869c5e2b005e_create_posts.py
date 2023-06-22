"""create posts

Revision ID: 869c5e2b005e
Revises: ddb36b25930a
Create Date: 2023-06-22 14:36:18.584163

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '869c5e2b005e'
down_revision = 'ddb36b25930a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('text', sa.TEXT(), nullable=False),
                    sa.Column('pr_type', sa.Enum('NONE', 'PUBLICATIONS', 'CLICKS', name='prtype'), nullable=True),
                    sa.Column('budget', sa.INTEGER(), nullable=True),
                    sa.Column('pub_price', sa.NUMERIC(precision=10, scale=2), nullable=True),
                    sa.Column('url_price', sa.NUMERIC(precision=10, scale=2), nullable=True),
                    sa.Column('subs_min', sa.INTEGER(), nullable=True),
                    sa.Column('author_id', sa.BIGINT(), nullable=True),
                    sa.Column('reg_date', sa.DATE(), nullable=True),
                    sa.Column('upd_date', sa.DATE(), nullable=True),
                    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('posts')
    # ### end Alembic commands ###
