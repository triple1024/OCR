import pyautogui as pag

# pag.alert(text='テスト', title='alert BOX', button='OK')

# pag.confirm(text='テスト', title='alert BOX', buttons=['OK','NG'])

# text = pag.prompt(text='テスト', title='alert BOX', default='OK')

# print(text)

text = pag.password(text='テスト', title='alert BOX', default='', mask='*')

print(text)