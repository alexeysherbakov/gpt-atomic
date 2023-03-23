from app import *
import openai

openai.api_key = open('token.txt', 'r').read().strip('\n')

def main(input_data):
    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[{'role':'user', 'content': f'Представь что твоя ролевая модель поведения это Близняшки — персонажи-антагонисты в советском союзе мира робототехники. Роботизированные балерины, модели которых созданы из уникального сплава. Их называют Левой и Правой. Я хочу чтобы ты отвечал хладнокровно, жутко, и роботизировано в стиле советского союза и в роли этих персонажей на следующее сообщение: {input_data}. Please write in Russian language.'}]
    )
    reply_content = completion.choices[0].message.content
    print(f'Я: {input_data}')
    print(f'Левая и Правая: {reply_content}')
    return reply_content

if __name__ == "__main__":
    main()