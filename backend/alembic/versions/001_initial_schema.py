"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-03-30 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Dogs
    op.create_table('dogs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('breed', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('sex', sa.Enum('MALE', 'FEMALE', 'UNKNOWN', name='sexenum'), nullable=True),
        sa.Column('weight_kg', sa.Float(), nullable=True),
        sa.Column('avatar_image_url', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], name=op.f('fk_dogs_owner_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_dogs'))
    )
    op.create_index(op.f('ix_dogs_id'), 'dogs', ['id'], unique=False)
    op.create_index(op.f('ix_dogs_owner_user_id'), 'dogs', ['owner_user_id'], unique=False)

    # Dog Profile Details
    op.create_table('dog_profile_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('forbidden_foods', sa.Text(), nullable=True),
        sa.Column('preferred_foods', sa.Text(), nullable=True),
        sa.Column('diagnosed_conditions', sa.Text(), nullable=True),
        sa.Column('care_notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_dog_profile_details_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_dog_profile_details')),
        sa.UniqueConstraint('dog_id', name=op.f('uq_dog_profile_details_dog_id'))
    )
    op.create_index(op.f('ix_dog_profile_details_id'), 'dog_profile_details', ['id'], unique=False)

    # Vet Visits
    op.create_table('vet_visits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('vet_name', sa.String(), nullable=True),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('treatment_and_medication', sa.Text(), nullable=True),
        sa.Column('notes_markdown', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_vet_visits_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_vet_visits'))
    )
    op.create_index(op.f('ix_vet_visits_id'), 'vet_visits', ['id'], unique=False)

    # Vaccinations
    op.create_table('vaccinations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('vaccine_type', sa.String(), nullable=False),
        sa.Column('valid_until', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_vaccinations_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_vaccinations'))
    )
    op.create_index(op.f('ix_vaccinations_id'), 'vaccinations', ['id'], unique=False)

    # Invoices
    op.create_table('invoices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=True),
        sa.Column('vet_visit_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('file_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_invoices_dog_id_dogs')),
        sa.ForeignKeyConstraint(['vet_visit_id'], ['vet_visits.id'], name=op.f('fk_invoices_vet_visit_id_vet_visits')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_invoices'))
    )
    op.create_index(op.f('ix_invoices_id'), 'invoices', ['id'], unique=False)

    # Care Tasks
    op.create_table('care_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('interval_type', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', 'CUSTOM_DAYS', name='intervaltype'), nullable=False),
        sa.Column('interval_days', sa.Integer(), nullable=True),
        sa.Column('next_due_date', sa.Date(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_care_tasks_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_care_tasks'))
    )
    op.create_index(op.f('ix_care_tasks_id'), 'care_tasks', ['id'], unique=False)

    # Care Task Logs
    op.create_table('care_task_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('care_task_id', sa.Integer(), nullable=False),
        sa.Column('done_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['care_task_id'], ['care_tasks.id'], name=op.f('fk_care_task_logs_care_task_id_care_tasks')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_care_task_logs'))
    )
    op.create_index(op.f('ix_care_task_logs_id'), 'care_task_logs', ['id'], unique=False)

    # Training Goals
    op.create_table('training_goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'PAUSED', name='goalstatus'), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_training_goals_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_training_goals'))
    )
    op.create_index(op.f('ix_training_goals_id'), 'training_goals', ['id'], unique=False)

    # Behavior Issues
    op.create_table('behavior_issues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('typical_triggers', sa.Text(), nullable=True),
        sa.Column('severity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_behavior_issues_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_behavior_issues'))
    )
    op.create_index(op.f('ix_behavior_issues_id'), 'behavior_issues', ['id'], unique=False)

    # Training Logs
    op.create_table('training_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('training_goal_id', sa.Integer(), nullable=True),
        sa.Column('behavior_issue_id', sa.Integer(), nullable=True),
        sa.Column('datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('notes_markdown', sa.Text(), nullable=True),
        sa.Column('video_urls_json', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['behavior_issue_id'], ['behavior_issues.id'], name=op.f('fk_training_logs_behavior_issue_id_behavior_issues')),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_training_logs_dog_id_dogs')),
        sa.ForeignKeyConstraint(['training_goal_id'], ['training_goals.id'], name=op.f('fk_training_logs_training_goal_id_training_goals')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_training_logs'))
    )
    op.create_index(op.f('ix_training_logs_id'), 'training_logs', ['id'], unique=False)

    # Walks
    op.create_table('walks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('start_datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('mood', sa.Enum('CALM', 'NORMAL', 'STRESSED', name='walkmood'), nullable=True),
        sa.Column('distance_km', sa.Float(), nullable=True),
        sa.Column('notes_markdown', sa.Text(), nullable=True),
        sa.Column('video_urls_json', sa.JSON(), nullable=True),
        sa.Column('gpx_file_url', sa.String(), nullable=True),
        sa.Column('has_route_data', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_walks_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_walks'))
    )
    op.create_index(op.f('ix_walks_id'), 'walks', ['id'], unique=False)
    op.create_index(op.f('ix_walks_user_id'), 'walks', ['user_id'], unique=False)

    # Walk Dogs
    op.create_table('walk_dogs',
        sa.Column('walk_id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_walk_dogs_dog_id_dogs')),
        sa.ForeignKeyConstraint(['walk_id'], ['walks.id'], name=op.f('fk_walk_dogs_walk_id_walks')),
        sa.PrimaryKeyConstraint('walk_id', 'dog_id', name=op.f('pk_walk_dogs'))
    )

    # Equipment Items
    op.create_table('equipment_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dog_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('LEASH', 'HARNESS', 'COLLAR', 'TOY', 'BED', 'BOWL', 'OTHER', name='equipmenttype'), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('purchase_date', sa.Date(), nullable=True),
        sa.Column('brand', sa.String(), nullable=True),
        sa.Column('size', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], name=op.f('fk_equipment_items_dog_id_dogs')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_equipment_items'))
    )
    op.create_index(op.f('ix_equipment_items_id'), 'equipment_items', ['id'], unique=False)

    # Tags
    op.create_table('tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_tags_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_tags'))
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_user_id'), 'tags', ['user_id'], unique=False)

    # Tag Assignments
    op.create_table('tag_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name=op.f('fk_tag_assignments_tag_id_tags')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_tag_assignments'))
    )
    op.create_index(op.f('ix_tag_assignments_id'), 'tag_assignments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tag_assignments_id'), table_name='tag_assignments')
    op.drop_table('tag_assignments')
    op.drop_index(op.f('ix_tags_user_id'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_equipment_items_id'), table_name='equipment_items')
    op.drop_table('equipment_items')
    op.drop_table('walk_dogs')
    op.drop_index(op.f('ix_walks_user_id'), table_name='walks')
    op.drop_index(op.f('ix_walks_id'), table_name='walks')
    op.drop_table('walks')
    op.drop_index(op.f('ix_training_logs_id'), table_name='training_logs')
    op.drop_table('training_logs')
    op.drop_index(op.f('ix_behavior_issues_id'), table_name='behavior_issues')
    op.drop_table('behavior_issues')
    op.drop_index(op.f('ix_training_goals_id'), table_name='training_goals')
    op.drop_table('training_goals')
    op.drop_index(op.f('ix_care_task_logs_id'), table_name='care_task_logs')
    op.drop_table('care_task_logs')
    op.drop_index(op.f('ix_care_tasks_id'), table_name='care_tasks')
    op.drop_table('care_tasks')
    op.drop_index(op.f('ix_invoices_id'), table_name='invoices')
    op.drop_table('invoices')
    op.drop_index(op.f('ix_vaccinations_id'), table_name='vaccinations')
    op.drop_table('vaccinations')
    op.drop_index(op.f('ix_vet_visits_id'), table_name='vet_visits')
    op.drop_table('vet_visits')
    op.drop_index(op.f('ix_dog_profile_details_id'), table_name='dog_profile_details')
    op.drop_table('dog_profile_details')
    op.drop_index(op.f('ix_dogs_owner_user_id'), table_name='dogs')
    op.drop_index(op.f('ix_dogs_id'), table_name='dogs')
    op.drop_table('dogs')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

