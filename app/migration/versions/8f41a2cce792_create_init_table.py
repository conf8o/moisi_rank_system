"""create init table

Revision ID: 8f41a2cce792
Revises: 
Create Date: 2023-04-16 13:00:59.788060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f41a2cce792'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry_players',
    sa.Column('entry_id', sa.Uuid(), nullable=False),
    sa.Column('player_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('player_id')
    )
    op.create_table('parties',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('match_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('party_players',
    sa.Column('party_id', sa.Uuid(), nullable=False),
    sa.Column('player_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['party_id'], ['parties.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('party_id', 'player_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('party_players')
    op.drop_table('parties')
    op.drop_table('entry_players')
    op.drop_table('players')
    op.drop_table('matches')
    op.drop_table('entries')
    # ### end Alembic commands ###
