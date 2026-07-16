"""Add extended modules - goals, calendar, family, assets, shopping, mental, gamification

Revision ID: 002
Revises: 001
Create Date: 2026-07-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Goals
    op.create_table(
        'goals',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('target_value', sa.Numeric(15, 2)),
        sa.Column('current_value', sa.Numeric(15, 2), server_default='0'),
        sa.Column('unit', sa.String(20)),
        sa.Column('deadline', sa.DateTime),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('priority', sa.Integer, server_default='2'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Goal Milestones
    op.create_table(
        'goal_milestones',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('goal_id', UUID(as_uuid=True), sa.ForeignKey('goals.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('target_value', sa.Numeric(15, 2)),
        sa.Column('is_completed', sa.Boolean, server_default='false'),
        sa.Column('completed_at', sa.DateTime),
        sa.Column('order', sa.Integer, server_default='0'),
    )

    # Calendar Events
    op.create_table(
        'calendar_events',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('location', sa.String(500)),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime),
        sa.Column('all_day', sa.Boolean, server_default='false'),
        sa.Column('recurrence', sa.String(20)),
        sa.Column('color', sa.String(7)),
        sa.Column('reminder_minutes', sa.Integer, server_default='15'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Families
    op.create_table(
        'families',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('invite_code', sa.String(10), unique=True, nullable=False),
        sa.Column('created_by', UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Family Members
    op.create_table(
        'family_members',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('family_id', UUID(as_uuid=True), sa.ForeignKey('families.id', ondelete='CASCADE')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('role', sa.String(20), server_default='member'),
        sa.Column('joined_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Shared Tasks
    op.create_table(
        'shared_tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('family_id', UUID(as_uuid=True), sa.ForeignKey('families.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('assigned_to', UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_by', UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('is_completed', sa.Boolean, server_default='false'),
        sa.Column('due_date', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Shared Budgets
    op.create_table(
        'shared_budgets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('family_id', UUID(as_uuid=True), sa.ForeignKey('families.id', ondelete='CASCADE')),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('amount', sa.Float, server_default='0'),
        sa.Column('spent', sa.Float, server_default='0'),
        sa.Column('period', sa.String(20), server_default='monthly'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Assets
    op.create_table(
        'assets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('purchase_date', sa.DateTime),
        sa.Column('purchase_price', sa.Numeric(12, 2)),
        sa.Column('current_value', sa.Numeric(12, 2)),
        sa.Column('currency_code', sa.String(3), server_default='USD'),
        sa.Column('serial_number', sa.String(100)),
        sa.Column('notes', sa.Text),
        sa.Column('photo_url', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Asset Reminders
    op.create_table(
        'asset_reminders',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('asset_id', UUID(as_uuid=True), sa.ForeignKey('assets.id', ondelete='CASCADE')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('reminder_type', sa.String(50), nullable=False),
        sa.Column('next_date', sa.DateTime, nullable=False),
        sa.Column('repeat_days', sa.Integer, server_default='365'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Shopping Lists
    op.create_table(
        'shopping_lists',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('budget', sa.Numeric(10, 2)),
        sa.Column('currency_code', sa.String(3), server_default='USD'),
        sa.Column('is_completed', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Shopping Items
    op.create_table(
        'shopping_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('list_id', UUID(as_uuid=True), sa.ForeignKey('shopping_lists.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('quantity', sa.Integer, server_default='1'),
        sa.Column('estimated_price', sa.Numeric(10, 2)),
        sa.Column('actual_price', sa.Numeric(10, 2)),
        sa.Column('is_purchased', sa.Boolean, server_default='false'),
        sa.Column('category', sa.String(50)),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Stress Logs
    op.create_table(
        'stress_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('source', sa.String(100)),
        sa.Column('notes', sa.Text),
        sa.Column('logged_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Meditation Logs
    op.create_table(
        'meditation_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('duration_minutes', sa.Integer, nullable=False),
        sa.Column('technique', sa.String(50)),
        sa.Column('notes', sa.Text),
        sa.Column('logged_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Gratitude Entries
    op.create_table(
        'gratitude_entries',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('entry_date', sa.DateTime, nullable=False),
        sa.Column('item1', sa.String(200), nullable=False),
        sa.Column('item2', sa.String(200), nullable=False),
        sa.Column('item3', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # User Progress (Gamification)
    op.create_table(
        'user_progress',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True),
        sa.Column('level', sa.Integer, server_default='1'),
        sa.Column('xp', sa.Integer, server_default='0'),
        sa.Column('total_xp', sa.Integer, server_default='0'),
        sa.Column('streak_days', sa.Integer, server_default='0'),
        sa.Column('longest_streak', sa.Integer, server_default='0'),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Achievements
    op.create_table(
        'achievements',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500)),
        sa.Column('icon', sa.String(50)),
        sa.Column('xp_reward', sa.Integer, server_default='100'),
        sa.Column('requirement_type', sa.String(50), nullable=False),
        sa.Column('requirement_value', sa.Integer, nullable=False),
    )

    # User Achievements
    op.create_table(
        'user_achievements',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('achievement_id', UUID(as_uuid=True), sa.ForeignKey('achievements.id')),
        sa.Column('unlocked_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Daily Challenges
    op.create_table(
        'daily_challenges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('challenge_date', sa.DateTime, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('xp_reward', sa.Integer, server_default='50'),
        sa.Column('is_completed', sa.Boolean, server_default='false'),
        sa.Column('completed_at', sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('daily_challenges')
    op.drop_table('user_achievements')
    op.drop_table('achievements')
    op.drop_table('user_progress')
    op.drop_table('gratitude_entries')
    op.drop_table('meditation_logs')
    op.drop_table('stress_logs')
    op.drop_table('shopping_items')
    op.drop_table('shopping_lists')
    op.drop_table('asset_reminders')
    op.drop_table('assets')
    op.drop_table('shared_budgets')
    op.drop_table('shared_tasks')
    op.drop_table('family_members')
    op.drop_table('families')
    op.drop_table('calendar_events')
    op.drop_table('goal_milestones')
    op.drop_table('goals')
