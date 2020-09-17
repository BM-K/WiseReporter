# WiseReporter
WiseReporter Data Preprocessing Doc

## Strong Tag Preprocessing
신문사에서 summary처럼 보이는 tag가 존재

### Problems
<br>
*Special Symbol 문제* <br>
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
<br><br>
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
### Num Data After Preprocessing
|Tag|Befor|After|
|------|------|------|
|Strong|38,707|13,687|
