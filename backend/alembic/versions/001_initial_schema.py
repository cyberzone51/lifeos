"""Initial schema - all tables

Revision ID: 001
Revises: 
Create Date: 2026-07-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('telegram_id', sa.BigInteger, unique=True, nullable=True),
        sa.Column('username', sa.String(100)),
        sa.Column('email', sa.String(255), unique=True),
        sa.Column('phone', sa.String(20)),
        sa.Column('is_premium', sa.Boolean, default=False),
        sa.Column('premium_expires_at', sa.DateTime),
        sa.Column('language_code', sa.String(10), default='en'),
        sa.Column('currency_code', sa.String(3), default='USD'),
        sa.Column('timezone', sa.String(50), default='UTC'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Profiles
    op.create_table(
        'profiles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('full_name', sa.String(200)),
        sa.Column('avatar_url', sa.Text),
        sa.Column('birth_date', sa.Date),
        sa.Column('gender', sa.String(20)),
        sa.Column('bio', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Expense Categories
    op.create_table(
        'expense_categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('color', sa.String(7)),
        sa.Column('is_system', sa.Boolean, default=False),
    )

    # Expenses
    op.create_table(
        'expenses',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('expense_categories.id')),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency_code', sa.String(3), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('receipt_url', sa.Text),
        sa.Column('tags', ARRAY(sa.String)),
        sa.Column('expense_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_expenses_user_date', 'expenses', ['user_id', sa.text('expense_date DESC')])

    # Income Categories
    op.create_table(
        'income_categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('color', sa.String(7)),
        sa.Column('is_system', sa.Boolean, default=False),
    )

    # Incomes
    op.create_table(
        'incomes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('income_categories.id')),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency_code', sa.String(3), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('tags', ARRAY(sa.String)),
        sa.Column('income_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Budgets
    op.create_table(
        'budgets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('expense_categories.id')),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('period', sa.String(20), nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Tasks
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('priority', sa.Integer, default=2),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('due_date', sa.DateTime),
        sa.Column('reminder_at', sa.DateTime),
        sa.Column('tags', ARRAY(sa.String)),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'])
    op.create_index('idx_tasks_user_due', 'tasks', ['user_id', 'due_date'])

    # Habits
    op.create_table(
        'habits',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('icon', sa.String(50)),
        sa.Column('color', sa.String(7)),
        sa.Column('frequency', sa.String(20), default='daily'),
        sa.Column('target_count', sa.Integer, default=1),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_habits_user', 'habits', ['user_id'])

    # Habit Logs
    op.create_table(
        'habit_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('habit_id', UUID(as_uuid=True), sa.ForeignKey('habits.id', ondelete='CASCADE')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('completed_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('value', sa.Numeric(10, 2)),
        sa.Column('notes', sa.Text),
    )
    op.create_index('idx_habit_logs_habit_date', 'habit_logs', ['habit_id', sa.text('completed_at DESC')])

    # Weight Logs
    op.create_table(
        'weight_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('weight', sa.Numeric(5, 2), nullable=False),
        sa.Column('unit', sa.String(5), default='kg'),
        sa.Column('logged_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Sleep Logs
    op.create_table(
        'sleep_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('bedtime', sa.DateTime, nullable=False),
        sa.Column('wake_time', sa.DateTime, nullable=False),
        sa.Column('quality', sa.Integer),
        sa.Column('notes', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Mood Logs
    op.create_table(
        'mood_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('mood', sa.Integer, nullable=False),
        sa.Column('notes', sa.Text),
        sa.Column('logged_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Journal Entries
    op.create_table(
        'journal_entries',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500)),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('mood', sa.Integer),
        sa.Column('tags', ARRAY(sa.String)),
        sa.Column('entry_date', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_journal_user_date', 'journal_entries', ['user_id', sa.text('entry_date DESC')])

    # Knowledge Items
    op.create_table(
        'knowledge_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('item_type', sa.String(20), nullable=False),
        sa.Column('title', sa.String(500)),
        sa.Column('content', sa.Text),
        sa.Column('file_url', sa.Text),
        sa.Column('tags', ARRAY(sa.String)),
        sa.Column('summary', sa.Text),
        sa.Column('metadata', JSONB),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_knowledge_user_type', 'knowledge_items', ['user_id', 'item_type'])

    # AI Conversations
    op.create_table(
        'ai_conversations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(500)),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # AI Messages
    op.create_table(
        'ai_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', UUID(as_uuid=True), sa.ForeignKey('ai_conversations.id', ondelete='CASCADE')),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('agent_type', sa.String(50)),
        sa.Column('tokens_used', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_ai_messages_conv', 'ai_messages', ['conversation_id', 'created_at'])

    # AI Memory
    op.create_table(
        'ai_memory',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('key', sa.String(200), nullable=False),
        sa.Column('value', sa.Text, nullable=False),
        sa.Column('confidence', sa.Numeric(3, 2), default=1.0),
        sa.Column('source', sa.String(50)),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_ai_memory_user', 'ai_memory', ['user_id', 'category'])

    # Notifications
    op.create_table(
        'notifications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('is_read', sa.Boolean, default=False),
        sa.Column('data', JSONB),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )

    # Payments
    op.create_table(
        'payments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('payment_type', sa.String(50), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency_code', sa.String(3), nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('telegram_payment_id', sa.String(200)),
        sa.Column('metadata', JSONB),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )


def downgrade() -> None:
    op.drop_table('payments')
    op.drop_table('notifications')
    op.drop_table('ai_memory')
    op.drop_table('ai_messages')
    op.drop_table('ai_conversations')
    op.drop_table('knowledge_items')
    op.drop_table('journal_entries')
    op.drop_table('mood_logs')
    op.drop_table('sleep_logs')
    op.drop_table('weight_logs')
    op.drop_table('habit_logs')
    op.drop_table('habits')
    op.drop_table('tasks')
    op.drop_table('budgets')
    op.drop_table('incomes')
    op.drop_table('income_categories')
    op.drop_table('expenses')
    op.drop_table('expense_categories')
    op.drop_table('profiles')
    op.drop_table('users')
