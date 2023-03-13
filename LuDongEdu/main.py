import requests
import ddddocr
from bs4 import BeautifulSoup as BS
from requests_toolbelt.multipart.encoder import MultipartEncoder

class ldu:
    def __init__(self,account,pwdEncryption) -> None:
        self.s = requests.session()
        self.s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'}
        self.account = account
        self.pwdEncryption = pwdEncryption
        
    def page_login(self):
        html = self.s.get('https://xsjw.ldu.edu.cn/login').text
        soup = BS(html,'lxml')
        self.token = soup.find_all('input',{'id':'tokenValue'})[0]['value']

    def deal_pic(self):
        res = self.s.get('https://xsjw.ldu.edu.cn/img/captcha.jpg')

        image = res.content
        ocr = ddddocr.DdddOcr(beta=True)
        self.picWords = ocr.classification(image)
        print(f"read pic: {self.picWords}")
    
    def post_check(self):
        form = {
        'tokenValue': self.token,
        'j_username': self.account,
        'j_password': self.pwdEncryption,
        'j_captcha': self.picWords
        }
        res = self.s.post('https://xsjw.ldu.edu.cn/j_spring_security_check',\
            data=form,allow_redirects=False)
        print(f'login: {res.status_code}')
        
    def login(self):
        self.page_login()
        self.deal_pic()
        self.post_check()
    
    def evaluation(self,evaTxt='好'):
        # evaTxt: evaluate text
        
        self.login()

        form = {
            'pageNum': 1,
            'pageSize': 30,
            'flag': 'ktjs'
        }
        queryAllUrl = 'https://xsjw.ldu.edu.cn/admin/teachingAssessment/evaluation/queryAll'
        res = self.s.post(queryAllUrl,data=form)
        queryAll = res.json()
        recordsLi = queryAll['data']['records']
        
        tasksLen = len(recordsLi)
        print(f"find {tasksLen} subjects to evaluate.")
        paramsDic = {'WJBM': '','KTID':[],'PGID':[]}
        paramsDic['WJBM'] = recordsLi[0]['WJBM']
        for tdic in recordsLi:
            paramsDic['KTID'].append(tdic['KTID'])
            paramsDic['PGID'].append(tdic['PGID'])
        
        for i in range(tasksLen):
            formEva = {'wjbm': paramsDic['WJBM'],'pgid': '','ktid': '','tjcs':'2'} # evaluate form
            formEva['pgid'] = paramsDic['PGID'][i]
            formEva['ktid'] = paramsDic['KTID'][i]
            
            print(f'{i+1} is doing.')
            # find detail params
            viewHtmlUrl = f'https://xsjw.ldu.edu.cn/student/teachingEvaluation/newEvaluation/editEvaluationResult/{paramsDic["KTID"][i]}'
            deHtml = self.s.get(viewHtmlUrl).text
            soup0 = BS(deHtml,'lxml')
            # token value
            evaToken = soup0.find_all('input',{'id':'tokenValue'})[0]['value']
            formEva['tokenValue'] = evaToken
            
            chooseBtn = soup0.find_all('input',{'class':'ace'})
            # 4 bottons : a b c d, choose a
            for ind,cb in enumerate(chooseBtn):
                if ind % 4 == 0:
                    try:
                        cbv = cb['value']
                    except:
                        cbv = ''
                    formEva[cb['name']] = cbv
                    
            comment = soup0.find_all('textarea')[0]['name']
            formEva[comment] = evaTxt
            
            # multipart/form-data
            multipartEncode = MultipartEncoder(
                fields=formEva,
                boundary='------WebKitFormBoundaryAJd4vzDGDC1rUrCL--'
            )
            # evaUrl = f'https://xsjw.ldu.edu.cn/student/teachingAssessment/baseInformation/questionsAdd/doUpdateTmAndDa?tokenValue={evaToken}' # edit evaluation url
            evaUrl = f'https://xsjw.ldu.edu.cn/admin/teachingAssessment/baseInformation/questionsAdd/doSave?tokenValue={evaToken}'
            
            self.s.headers.update({'Content-Type': multipartEncode.content_type})
            # print(multipartEncode.content_type)
            # post
            evaRes = self.s.post(evaUrl,data=multipartEncode)
            print(f'eva status: {evaRes.status_code}')
            print(evaRes.text)

    def test(self):
        self.login()
        url = 'https://xsjw.ldu.edu.cn/main/academicInfo'
        form = {
            'flag': ''
        }
        res = self.s.post(url,data=form)
        print(f'test: {res.text}')

if __name__ == '__main__':
    account = "20202203012"
    pwdEncryption = "bac2b3b74ba7710975de42cb71694232" # md5
    sp = ldu(account,pwdEncryption)

    sp.evaluation()