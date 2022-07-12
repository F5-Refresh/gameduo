from django.urls import path

from .views import raid_ranking

urlpatterns = [
    path('/boss-raid/ranking', raid_ranking.BossRaidRankingView.as_view()),
]
