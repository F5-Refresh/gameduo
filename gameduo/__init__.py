import json
import os

import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameduo.settings")

from django.core.cache import cache
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# 장고 서버가 켜질때 자동으로 실행하며 json데이터를 redis에 저장합니다.
data = json.loads(requests.get('https://dmpilf5svl7rv.cloudfront.net/assignment/backend/bossRaidData.json').content)
cache.set('limit_time', data['bossRaids'][0]['bossRaidLimitSeconds'], timeout=None)
for level_data in data['bossRaids'][0]['levels']:
    cache.set(f"level{level_data['level']}", level_data['score'], timeout=None)  # 캐싱

# 동시 유저입장을 위한 플래그
cache.set('can_enter', True, timeout=None)
