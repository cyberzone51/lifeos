"""Models package — экспорт всех моделей."""

from app.models.user import User
from app.models.profile import Profile
from app.models.finance import Expense, Income, Budget, ExpenseCategory, IncomeCategory
from app.models.tasks import Task
from app.models.habits import Habit, HabitLog
from app.models.health import WeightLog, SleepLog, MoodLog
from app.models.journal import JournalEntry
from app.models.knowledge import KnowledgeItem
from app.models.ai import AIConversation, AIMessage, AIMemory
from app.models.goals import Goal, GoalMilestone
from app.models.calendar import CalendarEvent
from app.models.family import Family, FamilyMember, SharedTask, SharedBudget
from app.models.assets import Asset, AssetReminder
from app.models.shopping import ShoppingList, ShoppingItem
from app.models.mental import StressLog, MeditationLog, GratitudeEntry
from app.models.gamification import UserProgress, Achievement, UserAchievement, DailyChallenge

__all__ = [
    # User
    "User", "Profile",
    # Finance
    "Expense", "Income", "Budget", "ExpenseCategory", "IncomeCategory",
    # Tasks
    "Task",
    # Habits
    "Habit", "HabitLog",
    # Health
    "WeightLog", "SleepLog", "MoodLog",
    # Journal
    "JournalEntry",
    # Knowledge
    "KnowledgeItem",
    # AI
    "AIConversation", "AIMessage", "AIMemory",
    # Goals
    "Goal", "GoalMilestone",
    # Calendar
    "CalendarEvent",
    # Family
    "Family", "FamilyMember", "SharedTask", "SharedBudget",
    # Assets
    "Asset", "AssetReminder",
    # Shopping
    "ShoppingList", "ShoppingItem",
    # Mental Wellness
    "StressLog", "MeditationLog", "GratitudeEntry",
    # Gamification
    "UserProgress", "Achievement", "UserAchievement", "DailyChallenge",
]
