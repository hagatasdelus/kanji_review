def make_answer_format(answer):
    answer_tag = ''
    answer_tag += '<div style="text-align: center; font-family: serif; font-size: 30px;">'
    answer_tag += f'''
            <p>{answer.readings}</p>
            </div>
        '''
    return answer_tag
