from groq import Groq
import os
from dotenv import load_dotenv

# carrega variáveis de ambiente do .env
load_dotenv()
# salva chave para api
api_key = os.getenv('API_KEY')
# acesso a partir de key
client = Groq(api_key=api_key)

# =================
# FUNÇÕES PARA RECONHECER COMO PROSSEGUIR NO PROGRAMA

# modelo reconhece se o aluno quer fazer questões; retorna 'SIM' ou 'NÃO'
def aluno_quer_questionario(prompt_estudante):
  prompt = 'Reconheça explicitamente o pedido do aluno de gerar um questionário e RESPONDA APENAS com "NÃO" \
            se o aluno não quer que seja gerado um questionário e com "SIM" se ele quiser que seja gerado um questionário. \
            A mensagem do aluno está entre colchetes: [' + prompt_estudante + '].'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# modelo reconhece se o aluno quer finalizar programa; retorna 'SIM' ou 'NÃO'
def aluno_quer_terminar_programa(prompt_estudante):
  prompt = 'Reconheça explicitamente e implicitamente e RESPONDA APENAS com "NÃO" se o aluno quer continuar fazendo \
            perguntas e com "SIM" se ele quiser finalizar o programa. A mensagem do aluno está entre colchetes: [' + prompt_estudante + '].'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# =================
# FUNÇÕES PARA RETIRAR INFORMAÇÕES DO PROMPT DO ALUNO

# a partir do prompt do usuário, o modelo reconhece qual o assunto e matéria a ser estudado; retorna string contendo apenas o conteúdo de estudo
def reconhece_assunto(prompt_estudante):
  prompt = 'Apenas indique o conteúdo de estudo ao qual a mensagem entre colchetes se refere [' + prompt_estudante + ']\
            e não explique nada, diga apenas qual o assunto.'
  completion = client.chat.completions.create(
    # model='deepseek-r1-distill-llama-70b',
    # model='llama-3.3-70b-versatile',
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=0, max_tokens=2024, top_p=0.4, stream=False, stop=None
  )
  return completion.choices[0].message.content

# a partir do prompt do usuário, o modelo reconhece o nível do estudante na matéria; retorna nível do aluno
def reconhece_nivel_aluno_texto(prompt_estudante):
  prompt = 'Indique qual o nível do aluno a partir das suas respostas a partir da mensagem entre colchetes [' + prompt_estudante + ']. \
            Responda simplesmente com o nível do aluno. \
            Os níveis para classificação dos alunos: iniciante, iniciante-intermediário, intermediário, intermediário-avançado, avançado.'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# a partir do prompt do usuário, o modelo reconhece o nível do estudante na matéria; retorna nível do aluno
def reconhece_nivel_aluno_questoes(respostas_certas, respostas_aluno):
  prompt = 'Compare as respostas certas com as respostas do aluno. Indique qual o nível do aluno a partir das suas respostas. \
            Os níveis para classificação dos alunos: iniciante, iniciante-intermediário, intermediário, intermediário-avançado, avançado. \
            Responda simplesmente com o nível do aluno. \
            As respostas certas estão entre colchetes [' + respostas_certas + '] e as respostas do aluno estão entre chaves {' + respostas_aluno + '}.'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# a partir de todos os prompts do usuário, o modelo reconhece o nível do estudante na matéria e sua evolução; retorna nível e evolução do aluno
def reconhece_nivel_prompts_aluno(todos_prompts_aluno):
  prompt = 'Reconheça o avanço do aluno ao longo das mensagens dele. Reconheça o avanço dele para cada diferente assunto. Cada mensagem do aluno está separada pelo símbolo "}" \
            e todas as mensagens do aluno estão entre colchetes [' + todos_prompts_aluno + ']. Descreva breve e resumidamente a evolução dele e o parabenize!'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# =================
# FUNÇÕES PARA GERAÇÃO E RESOLUÇÃO DE QUESTÕES

# o modelo vai gerar questões sobre o assunto reconhecido; retorna as questões geradas
def gera_questionario(assunto):
  prompt = 'Gere um questionário de 3 questões sobre o assunto ' + assunto
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# o modelo vai responder às questões que ele gerou para fornecer respostas corretas para comparação posteriormente; retorna respostas às questões
def resolve_questionario(questoes):
  prompt = 'Resolva as questões entre colchetes [' + questoes + '].'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# =================
# FUNÇÕES QUE TRAZEM EXPLICAÇÕES E FEEDBACKS PARA O USUÁRIO

# a partir do assunto reconhecido e do prompt do usuário, retorna uma explicação sobre o conteúdo passado
def explica(assunto, prompt_estudante):
  nivel_aluno = reconhece_nivel_aluno_texto(prompt_estudante)

  prompt = 'Responda detalhadamente à mensagem entre colchetes [' + prompt_estudante + '] como um tutor que dá suporte ao\
            aprendizado do estudante e responda perguntas detalhadamente, explique detalhadamente e tire as dúvidas\
            do usuário sobre o conteúdo' + assunto + '. Responda à mensagem para que um aluno de nível ' + nivel_aluno + ' entenda.'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# compara as respostas corretas e as respostas do aluno e envia um feedback para ele; retorna o feedback para o aluno
def compara_respostas_feedback(respostas_certas, respostas_aluno):
  nivel_aluno = reconhece_nivel_aluno_questoes(respostas_certas, respostas_aluno)

  prompt = 'Compare as respostas certas com as respostas do aluno. Explique detalhadamente o que o aluno errou num nível ' + nivel_aluno + 'para que ele entenda. . \
            As respostas certas estão entre colchetes [' + respostas_certas + '] e as respostas do aluno estão entre chaves {' + respostas_aluno + '}.'
  completion = client.chat.completions.create(
    model='llama-3.3-70b-specdec',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1, max_tokens=5000, top_p=0.5, stream=False, stop=None
  )
  return completion.choices[0].message.content

# =================
# LOOP DE FUNCIONAMENTO DO CHAT

lista_prompts_aluno = []

while(True):
  prompt_estudante = input('Escreva sua dúvida: ')
  lista_prompts_aluno.append(prompt_estudante)

  if(aluno_quer_questionario(prompt_estudante) == 'SIM'):
    questoes = gera_questionario(assunto)
    print('Para praticar, geramos as seguintes questões. Tente resolvé-las e ter um feedback de desempenho!\n\n\=================\n\nQuestionário:\n', questoes)
    print('\n\=================\n')
    respostas_aluno = input('Digite suas respostas: ')
    lista_prompts_aluno.append(respostas_aluno)
    
    questoes_resolvidas = resolve_questionario(questoes)
    print(compara_respostas_feedback(questoes_resolvidas, respostas_aluno))
    print('\n\=================\n')
  else:
    if(aluno_quer_terminar_programa(prompt_estudante) == 'SIM'):
      break
    assunto = reconhece_assunto(prompt_estudante)
    print(explica(assunto, prompt_estudante))
    print('\n\=================\n')

# salva os prompts do aluno no arquivo
f = open("prompts_aluno.txt", "a")
f.write('}' + '}'.join(lista_prompts_aluno))
f.close()

# lê o arquivo e salva todo o texto na variável 'prompts'
f = open("prompts_aluno.txt", "r")
prompts = f.read()
f.close()

# ao fim da execução do programa, é indicada a evolução do estudante a partir de todos os prompts de todas as sessões
print(reconhece_nivel_prompts_aluno(prompts))
print('Finalizando o programa')

'''

testes

Eu estou com dúvidas no assunto sobre o fim da Idade Média e gostaria que você falasse um pouco sobre esse assunto de História.
Mas eu ainda não entendi direito o motivo maior para o fim da idade média
Acho que entendi, o conjunto de eventos que ocorreram no século 14 foi que levou então à queda da igreja católica e do sistema feudal nas regiões da europa, culminando no fim da idade média?
Ok, entendi perfeitamente que todos os eventos criou um ambiente complexo e fez o fim do sistema feudal e da idade média se desenvolver. Obrigada!

Estou com dúvidas em matemática, pois não estou entendendo como fazer equações lineares, pode me ajudar?
Estou estudando geografia e gostaria que você explicasse detalhadamente o começo, meio e fim da guerra fria
o que foi o pacto de varsóvia?
o professor de biologia nao explicou direito o assunto de panspermia cosmica que vai cair na prova eu nao sei de nada me ajuda

'''