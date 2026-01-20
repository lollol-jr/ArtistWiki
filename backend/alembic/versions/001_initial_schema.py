"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Artists table
    op.create_table(
        'artists',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=True),
        sa.Column('death_date', sa.Date, nullable=True),
        sa.Column('nationality', sa.String(100), nullable=True),
        sa.Column('biography', sa.Text, nullable=True),
        sa.Column('mediawiki_page_id', sa.Integer, unique=True, nullable=True),
        sa.Column('mediawiki_page_title', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index('idx_artists_name', 'artists', ['name'])
    op.create_index('idx_artists_type', 'artists', ['type'])
    op.create_index('idx_artists_mediawiki_page_id', 'artists', ['mediawiki_page_id'])

    # Works table
    op.create_table(
        'works',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('artist_id', UUID(as_uuid=True), sa.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('year', sa.Integer, nullable=True),
        sa.Column('type', sa.String(100), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('mediawiki_page_id', sa.Integer, unique=True, nullable=True),
        sa.Column('mediawiki_page_title', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index('idx_works_artist_id', 'works', ['artist_id'])
    op.create_index('idx_works_year', 'works', ['year'])
    op.create_index('idx_works_mediawiki_page_id', 'works', ['mediawiki_page_id'])

    # Relationships table
    op.create_table(
        'relationships',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('source_artist_id', UUID(as_uuid=True), sa.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_artist_id', UUID(as_uuid=True), sa.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False),
        sa.Column('relationship_type', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('idx_relationships_source', 'relationships', ['source_artist_id'])
    op.create_index('idx_relationships_target', 'relationships', ['target_artist_id'])
    op.create_unique_constraint(
        'uq_relationship',
        'relationships',
        ['source_artist_id', 'target_artist_id', 'relationship_type']
    )

    # Agent Jobs table
    op.create_table(
        'agent_jobs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('job_type', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('target_id', UUID(as_uuid=True), nullable=True),
        sa.Column('target_type', sa.String(50), nullable=True),
        sa.Column('input_data', JSONB, nullable=True),
        sa.Column('output_data', JSONB, nullable=True),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('started_at', sa.DateTime, nullable=True),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('idx_agent_jobs_status', 'agent_jobs', ['status'])
    op.create_index('idx_agent_jobs_job_type', 'agent_jobs', ['job_type'])
    op.create_index('idx_agent_jobs_target_id', 'agent_jobs', ['target_id'])


def downgrade() -> None:
    op.drop_table('agent_jobs')
    op.drop_table('relationships')
    op.drop_table('works')
    op.drop_table('artists')
