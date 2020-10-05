# Wise Reporter Preprocessing
Wise Reporter Data Preprocessing Doc

## Company Id, Name, Num
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
|~~36~~|~~21~~|~~cnbc.sbs.co.kr~~|~~12729~~|
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
|~~55~~|~~15~~|~~www.ichannela.com~~|~~977~~|
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
|~~73~~|~~91~~|~~www.cine21.com~~|~~21~~|
|~~74~~|~~84~~|~~www.mydaily.co.kr~~|~~12~~|
|~~75~~|~~86~~|~~sports.khan.co.kr~~|~~9~~|
|~~76~~|~~100~~|~~sports.mk.co.kr~~|~~2~~|
|~~77~~|~~118~~|~~www.newsen.com~~|~~1~~|
|~~78~~|~~121~~|~~www.spotvnews.co.kr~~|~~1~~|

# Preprocessing
공통 + 개별 요소로 전처리하였습니다. <br>
'무난'은 공통으로만 처리한 기사입니다.

## 삭제 기사
```
www.sportsseoul.com
sports.chosun.com
sports.khan.co.kr
www.xportsnews.com
-> sport 기사는 target에 광고 밖에 없음

www.ichannela.com
-> target이 summary가 아님

cnbc.sbs.co.kr
-> 동영상 뉴스

50개 미만 데이터 
```

## 공통
```
target이 source에도 나오는 경우 제거
광고, 기자 제거
```
## Newsis
```
cid = 12
맨 윗줄에 '【서울=뉴시스】 = ' 제거 
```
## Fnnews
```
cid = 32
무난
```
## News1
```
cid = 11
맨 윗줄에 '(서울=뉴스1) 문대현 기자 = ' 제거
```
## Asiae
```
cid = 28
무난
```
## Edaily
```
cid = 29
source에 (1245) 이런 숫자 제거
```
## HanKyung
```
cid = 33
source, tgt 겹침 추가 제거
```
## Nocutnews
```
cid = 35
무난
```

## Heraldcorp
```
cid = 34
무난
```
## Segye
```
cid = 6
source에 'ⓒ 세상을 보는 눈, 세계일보' 제거
target에 '세계일보' 제거
source에 '기자' 추가 제거
```

## Sedaily
```
cid = 27
source에 '[서울경제]' 제거
```
## Wowty
```
cid = 16
target에 '▶ 네이버 홈에서 [한국경제TV] 채널 구독하기 [생방송보기]' 광고 추가 제거
target에 '※' or '<사진' 로 시작되는 필요없는 target 제거
```

## Moneys
```
cid = 37
source에 '☞' 로 시작하는 광고 추가 제거
target에 '▶ 고수들의' or '☞' 로 시작되는 광고 추가 제거
```

## Kmib
```
cid = 2
무난
```
## Hankookilbo
```
cid = 10
source에 '▶'로 시작하는 광고 추가 제거
```
## Mt
```
cid = 26
source에 '▶' 로 시작하는 광고 추가 제거
target에 '변호사' 로 시작되는 의미없는 target 제거
```
## Yna
```
cid = 13
source에 '(서울=연합뉴스) 정빛나 기자 = ' 부분 제거
target에 '기사제공' 제거
```
## Pressian
```
cid = 40
무난
```

## Mk
```
cid = 25
무난
```

## Seoul
```
cid = 5
무난
```

## Donga
```
cid = 3
무난
```

## Inews24
```
cid = 44
source에 '[아이뉴스24 ] ' 제거
```

## Etnews
```
cid = 45
source에 '※'로 시작하는 글 제거
target에 '▶ 네이버 모바일에서 [전자신문] 채널 구독하기' 광고 제거
target에 '▶ 인공지능(' 글 제거
target에 '◆ Report' 글 제거
```

## Dt
```
cid = 42
source에 '네이버 채널에서' 광고 추가 제거
target에 '고견을 듣는다' 제거
```

## Munhwa
```
cid = 4
target에 '[ 문화닷컴 바로가기 | 문화일보가 직접 편집한 뉴스 채널 | 모바일 웹 ]' 광고 추가 제거
```

## BizChosun
```
cid = 7
무난
```

## Busan
```
cid = 66
무난
```
## Hani
```
cid = 9
source에 '<한겨레21>이 후원제를 시작합니다.' 광고 추가 제거
```

## Mbn
```
cid = 20
source에 '동영상 뉴스' 제거
target에 '▶네이버' 광고 추가 제거
```

## Dailian
```
cid = 36
source에 '(주)데일리안 - 무단전재, 변형, 무단배포 금지' 제거
```

## Imaeil
```
cid = 65
무난
```

## Ohmynews
```
cid = 39
summary에 '덧붙이는 글' 제거
target에 '▶오마이뉴스에서는' 광고 제거
target에 '▲ [오마이포토]' 광고 제거
target에 '덧붙이는 글' 제거
```

## NewsJoins
```
cid = 8
source에 '▶ 네이버 메인에서 중앙일보를 받아보세요' 광고 추가 제거
```

## Kwnews
```
cid = 64
source에 '【철원】 [양구] ' 지역명 나오는 것 제거
```

## Khan
```
cid = 1
source에 '▶ 네이버 메인에서 경향신문 받아보기' 광고 추가 제거
```

## Tf
```
cid = 124
무난
```

## Tvchosun
```
cid = 23
target에 '☞ 네이버 메인에서 TV조선 구독하기' 광고 추가 제거
source, tgt 겹침 추가 제거
```

## Ytn
```
cid = 24
source에 'YTN 제공' 제거
target에 '▶ 대한민국 24시간 뉴스 채널 YTN 생방송보기 반복' 광고 제거
```

## BizChosun
```
cid = 30
무난
```

## Sbs
```
cid = 117
source에 '※', '▶' 로 시작하는 광고 제거
target에 '[SBS스페셜]' 제거
target에 '*' 로 시작하는 의미 없는 target 제거
```

## Joseilbo
```
cid = 31
무난
```

## Jtbc
```
cid = 17
무난
```

## Kbs
```
cid = 108
source에 '※', '*' 로 시작하는 의미 없는 글 제거
```

## Sisajournal
```
cid = 54
target에 '☞ 네이버에서 시사저널 뉴스를 받아 보세요' 광고 제거
```

## Womennews
```
cid = 69
source에 '▶ 네이버에서 여성신문 채널을 구독하세요.' 광고 추가 제거
target에 '[여신 후원자 되기]' 광고 제거
```

## Mediatoday
```
cid = 38
무난
```

## MagazineHankyung
```
cid = 63
무난
```

## Isplus
```
cid = 93
무난
```

## Imbc
```
cid = 113
source에 '동영상 뉴스' 제거
source에 'MBC뉴스', 'Copyright' 
```

## NewsJoins
```
cid = 61
source에 '▶ 네이버 메인에서 중앙일보를 받아보세요' 광고 추가 제거
```

## Journalist
```
cid = 67
무난
```

## H21Hani
```
cid = 62
source에 '<한겨레21>이 후원제를 시작합니다.' 광고 추가 제거
```

## Sisain
```
cid = 53
무난
```

## WeeklyDonga
```
cid = 59
무난
```

## Shindonga
```
cid = 55
무난
```

## Mk
```
cid = 52
무난
```

## Newscham
```
cid = 71
source에 '이 기사는 정보공유라이선스 2.0 : 영리금지'를 따릅니다.' 제거
```

## EnewsImbc
```
cid = 98
무난
```

## Zdnet
```
cid = 46
target에 '/▶ 지디넷코리아 '홈페이지'' 제거
```

## WeeklyChosun
```
cid = 60
무난
```

## Newstapa
```
cid = 119
무난
```

## Ildaro
```
cid = 70
source에 '※' 로 시작하는 광고 제거
```

## WeeklyKhan
```
cid = 58
source에 '※이번 호를 끝으로 시리즈 연재를 마칩니다.' 제거
```

## Chosun
```
cid = 125
무난
```

## SanChosun
```
cid = 56
무난
```

## Osen
```
cid = 78
source에 '[OSEN=박선양 기자]' 제거
```

## Kormedi
```
cid = 73
무난
```
## 데이터 개수
|전체|전처리 후|
|:----:|:----:|
|2263698|1752769|

## Example
<img src = 'https://user-images.githubusercontent.com/55969260/94549090-a0b7a900-028c-11eb-8e3a-2b7daae7d2b4.png'> <br>
<img src = 'https://user-images.githubusercontent.com/55969260/94549161-c3e25880-028c-11eb-8220-5a2f7e1db306.png'> <br>
<img src = 'https://user-images.githubusercontent.com/55969260/94549245-e1172700-028c-11eb-9eb6-ec5569bb22d5.png'> <br>
<img src = 'https://user-images.githubusercontent.com/55969260/94549278-ed02e900-028c-11eb-89c9-b3fff0802946.png'> <br>
<img src = 'https://user-images.githubusercontent.com/55969260/94549309-fa1fd800-028c-11eb-9c43-361d8558538f.png'> <br>
