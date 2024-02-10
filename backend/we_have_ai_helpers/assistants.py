from openai import OpenAI
client = OpenAI()
# https://platform.openai.com/docs/api-reference/assistants/createAssistant


assitant_code_interpreter_01 = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4",
)

assitant_func_01 = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4",
)

assitant_retrieval_01 = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "retrieval"}],
    model="gpt-4",
)
print(assitant_func_01)
