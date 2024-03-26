import fitz
import sys

# считываем текст из pdf файла
file = f'data/{input()}'
with fitz.open(file) as doc:
    all_text = ''
    for page in doc:
        all_text += page.get_text()

# разбиваем текст на задания
all_text = all_text.replace('-\n', '').split('\n')
print(all_text)
tasks = {}

task_num = 0
for i in all_text:
    if i.startswith(f'{task_num + 1}.'):
        task_num += 1
        tasks[task_num] = [i]
    elif task_num != 0 and i != '':
        tasks[task_num].append(i)

doc = fitz.Document()
blank_page = fitz.open('data/blank.pdf')

for key in tasks.keys():
    doc.insert_pdf(blank_page)
    page = doc[key - 1]

    n = 18
    rect = page.rect + (n, n, -n, -n)
    text = ''.join(tasks[key]).replace('- ', '')

    page.insert_htmlbox(rect, ' '.join(tasks[key]), css="* {font-family: 'math';font-size:13px;}")

doc.save(f'{file[:-4]}-copy.pdf')
