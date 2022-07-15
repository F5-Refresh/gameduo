# gameduo
게임듀오 기업과제입니다. 유저는 보스레이드 게임(PvE)을 플레이하고, 랭킹을 조회할 수 있습니다. 
<br>


## 📚 Skills
<br>

 - Language

    ![python](https://img.shields.io/badge/python-3.9-3670A0?logo=python&logoColor=white)

 - FrameWork

    ![Django](https://img.shields.io/badge/django-3.2.13-%23092E20?&logo=Django&logoColor=white)
    ![DjangoRest](https://img.shields.io/badge/DJANGOREST-3.13.1-ff1709?logo=django&logoColor=white&color=ff1709&labelColor=gray)
    
 - DataBase 

    ![MySQL](https://img.shields.io/badge/mysql-8.0-4479A1.svg?logo=mysql&logoColor=white)
    ![Redis](https://img.shields.io/badge/redis-DC382D.svg?logo=redis&logoColor=white)

 - Deploy 

    ![AWS](https://img.shields.io/badge/AWSE2-%23FF9900.svg?logo=amazon-aws&logoColor=white)
    ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
    ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?logo=nginx&logoColor=white)
    ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?logo=gunicorn&logoColor=white)

 - ETC

    ![GitHub](https://img.shields.io/badge/github-%23121011.svg?logo=github&logoColor=white)
    ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?logo=swagger&logoColor=white)
    ![Git](https://img.shields.io/badge/-git-F05032?logo=git&logoColor=white)
    
    <br>

## ✅ 프로젝트 소개
<br>

- 레이드가 가능한 게임에 대한 프로젝트입니다.
- 레이드를 진행하며 점수를 얻을 수 있고 랭킹 시스템이 존재합니다.
- 유저를 검색하고 현재 레이드 진행 상황에 대한 기록도 확인할 수 있습니다.
- 레이드는 한 유저만 들어갈 수 있으며 제한 시간이 끝나버리면 자동으로 레이드 실패가 됩니다.
- 레이드 실패 시에는 점수를 얻을 수 없습니다.

<br>

## 📌 요구 사항

<br>

- 유저 생성
- 유저 조회
- 보스레이드 상태 조회
- 보스레이드 시작
- 보스레이드 종료
- 랭킹 조회

<br>

## 🔑 기능구현

**1. 유저생성**

- 유저를 생성합니다.

**2. 유저로그인 / 로그아웃**
- JWT 인증방식을 사용하여 로그인/로그아웃을 합니다.

**3. 유저 조회**
- 전체 유저는 페이지네이션으로 조회 가능합니다.
- 개별 유저를 아이디로 조회할 수 있습니다.


**4. 레이드 상태 조회**
- 현재 레이드가 진행 여부와 진행하고 있는 유저id를 반환합니다.

**5. 레이드 시작**
- 다른 유저가 레이드가 진행 중일 시 레이드 진행이 불가합니다.
- 아무도 레이드를 진행하고 있지 않다면 레이드를 진행합니다.
- 레이드를 진행 중일시 레이드 이력이 만들어지고 다른 유저는 입장을 할 수 없게 됩니다.
- 제한 시간을 초과하면 자동으로 실패되며 다른 유저가 입장이 가능해집니다.
- 성공/실패를 이미 한 상태라면 스케쥴러는 아무 작업도 하지 않습니다.

**6. 레이드 종료**
- 클라이언트가 레이드 성공/실패를 서버에게 알려주고 레이드 성공 시 점수를 부여합니다.
- 레이드가 종료되므로 다른 유저 입장이 가능해집니다.

**7. 랭킹 조회**
- 모든 유저의 레이드 점수 총점을 기반으로 TOP10 정보를 조회합니다.
- 로그인한 유저의 개인 순위를 조회합니다.
- TOP10 순위는 5분마다 업데이트됩니다.
- TOP10 순위는 1 ~ 10위가 아닌 0~9위 순으로 반환합니다.

<br>

## 📁API Doc
<br>

|Action| Method| URL|
|-----|----|----|
|회원가입| POST| users/signup
|로그인| POST| users/login/
|로그아웃| POST| users/logout/
|유저 조회| GET| users/search/<str: account>
|레이드 상태 조회| GET| raid/status-search
|레이드 시작| POST| raid/start_raid
|레이드 종료| POST| raid/end_raid
|랭킹 조회| GET| raid/ranking

<br>

## 💾ERD
<br>

![image](https://user-images.githubusercontent.com/87809367/178980685-e8ec1f4e-728c-4550-8e1b-acb34827fa08.png)

<br>

## 👋 Team & Task
<br>

|Name|Task|
|-----|----
|김동규| 유저 & 레이드 상태 조회, 프로젝트 배포
|남효정| JWT 로그인 & 로그아웃 구현
|이동연| 레이드 시작 & 종료 구현, 랭킹 조회
|전기원| 회원가입 구현
|조병민| 레이드 시작 & 종료 구현, 랭킹 조회
