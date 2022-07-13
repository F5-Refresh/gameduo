import json

import requests
from django.core.cache import cache

# 장고 서버가 켜질때 자동으로 실행하며 json데이터를 redis에 저장합니다.
data = json.loads(requests.get('https://dmpilf5svl7rv.cloudfront.net/assignment/backend/bossRaidData.json').content)
cache.set('limit_time', data['bossRaids'][0]['bossRaidLimitSeconds'])
for level_data in data['bossRaids'][0]['levels']:
    cache.set(f"level{level_data['level']}", level_data['score'])  # 캐싱
cache.set('is_use', False)

print(cache.get('level0'))
print(cache.get('level1'))
print(cache.get('level2'))
