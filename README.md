# WiseReporter
WiseReporter Data Preprocessing Doc

## Comple Tag Preprocessing
신문사에서 summary tag가 존재

### Problems

*Advertising 문제* <br>
- Example source

```
핀테크 회사들이 은행과 제휴를 맺고 적금 ~~
연 1.0%의 캐시백을 증정할 계획이다.
▶네이버 채널에서 '아이뉴스24'를 구독해주세요.
▶아이뉴스TV에서 부동산 고수를 만나보세요.
----------
```
- Solution : source에 '▶' 기호가 2개 있을시 그 이하 삭제
```python
# 광고인가??!
def remove_ad(data):
    count_ad = data.count('▶')

    if count_ad == 2:
        start_ad = data.find('▶')
        return data[:start_ad]
    else:
        return data
```


## Strong Tag Preprocessing
신문사에서 summary처럼 보이는 tag가 존재

### Problems

*Special Symbol 문제* 
- Example targets

```
● 계륵이던 자소서, 취업전선 총아로
● 컨설팅, 작성 대행 등 ‘장삿거리’ 돼
● ‘자소서 포비아’ 낱말까지 횡행
● “기업, 자소서 리터러시 갖췄는지 의문
-------------------------------------------------
세부 실천과제는 ▲정책 연구기능 강화 ▲연구
-------------------------------------------------
```

- Solution : target에 눈으로 확인된 심볼 제거

```python
# 특수기호 제거!
def remove_special_symbol(summ_data):
    symbol = ['■', '▲', '●', '◆', '◇', 'ㆍ']

    for step, sym in enumerate(symbol):
        summ_data = summ_data.replace(sym, '')

    return summ_data
```

*Advertising 문제* <br>
- Example targets
```
"▶ 헉! 소리나는 스!토리 뉴스 [헉스]
▶ 클릭해, 뉴스 들어간다 [뉴스쿨]
▶ 세상에 이런일이 [fn파스]"
```
- Solution : target에 '▶' 있을 시 전체 데이터 제거
```python
# target이 광고인가??!
def IsAd(summ_data):
    ad_idx = summ_data.find('▶')
    
    return False if ad_idx == -1 else True
```

'▶' 이게 있다고 광고라고요?? 아닌 데이터도 있을 거 같은데??

```
▶ [인터랙티브] 젊은정치 실종, 아프니까 청년정치다?
-------------------------------------------------
▶ 동아일보 단독 뉴스 / 트렌드 뉴스
-------------------------------------------------
▶ 네이버 홈에서 [동아일보] 채널 구독하기
-------------------------------------------------
▶ 네이버 모바일에서 [전자신문] 채널 구독하기
-------------------------------------------------
```
뽑아보니 다 광고였던 것이였따..;; <br> <br>

*의미 없는 Target 문제* <br>
- Example targets
```
■ 취재파일
-------------------------------------------------
●일시:
-------------------------------------------------
〈큰 사진〉
-------------------------------------------------
```
- Solution : special symbol 제거 후 N 이하 target 제거
```python
# N개 토큰 이하일 경우 제거~
def remove_under_N_tokens(summ_data, N=3):
    summ_list = summ_data.split(' ')

    return False if len(summ_list) <= N else True
```
### Num of Data after Preprocessing
|Tag|Befor|After|
|------|------|------|
|Comple|43,456|39,289|
|Strong|38,707|13,687|

## Company Id, 갯수
|idx|Company Id|Num|
|----|----|----|
|1|12|319717|
|2|32|174692|
|3|11|154562|
|4|28|135664|
|5|29|135632|
|6|33|128691|
|7|35|108112|
|8|34|69448|
|9|6|64863|
|10|27|61471|
|11|||
|12|||
|13|||
|14|||
|15|||
|16|||
|17|||
|18|||
|19|||
|20|||
|21|||
|22|||
|23|||
|24|||
|25|||
|26|||
|27|||
|28|||
|29|||
|30|||
|31|||
|32|||
|33|||
|34|||
|35|||
|36|||
|37|||
|38|||
|39|||
|40|||
|41|||
|42|||
|43|||
|44|||
|45|||
|46|||
|47|||
|48|||
|49|||
|50|||
|51|||
|52|||
|53|||
|54|||
|55|||
|56|||
|57|||
|58|||
|59|||
|60|||
|61|||
|62|||
|63|||
|64|||
|65|||
|66|||
|67|||
|68|||
|69|||
|70|||
|71|||
