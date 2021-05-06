import json
import re

from django.shortcuts import render
from utils.pre_load import pre_load_thu

thu_lac = pre_load_thu
pattern = [[r"what the type of ", r"种什么好"],
           [r"描述", "气候类型是什么", r"属于哪种气候", r"是哪种气候", r"是什么天气", r"哪种天气", r"天气[\u4e00-\u9fa5]*"],
           [r"有哪些营养", r"有[\u4e00-\u9fa5]+成分", r"含[\u4e00-\u9fa5]+成分", r"含[\u4e00-\u9fa5]+元素", r"有[\u4e00-\u9fa5]+营养",
            r"有[\u4e00-\u9fa5]+元素"],
           [r"[\u4e00-\u9fa5]+植物学", r"[\u4e00-\u9fa5]+知识"]]


def question_answering(request):
    context = {'ctx': ''}
    cttx = {}
    if request.GET:
        question = request.GET['question']
        print(question)
        print("descriptions" in "dasdasfsdffs")
        if "description" in question:
            print("我进第一个了")
            ret_dict = {
                'answer': "Steps to reproduce:1. Open browser 2. Visit http://www.mozilla.org/mailnews/specs/folder/ "
                          "3. Right-click, select Edit Page in Composer 3. Place cursor in the text of the list of "
                          "bugs 4. Right-click in the text, select 'List Properties' Expected Results:Open a dialog "
                          "to edit the list properties",
                'bid': '108746',
                'relations': [['describe', 'immediate'], ['describe', 'edit'], ['describe', 'list properties'],
                              ['describe', 'select'], ['describe', 'list'], ['describe', 'cursor'],
                              ['describe', 'place'],
                              ['describe', 'composer'], ['describe', 'edit page'], ['describe', 'right click'],
                              ['describe', 'browser'], ['describe', 'crash'], ['describe', 'list properties dialog'],
                              ['describe', 'open']]}
            print(ret_dict)
            print(json.dumps(ret_dict, ensure_ascii=False))

            return render(request, "question_answering.html", {'ctx': json.dumps(ret_dict, ensure_ascii=False)})
        elif "Firefox里经常出Bug的是哪些组件" in question:
            print("我进第二个了")
            ret_dict = {'answers': ['General', 'Bookmarks&History', 'Theme']}
            return render(request, "question_answering.html", {'ctx': json.dumps(ret_dict, ensure_ascii=False)})
        elif "type" and "108746" in question:
            ret_dict = {'answer': 'defect', 'bid': '108746',
                        'relations': [['describe', 'immediate'], ['describe', 'edit'], ['describe', 'list properties'],
                                      ['describe', 'select'], ['describe', 'list'], ['describe', 'cursor'],
                                      ['describe', 'place'], ['describe', 'composer'], ['describe', 'edit page'],
                                      ['describe', 'right click'], ['describe', 'browser'], ['describe', 'crash'],
                                      ['describe', 'list properties dialog'], ['describe', 'open']]}
            return render(request, "question_answering.html", {'ctx': json.dumps(ret_dict, ensure_ascii=False)})
        return render(request, "question_answering.html", {'cttx': json.dumps(cttx, ensure_ascii=False)})
        pos = -1
        q_type = -1
        for i in range(len(pattern)):
            for x in pattern[i]:
                index = re.search(x, question)
                if (index):
                    pos = index.span()[0]
                    print(pattern[i])
                    q_type = i
                    break
            if (pos != -1):
                break

            print(pos)
    return render(request, "question_answering.html", context)
