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
|idx|Company Id|Company Name|Num|
|----|:----:|:----:|:----:|
|1|12|www.newsis.com|319717|
|2|32|www.fnnews.com|174692|
|3|11|news1.kr|154562|
|4|28|view.asiae.co.kr|135664|
|5|29|www.edaily.co.kr|135632|
|6|33|www.hankyung.com|128691|
|7|35|www.nocutnews.co.kr|108112|
|8|34|news.heraldcorp.com|69448|
|9|6|www.segye.com|64863|
|10|27|www.sedaily.com|61471|
|11|16|news.wowtv.co.kr|59239|
|12|37|moneys.mt.co.kr|55498|
|13|2|news.kmib.co.kr|52470|
|14|10|www.hankookilbo.com|50066|
|15|26|news.mt.co.kr|46836|
|16|13|yna.kr|46614|
|17|40|www.pressian.com|37591|
|18|25|news.mk.co.kr|36592|
|19|5|www.seoul.co.kr|34995|
|20|3|www.donga.com|32749|
|21|44|www.inews24.com|29438|
|22|45|www.etnews.com|28360|
|23|42|www.dt.co.kr|27795|
|24|4|www.munhwa.com|26108|
|25|7|biz.chosun.com|25802|
|26|66|www.busan.com|25020|
|27|9|www.hani.co.kr|24042|
|28|20|www.mbn.co.kr|23112|
|29|36|www.dailian.co.kr|22437|
|30|65|news.imaeil.com|21721|
|31|39|www.ohmynews.com|20559|
|32|8|news.joins.com|20020|
|~~33~~|~~88~~|~~www.sportsseoul.com~~|~~19469~~|
|34|64|www.kwnews.co.kr|19128|
|~~35~~|~~90~~|~~sports.chosun.com~~|~~14314~~|
|36|21|cnbc.sbs.co.kr|12729|
|37|1|news.khan.co.kr|12702|
|38|124|news.tf.co.kr|11680|
|39|23|news.tvchosun.com|9007|
|40|24|www.ytn.co.kr|7742|
|41|30|biz.chosun.com|6750|
|42|117|news.sbs.co.kr|5200|
|43|31|www.joseilbo.com|4760|
|44|17|news.jtbc.joins.com|4701|
|45|108|news.kbs.co.kr|4512|
|46|54|www.sisajournal.com|4185|
|47|69|www.womennews.co.kr|3757|
|48|38|www.mediatoday.co.kr|3187|
|~~49~~|~~87~~|~~sports.khan.co.kr~~|~~3180~~|
|~~50~~|~~92~~|~~www.xportsnews.com~~|~~3149~~|
|51|63|magazine.hankyung.com|1983|
|52|93|isplus.live.joins.com|1942|
|53|113|imnews.imbc.com|1239|
|54|61|news.joins.com|1227|
|55|15|www.ichannela.com|977|
|56|67|www.journalist.or.kr|851|
|57|62|h21.hani.co.kr|829|
|58|53|www.sisain.co.kr|673|
|59|59|weekly.donga.com|522|
|60|55|shindonga.donga.com|454|
|61|52|news.mk.co.kr|437|
|62|71|www.newscham.ney|361|
|63|98|enews.imbc.com|354|
|64|46|www.zdnet.co.kr|335|
|65|60|weekly.chosun.com|315|
|66|119|newstapa.org|262|
|67|70|www.ildaro.com|259|
|68|58|weekly.khan.co.kr|206|
|69|125|news.chosun.com|162|
|70|56|san.chosun.com|80|
|71|78|www.osen.co.kr|64|
|72|73|kormedi.com|52|
|73|91|www.cine21.com|21|
|74|84|www.mydaily.co.kr|12|
|~~75~~|~~86~~|~~sports.khan.co.kr~~|~~9~~|
|~~76~~|~~100~~|~~sports.mk.co.kr~~|~~2~~|
|77|118|www.newsen.com|1|
|78|121|www.spotvnews.co.kr|1|
