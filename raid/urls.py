from django.urls import path

from raid.views.boss_raid_view import BossRaidView
from raid.views.raid_status_search import RaidStatusSearchView

from .views import raid_ranking

urlpatterns = [
    path('/ranking', raid_ranking.BossRaidRankingView.as_view()),
    path('/status-search', RaidStatusSearchView.as_view()),
    path('start_raid', BossRaidView.start_boss_raid),
    path('end_raid', BossRaidView.end_boss_raid),
]
