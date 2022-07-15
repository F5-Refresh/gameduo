from django.urls import path

from raid.views.raid_ranking import BossRaidRankingView
from raid.views.raid_status_search import RaidStatusSearchView
from raid.views.raid_view import RaidView

urlpatterns = [
    path('/status-search', RaidStatusSearchView.as_view()),
    path('/ranking', BossRaidRankingView.as_view()),
    path('/start_raid', RaidView.start_raid),
    path('/end_raid', RaidView.end_raid),
]
