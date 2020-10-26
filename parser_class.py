import re

class BaseParser:
    def __init__(self):
        self.company_id = -1

    def split_paragraph_and_get_if_last_char_is_dot(self, content):
        content = content.split("\n")
        content = [v for v in content if v.strip()]

        last_char_is_dot_paragraph_list = []
        for paragraph in content:
            if paragraph.strip()[-1] == '.':
                last_char_is_dot_paragraph_list.append(paragraph.strip())
        last_char_is_dot_paragraph_str = '\n\n'.join(last_char_is_dot_paragraph_list)

        return last_char_is_dot_paragraph_str

    def big_brace_processing(self, sentence):
        if len(re.findall("\s\s+", sentence)) != 0 and len(re.findall("\s\s+", sentence)[0]) >= 4:
            sentence = sentence[
                       sentence.find(re.findall("\s\s+", sentence)[0]) + len(re.findall("\s\s+", sentence)[0]):]

        if len(re.findall('\[.*?\]', sentence)) >= 1:

            if sentence.find(re.findall('\[.*?\]', sentence)[0]) == 0:

                if len(re.findall('\[.*?\]', sentence)) >= 2:
                    if sentence.find(re.findall('\[.*?\]', sentence)[1]) == sentence.find(
                            re.findall('\[.*?\]', sentence)[0]) + len(re.findall('\[.*?\]', sentence)[0]):
                        sentence = sentence.replace(re.findall('\[.*?\]', sentence)[1], "")

                    sentence = sentence.replace(re.findall('\[.*?\]', sentence)[0], "")
                else:
                    sentence = sentence[sentence.find(re.findall('\[.*?\]', sentence)[0]) + len(
                        re.findall('\[.*?\]', sentence)[0]):]
            else:

                if "기자" in re.findall('\[.*?\]', sentence)[0]:
                    sentence = sentence[sentence.find(re.findall('\[.*?\]', sentence)[0]) + len(
                        re.findall('\[.*?\]', sentence)[0]):]

        return sentence.strip()

    def remove_ad(self, data):
        count_ad = data.count('▶')

        if count_ad == 2:
            start_ad = data.find('▶')
            return data[:start_ad]
        else:
            return data

    def remove_under_N_tokens(self, summ_data, N=3):
        if summ_data.find('\xa0') != -1:
            summ_data = summ_data.replace('\xa0', ' ')
            
        summ_list = summ_data.split(' ')

        return False if len(summ_list) <= N else True

    def IsAd(self, summ_data):
        ad_idx = summ_data.find('▶')

        return True if ad_idx == -1 else False

    def del_overlap(self, result, summary):
        summary_list = summary.split('\n')
        for s_list in summary_list:
            if s_list == '': continue
            result = result.replace(s_list, '')

        return result
    
    def ReplaceToken(self, _text, what1, what2):
        """원하는 토큰을 다른 것으로 치환!"""
        result = _text.replace(what1, what2)
    
        return result

    def DelEndLine(self, _text):
        """\n\n 삭제"""
        result = _text.replace('\n\n\n', ' ')
        result = result.replace('\n\n', ' ')
        result = result.replace('\n', ' ')
        result += '\n'

        return result

    def ReplaceTargetEndLine(self, _text):
        """Target \n -> <eos> """
        result = _text.replace('\n\n', '\n')
        result = result.replace('\n', '</s>')

        return result

    def RemoveSpecialSymbol(self, _text):
        """ 특수기호 제거 """
        symbol = ['▶', '●', '◆', '「', '」', '△', '▷', '◇', '■', '☞', 'Δ',
                  "'", '"', "‘", "’", '“', '”', '‘', '’', "‘", "’", "`"
                  '“', '”', '\xa0']
        for step, sym in enumerate(symbol):
            if sym == '\xa0': _text = _text.replace(sym, ' ')
            else : _text = _text.replace(sym, '')

        return _text

    def RemoveTargetIfThisSymbol(self, _text, isOk):
        """이 심볼 나오면 데이터(타겟)에서 제거"""
        symbol = ['[', ']', '◆', '#', '▶', '<', '>', '≪', '≫']
        check = isOk
        for step, sym in enumerate(symbol):
            if _text.find(sym) != -1:
                check = False

        return check

    def post_edit(self, _text, summary):
        """광고, src tgt 겹침, 기자 제거 """
        _text = _text.replace('\xa0', ' ')
        #_text = _text.replace('\n\n\n', '\n\n')0
        #_text = _text.replace('\n\n', '[SEP]')
        temp_lines = []
        result = []
        
        for line in _text.split('\n\n'):
            line = line.strip()
            if line != '':
                temp_lines.append(line)

        for idx in range(len(temp_lines)):
            split_sentence = temp_lines[idx].split(' ')
            if split_sentence[-1][-1:] == '.':
                result.append(temp_lines[idx])
            else: continue

        return '\n\n'.join(result)

class Newsis(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 12

    def parsing(self, article, summary):
        # Newsis
        #【서울=뉴시스】 =  맨윗줄에 이런거 있음 【 이게 특수문

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        
        if summary.find('[') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None
        
        result = Remove_CASE0(result, _pattern="【[가-힣]+=+[가-힣]+】+\s+[가-힣]+\s+[가-힣]+\s+=+\s")
        result = Remove_CASE0(result, _pattern="[가-힣=0-9(\s]+\)+\s")
        result = Remove_CASE0(result, _pattern="\[[가-힣=]+\]+\s")
        result = Remove_CASE0(result, _pattern="\[[가-힣=]+\]")
        result = Remove_CASE0(result, _pattern="\[[가-힣·=]+]")
        result = Remove_CASE0(result, _pattern="[가-힣]+\s+[가-힣]+\s+=")
        result = Remove_CASE0(result, _pattern="【[가-힣]+\=+[가-힣]+】")
        result = Remove_CASE0(result, _pattern="[가-힣]+\s+[가-힣]+\s+=+\s")
        result = Remove_CASE0(result, _pattern="【[가-힣]+=+[가-힣]+】+[가-힣]+\s+[가-힣]+\s+=+\s")
        result = Remove_CASE0(result, _pattern="【[가-힣]+=+[가-힣]+】+[가-힣]+\s+[가-힣]+기자+\s+=+\s")
        result = Remove_CASE0(result, _pattern="【[가-힣]+=+[가-힣]+】+[가-힣]+\s+[가-힣]+\s+[가-힣]+\s+=+\s")
        result = Remove_CASE0(result, _pattern="\[+[가-힣]+\=+[가-힣]+\]+\s+[가-힣]+\s+[가-힣]+\s+\=+\s")

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        return result, summary

class Fnnews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 32

    def parsing(self, article, summary):
        # 파이낸셜 뉴스
        # fnRASSI는 금융 AI 전문기업 씽크풀과 파이낸셜뉴스의 협업으로 로봇기자가 실시간으로 생산하는 기사입니다.
        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = Remove_CASE0(result, _pattern="【[가-힣]+=+[가-힣]+\s+기자+】")
        result = Remove_CASE0(result, _pattern="【[가-힣]+\s+[가-힣=\s]+】")
        result = Remove_CASE0(result, _pattern="\[+[가-힣]+\]+\s")
        result = Remove_CASE0(result, _pattern="【 [가-힣\s=]+】")
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1:
            isOk_tgt = False
        if summary.find('fnRASS') != -1:
            isOk_tgt = False

        findidx = result.find('fnRASS')
        result = result[:findidx]

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class News1(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 11
    
    def parsing(self, article, summary):
        # 서울뉴스1
        # (서울=뉴스1) 문대현 기자 = 시작하네
        # 앞에서 서울이 아닐수도 세종일수도 고성일수도있음

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가
        result = Remove_CASE0(result, _pattern='[가-힣]+\s+[가-힣]+,')
        result = Remove_CASE0(result, _pattern='[가-힣]+\s+[가-힣]+,+[가-힣]+\s+[가-힣]+,')
        result = Remove_CASE0(result, _pattern='[가-힣=0-9(\sㆍ)]+\s+[가-힣+\s]+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣=0-1]+\)+\s+[가-힣]+\s+[가-힣]+,')
        result = Remove_CASE0(result, _pattern='\([가-힣=0-1]+\)+\s+[가-힣]+\s+[가-힣]+')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=뉴스1\)+\s+[가-힣]+\s+기자+\s+=\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣0-9]+\)+\s+[가-힣]+\s+[가-힣]+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣0-9]+\)+\s+[가-힣]+\s+[가-힣,]+\s+[가-힣]+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣0-9]+\)+\s+[가-힣]+\s+[가-힣,]+\s+[가-힣,]+\s+[가-힣,]+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣0-9]+\)+\s+[가-힣]+\s+[가-힣,]+\s+[가-힣,]+\s+[가-힣,]+\s[가-힣,]+\s+=+\s')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Asiae(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 28

    def parsing(self, article, summary):
        # Asiae

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        
        if summary.find('▶') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = Remove_CASE0(result, _pattern='\[[가-힣=\s]+\]+\s')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Edaily(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 29

    def parsing(self, article, summary):
        # Edaily

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가 (1246) 이런 거 제거
        result = Remove_CASE0(result, _pattern='\([0-9]+\)')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary
    
class HanKyung(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 33

    def parsing(self, article, summary):
        # 한국경제
        # 맨처음 시작할때 src tgt 겹침

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        
        if summary.find('◆') != -1:
            isOk_tgt = False
        if summary.find('네이버에서') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary
    
class Nocutnews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 35

    def parsing(self, article, summary):
        # 노컷뉴스

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1:
            isOk_tgt = False
        if summary.find('사진으로') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary
    
class Heraldcorp(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 34

    def parsing(self, article, summary):
        # 해럴드경제

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = Remove_CASE0(result, _pattern='\[[가-힣=\s]+］')
        result = Remove_CASE0(result, _pattern='[가-힣\s=]+\]')
        result = Remove_CASE0(result, _pattern='[[가-힣\s=]+]+\s')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary
    
class Segye(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 6

    def parsing(self, article, summary):
        # 세계일보 (별로)
        # 맨마지막 ⓒ 세상을 보는 눈, 글로벌 미디어 이런글이있음
        # 아랫건 못지우겠음 다 다르다
        # 베이징=이우승 특파원 이런글도
        # 황용호 선임기자 -> 이런건 글자수로 짜를듯

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        summary = summary.replace('세계일보', '')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가
        result = result.replace('ⓒ 세상을 보는 눈, 세계일보', '')
        result = Remove_CASE0(result, _pattern='[가-힣]+\s+기자+\s+[a-zA-Z0-9_-]+@[a-z]+.[a-z]+\s')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Sedaily(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 27

    def parsing(self, article, summary):
        # 서울경제
        # [서울경제]가 거의 맨 첫줄에 뜬다

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        
        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        
        if summary.find('▶') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가 (1246) 이런 거 제거
        result = Remove_CASE0(result, _pattern='\([0-9]+\)')
        result = Remove_CASE0(result, _pattern=r"(\[서울경제\])")

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Wowty(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 16

    def parsing(self, article, summary):
        # wow TV
        # ▶ 네이버 홈에서 [한국경제TV] 채널 구독하기 [생방송보기]
        # ▶ 대한민국 재테크 총집결! - [증권 / 주식상담 / 부동산]

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶ 네이버 홈에서 [한국경제TV] 채널 구독하기 [생방송보기]') != -1:
            isOk_tgt = False
        if summary.find('※') != -1 or summary.find('<사진') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Moneys(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 37

    def parsing(self, article, summary):
        # 머니S

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1 or summary.find('☞') != -1 or summary.find('※') != -1:
            isOk_tgt = False

        findidx = result.find('☞')
        result = result[:findidx]

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Kmib(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 2

    def parsing(self, article, summary):
        # 국민일보

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('[국민일보') != -1 or summary.find('[') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Hankookilbo(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 10

    def parsing(self, article, summary):
        # 한국일보 tgt에 광고밖에 없는데? 데이터 빼자

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Mt(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 26

    def parsing(self, article, summary):
        # 머니투데이

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('변호사') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        findidx = result.find('▶')
        result = result[:findidx]

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Yna(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 13

    def parsing(self, article, summary):
        # 맨첫줄의 (서울=연합뉴스) 정빛나 기자 =  이런부분 떄야함
        # 맨첫줄이 기자요약문
        # 그다음두번째가 우리가 쓸 요약문
        # src가 다 짤리는데????????????????????????

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(article)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('기사제공') != -1:
            isOk_tgt = False
        
        if summary.find('▶') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣]+\)+\s+[가-힣]+\s+기자+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=[가-힣]+\)+\s+[가-힣]+\s+[가-힣]+\s+[가-힣]+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣]+=+[가-힣]+\)+\s+[가-힣]+\s+특파원+\s+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣·]+=+[가-힣]+\)+\s+[가-힣+\s]+=+\s')
        result = Remove_CASE0(result, _pattern='\([가-힣=]+\)+\s')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Mk(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 25

    def parsing(self, article, summary):
        # 매일경제

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('※')
        result = result[:findidx]

        if summary.find('네이버에') != -1:
            isOk_tgt = False

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Seoul(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 5

    def parsing(self, article, summary):
        # 서울신문

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('네이버에서') != -1:
            isOk_tgt = False
            
        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)
        
        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Donga(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 3

    def parsing(self, article, summary):
        # 동아일보

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        isOk_tgt_ad = super().IsAd(summary)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt and isOk_tgt_ad: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Inews24(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 44

    def parsing(self, article, summary):
        # Inews 24
        # [아이뉴스24 ] 가 맨윗줄에 있네

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('▶')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가
        result = Remove_CASE0(result, _pattern=r"(\[아이뉴스24\s+\])")
        result = Remove_CASE0(result, _pattern='\[[가-힣]+[0-9]+\s+[가-힣]+\s기자+\]')

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Etnews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 45

    def parsing(self, article, summary):
        # et News 전자신문   tgt 가 다 똑같은 문제..

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)

        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('※')
        result = result[:findidx]

        summary = summary.replace('▶ 네이버 모바일에서 [전자신문] 채널 구독하기', '')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶ 인공지능(') != -1:
            isOk_tgt = False
        if summary.find('▶') != -1:
            isOk_tgt = False
        if summary.find('◆ Report') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Dt(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 42

    def parsing(self, article, summary):
        # et News 전자신문

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('고견을 듣는다') != -1:
            isOk_tgt = False

        findidx = result.find('네이버 채널에서')
        result = result[:findidx]

        result = Remove_CASE0(result, _pattern=r"(\[디지털타임스\s+\])")

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가[ ] 에게 고견을 듣는다, 네이버 채널에서 '디지털타임스'를 구독해주세요.

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Hani(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 9

    def parsing(self, article, summary):
        # 한겨례

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Mbn(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 20

    def parsing(self, article, summary):
        # mbn
        # 동영상 뉴스 없애야될듯??? 이 데이터도 빼!

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1:
            isOk_tgt = False
        if result.find('동영상') != -1:
            isOk_src = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Dailian(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 36

    def parsing(self, article, summary):
        # Dailian
        # 맨 아랫줄 (주)데일리안 - 무단전재, 변형, 무단배포 금지

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가
        tmpLines = []
        for line in result.split('\n\n'):
            line = line.strip()
            if line != '':
                tmpLines.append(line)
        if '(주)데일리안' in tmpLines[-1]:
            tmpLines = tmpLines[:-1]

        result = '\n\n'.join(tmpLines)

        findidx = result.find('데일리안')
        result = result[:findidx]

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Ohmynews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 39

    def parsing(self, article, summary):
        # 오마이뉴스
        # 맨윗줄의 [오마이뉴스 ] 가 뜬다
        # 너무 잡다한 글들이 많음... 대체로 길긴한데 편집자글, 관련기사들이 많음
        # [오마이뉴스 이재환 기자]
        # ▶ 해당 기사는 모바일 앱 모이(moi) 에서 작성되었습니다.
        # ▶ 모이(moi)란? 일상의 이야기를 쉽게 기사화 할 수 있는 SNS 입니다.
        # ▶ 더 많은 모이 보러가기
        # src tgt에 화살표 나오면 없애자

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('덧붙이는 글')
        result = result[:findidx]
        findidx = result.find('▶')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('▶') != -1:
            isOk_tgt = False
        # ▲ [오마이포토]
        if summary.find('▲') != -1:
            isOk_tgt = False
        if summary.find('덧붙이는') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class NewsJoins(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 8

    def parsing(self, article, summary):
        # 기본으로도 커버가능
        #    이수정 기자 lee.sujeong1@joongang.co.kr
        #
        #
        # ▶ 네이버 메인에서 중앙일보를 받아보세요
        # ▶ 중앙일보 '홈페이지' / '페이스북' 친구추가
        #
        # ⓒ중앙일보(https://joongang.co.kr), 무단 전재 및 재배포 금지

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('▶')
        result = result[:findidx]
        findidx = result.find('◆  상담=중')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Cnbcsbs(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 21

    def parsing(self, article, summary):
        # SBS
        # 동영상 뉴스 빼야할듯?
        # ■ 경제와이드 모닝벨 '조간 브리핑' - 장연재 -> 네모 붙으면 tgt 아님
        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        findidx = result.find('SBSCNBC')
        result = result[:findidx]
        findidx = result.find('지금까지')
        result = result[:findidx]

        if summary.find('■ SBSCNBC 특보') != -1:
            isOk_tgt = False
        if summary.find('■') != -1:
            isOk_tgt = False
        if summary.find('사진') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Khan(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 1

    def parsing(self, article, summary):
        # 경향신문
        # 류인하 기자 acha@kyunghyang.com
        #
        #
        # ▶ 네이버 메인에서 경향신문 받아보기
        #  ▶ 두고 두고 읽는 뉴스 ▶ 인기 무료만화
        #
        #
        #
        # ©경향신문(www.khan.co.kr), 무단전재 및 재배포 금지

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('▶')
        result = result[:findidx]
        #result = super().post_edit(result, summary)

        while summary.find('ㆍ') != -1 : summary = summary.replace('ㆍ', '')
        #summary = summary.replace('ㆍ', '')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Tvchosun(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 23

    def parsing(self, article, summary):
        # ☞ 네이버 메인에서 TV조선 구독하기
        # ☞ 더 많은 TV조선 뉴스 보기
        # ☞ TV조선 뉴스 홈페이지 바로가기
        # * 뉴스제보 : 이메일(tvchosun@chosun.com), 카카오톡(tv조선제보), 전화(1661-0190)
        #
        # 홍연주 기자(playhong@chosun.com)
        #
        # - Copyrights ⓒ TV조선. 무단전재 및 재배포 금지 -

        # tgt ☞ 네이버 메인에서 TV조선 구독하기 계속 반복

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        summary = summary.replace('☞ 네이버 메인에서 TV조선 구독하기', '')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Ytn(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 24

    def parsing(self, article, summary):
        # YTN
        # 동영상 뉴스 지우자
        # tgt  ▶ 대한민국 24시간 뉴스 채널 YTN 생방송보기 반복

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        findidx = result.find('YTN ')
        result = result[:findidx]
        findidx = result.find('※')
        result = result[:findidx]
        findidx = result.find('▶')
        result = result[:findidx]

        if summary.find('▶') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        # 무난 YTN 천상규입니다.
        return result, summary

class BizChosun(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 30

    def parsing(self, article, summary):
        # biz chosun

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Sbs(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 117

    def parsing(self, article, summary):
        # SBS
        # 맨아래는 (기획·구성: 심우섭, 장아람 / 디자인: 감호정) 이런식으로 되어있으
        # 동영상 뉴스가 많네 6번인덱스 등등

        result = super().remove_ad(article)
        result = result.replace('.]','].')
    
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')
        result = result.replace('].', '.]')
        summary = summary.replace('[SBS스페셜] ', '')

        #result = Remove_CASE0(result, _pattern="\[[가-힣 \s]+\/[가-힣 \s]+\:")

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('*') != -1:
            isOk_tgt = False
        if result.find('※') != -1:
            isOk_tgt = False
        # 광고글, 오디오
        if result.count('▶') >= 2:
            isOk_src = False
        # ※ 자세한 내용은 동영상으로 확인하실 수 있습니다.
        if result.find('※') != -1:
            isOk_src = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Jtbc(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 17

    def parsing(self, article, summary):
        # JTBC
        # 동영상 뉴스 거르자

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Kbs(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 108

    def parsing(self, article, summary):
        # KBS
        # 동영상 뉴스

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        findidx = result.find('※')
        result = result[:findidx]
        findidx = result.find('*')
        result = result[:findidx]

        if result.count('▶') > 4:
            isOk_src = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class NewsJoins(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 61

    def parsing(self, article, summary):
        # 기본으로도 커버가능

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=2)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Imbc(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 113

    def parsing(self, article, summary):
        # Imbc
        # 동영상 뉴스는 뺴자 src 시작이 동영상 뉴스 이면 빼버리기
        # MBC 뉴스는 24시간 여러분의 제보를 기다립니다.

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        if result.find('동영상 뉴스') != -1:
            isOk_src = False

        findidx = result.find('MBC뉴스')
        result = result[:findidx]
        findidx = result.find('Copyright')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('MBC 뉴스는 24시간') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Ichannela(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 15

    def parsing(self, article, summary):
        # 채널 A
        # 동영상 뉴스 tgt ※자세한 내용은 사건상황실에서 확인하실 수 있습니다. 반복
        # tgt가 요약이 아님 데이터 빼야함

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('※자세한')
        result = result[:findidx]
        findidx = summary.find('※자세한')
        summary = summary[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Zdnet(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 46

    def parsing(self, article, summary):
        # ZDnet
        # 2번째 줄에 (지디넷코리아=) 가 남음
        # ZD 특으로 맨윗줄이 정말 짧은 요약문
        # 아래론 중간정도 요약문
        # ▶ 지디넷코리아 '홈페이지' 반복 걍 빼버리기
        # tgt랑 src 겹치는거 일반 적인 함수로 안 없어짐

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        summary = summary.replace("▶ 지디넷코리아 '홈페이지'", '')
        result = result.replace(summary, '')
        result = Remove_CASE0(result, _pattern="\([가-힣]+=+[가-힣]+\s+기자+\)")

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Chosun(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 125

    def parsing(self, article, summary):
        # 조선일보
        # [ ]
        # [][][]
        # 이렇게 마지막 두줄에 있음 위것 length 로 짤림
        # 아랫줄은 regex로 짜르자
        # 전처리 했는데 데이터가 다 사라져보린다.. 데이터 빼
        """
        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        isOk_src = super().remove_under_N_tokens(result, N=2)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        # isOk_tgt_ad = super().IsAd(summary)
        if isOk_src and isOk_tgt: pass
        else: return None

        # 추가
        result = Remove_CASE4(result, _pattern=r"\[.*?\]", _idx=-1)
        """
        return article, summary
##------------------------------------------------------------------
class Pressian(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 40

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Munhwa(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 4

    def parsing(self, article, summary):
        # [ 문화닷컴 바로가기 | 문화일보가 직접 편집한 뉴스 채널 | 모바일 웹 ]

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('문화닷컴 바로가기') != -1:
            isOk_tgt = False
        if summary.find('모바일 웹') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Busan(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 66

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Imaeil(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 65

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Kwnews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 64

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('*') != -1:
            isOk_tgt = False
        if summary.find('Small') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        # 추가 【철원】 [양구]
        result = result.replace('속보=', '')
        result = Remove_CASE0(result, _pattern="\【[가-힣]+\】+[가-힣]+=+")
        result = Remove_CASE0(result, _pattern="\【[가-힣]+\】+")
        result = Remove_CASE0(result, _pattern="\[[가-힣]+\]")

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Tf(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 124

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Joseilbo(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 31

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Sisajournal(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 54

    def parsing(self, article, summary):
        # ☞ 네이버에서 시사저널 뉴스를 받아 보세요

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('☞') != -1:
            isOk_src = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Womennews(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 69

    def parsing(self, article, summary):
        # [여신 후원자 되기]
        # ▶ 네이버에서 여성신문 채널을 구독하세요.
        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find("▶")
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('[여신 후원자') != -1:
            isOk_src = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Mediatoday(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 38

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class MagazineHankyung(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 63

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Isplus(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 93

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=3)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Journalist(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 67

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class H21Hani(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 62

    def parsing(self, article, summary):
        # 마지막줄
        # <한겨레21>이 후원제를 시작합니다. 정의와 진실을 지지하는 방법, <한겨레21>의 미래에 투자해주세요.

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('<한겨레21>이 후원제를')
        result = result[:findidx]
        findidx = result.find('*')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Sisain(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 53

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class WeeklyDonga(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 59

    def parsing(self, article, summary):
        # ▶ 네이버에서 [주간동아] 채널 구독하기
        # ▶ 주간동아 최신호 보기 / 정기구독 신청하기

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        isOk_tgt_ad = super().IsAd(summary)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt and isOk_tgt_ad: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Shindonga(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 55

    def parsing(self, article, summary):
        # ▶ 네이버에서 [신동아] 채널 구독하기
        # ▶ 신동아 최신호 보기 / 정기구독 신청하기

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        isOk_tgt_ad = super().IsAd(summary)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt and isOk_tgt_ad : pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Newscham(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 71

    def parsing(self, article, summary):
        # 이 기사는 정보공유라이선스 2.0 : 영리금지'를 따릅니다.

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('이 기사는 정보공유라이선스')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class EnewsImbc(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 98

    def parsing(self, article, summary):
        # ▶ 내 아이돌의 BEST PICK 광고

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        isOk_tgt_ad = super().IsAd(summary)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt and isOk_tgt_ad : pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class WeeklyChosun(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 60

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Newstapa(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 119

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Ildaro(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 70

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('※')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        if summary.find('ACTion!') != -1:
            isOk_tgt = False

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class WeeklyKhan(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 58

    def parsing(self, article, summary):
        # ※이번 호를 끝으로 시리즈 연재를 마칩니다.
        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        findidx = result.find('※')
        result = result[:findidx]

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class SanChosun(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 56

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Osen(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 78

    def parsing(self, article, summary):
        # [OSEN=박선양 기자]

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        result = Remove_CASE0(result, _pattern="\[[A-Z]+=[가-힣]+\s+기자+\]")

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

class Kormedi(BaseParser):
    def __init__(self):
        super().__init__()
        self.company_id = 73

    def parsing(self, article, summary):

        result = super().remove_ad(article)
        result = super().split_paragraph_and_get_if_last_char_is_dot(result)
        result = super().big_brace_processing(result)
        result = super().del_overlap(result, summary)
        result = super().ReplaceToken(result, '▲', '↑')
        summary = super().ReplaceToken(summary, '▲', '↑')

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)

        isOk_tgt = super().RemoveTargetIfThisSymbol(summary, isOk_tgt)

        if isOk_src and isOk_tgt: pass
        else: return None, None

        result = super().DelEndLine(result)
        summary = super().ReplaceTargetEndLine(summary)

        result = super().RemoveSpecialSymbol(result)
        summary = super().RemoveSpecialSymbol(summary)

        isOk_src = super().remove_under_N_tokens(result, N=10)
        isOk_tgt = super().remove_under_N_tokens(summary, N=2)
        if isOk_src and isOk_tgt:
            pass
        else:
            return None, None

        return result, summary

def Remove_CASE0(text, _pattern):
    """원하는 패턴 입력 받아 지워줌"""
    return re.sub(_pattern, '', text)

def MakeParser(cid):
    if cid == '12': parser = Newsis
    elif cid == '32': parser = Fnnews
    elif cid == '11': parser = News1
    elif cid == '28': parser = Asiae
    elif cid == '29': parser = Edaily
    elif cid == '33': parser = HanKyung
    elif cid == '35': parser = Nocutnews
    elif cid == '34': parser = Heraldcorp
    elif cid == '6': parser = Segye
    elif cid == '27': parser = Sedaily
    elif cid == '16': parser = Wowty
    elif cid == '37': parser = Moneys
    elif cid == '2': parser = Kmib
    elif cid == '10': parser = Hankookilbo
    elif cid == '26': parser = Mt
    elif cid == '13': parser = Yna
    elif cid == '40': parser = Pressian
    elif cid == '25': parser = Mk
    elif cid == '5': parser = Seoul
    elif cid == '3': parser = Donga
    elif cid == '44': parser = Inews24
    elif cid == '45': parser = Etnews
    elif cid == '42': parser = Dt
    elif cid == '4': parser = Munhwa
    elif cid == '7': parser = BizChosun
    elif cid == '66': parser = Busan
    elif cid == '9': parser = Hani
    elif cid == '20': parser = Mbn
    elif cid == '36': parser = Dailian
    elif cid == '65': parser = Imaeil
    elif cid == '39': parser = Ohmynews
    elif cid == '8': parser = NewsJoins
    elif cid == '64': parser = Kwnews
    elif cid == '21': parser = None #Cnbcsbs 동영상뉴스
    elif cid == '1': parser = Khan
    elif cid == '124': parser = Tf
    elif cid == '23': parser = Tvchosun
    elif cid == '24': parser = Ytn
    elif cid == '30': parser = BizChosun
    elif cid == '117': parser = Sbs
    elif cid == '31': parser = Joseilbo
    elif cid == '17': parser = Jtbc
    elif cid == '108': parser = Kbs
    elif cid == '54': parser = Sisajournal
    elif cid == '69': parser = Womennews
    elif cid == '38': parser = Mediatoday
    elif cid == '63': parser = MagazineHankyung
    elif cid == '93': parser = Isplus
    elif cid == '113': parser = Imbc
    elif cid == '61': parser = NewsJoins
    elif cid == '15': parser = None #Ichannela
    elif cid == '67': parser = Journalist
    elif cid == '62': parser = H21Hani
    elif cid == '53': parser = Sisain
    elif cid == '59': parser = WeeklyDonga
    elif cid == '55': parser = Shindonga
    elif cid == '52': parser = Mk
    elif cid == '71': parser = Newscham
    elif cid == '98': parser = EnewsImbc
    elif cid == '46': parser = Zdnet
    elif cid == '60': parser = WeeklyChosun
    elif cid == '119': parser = Newstapa
    elif cid == '70': parser = Ildaro
    elif cid == '58': parser = WeeklyKhan
    elif cid == '125': parser = None#Chosun
    elif cid == '56': parser = SanChosun
    elif cid == '78': parser = Osen
    elif cid == '73': parser = Kormedi
    else : return None

    return parser
