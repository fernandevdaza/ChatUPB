from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")

# Reemplazar con tu API Key
client = OpenAI(api_key=config.get("OPENAI_API_KEY"))

# Crea un Hilo de conversación
thread = client.beta.threads.create()

#Crea un mesnsaje en el hilo de conversación
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Explicame el método multiplicador de lagrange",
)

#Crea una ejecución del hilo de conversación
#configurar cuidadosamente los tokens, para evitar gastos innecesarios
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id='asst_MhFtFuc1soGd9eItosYv64BY',
  max_prompt_tokens=50,
  max_completion_tokens=50,
)

# Espera a que la ejecución del hilo de conversación se complete
while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")
        break

# Obtiene todos los mensajes del hilo de conversación
all_messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Imprime los mensajes del hilo de conversación
print("###################################################### \n")
print(f"USER: {message.content[0].text.value}")
print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")