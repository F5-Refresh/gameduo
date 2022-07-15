from django.urls import path

from raid.views.boss_raid_view import BossRaidView
from raid.views.raid_ranking import BossRaidRankingView
from raid.views.raid_status_search import RaidStatusSearchView

urlpatterns = [
    path('/status-search', RaidStatusSearchView.as_view()),
    path('/ranking', BossRaidRankingView.as_view()),
    path('/start_raid', BossRaidView.start_boss_raid),
    path('/end_raid', BossRaidView.end_boss_raid),
]
