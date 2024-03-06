# HibiscusSyriacusExplorer  [![Static Code Analyze](https://github.com/changminsuk/HibiscusSyriacusExplorer/actions/workflows/static_code_analyze.yml/badge.svg)](https://github.com/changminsuk/HibiscusSyriacusExplorer/actions/workflows/static_code_analyze.yml)
 🌺 무궁화 수종 분류 GPT 용 backend
 
 https://chat.openai.com/g/g-d8xjVnu15-hibiscus-syriacus-explorer

## Structure

* __src__ -- _소스파일의 최상위 디렉토리_
    * __src/app.py__ -- _각 서비스들을 최초 실행하는 main 함수_
    * __decorators__ -- _데코레이터 함수들을 모아둔 폴더_
    * __database__ -- _redis, mongo 에 접속할 수 있는 클래스_
    * __dtos__ -- _입력/출력을 위한 데이터 클래스_
    * __models__ -- _데이터베이스에 접근하기 위한 데이터 모델들_
    * __repository__ -- _데이터베이스 접근을 위한 wrapper 함수들의 모음_
    * __controllers__ -- _api 엔드포인트를 정의해둔 폴더_
    * __services__ -- _비즈니스 로직을 처리하는 클래스_
    * __tests__ -- _ 유닛테스트들을 모아둔 폴더_

## how to setup

1. pipenv 설치
```sh
brew install pipenv
```
```sh
pip install pipenv
```
2. python 3.10 버전으로 가상환경 생성
```sh
pipenv --python 3.10
```
3. 가상환경 진입
```sh
pipenv shell
```
4. 필요한 패키지 설치
```sh
pipenv sync
```
5. 서버 실행
```sh
pipenv run start
```
<br>
<br>

- pipenv 환경에서의 패키지 설치
```sh
pipenv install [패키지명]
```

- pipenv 배포 전 패키지 업데이트
```sh
pipenv update
```

