from openai import OpenAI
client = OpenAI()
# https://platform.openai.com/docs/api-reference/assistants/createAssistant


assistant_for_customer_user = client.beta.assistants.create(
    instructions="You are a personal assistant that helps answer questions about automotives, cars, car parts, performance and other car related questions. ",
    name="Customer Assistant",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo",
)

assitant_to_run_functions = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="run django functions",
    tools=[{"type": "function"}],
    model="gpt-3.5-turbo",
)

assitant_retrieval_01 = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="data retrieval",
    tools=[{"type": "retrieval"}],
    model="gpt-3.5-turbo",
)
print(assistant_for_customer_user)


# file = client.files.create(
#     file=open(
#         "/Users/stephenwang/Downloads/vin_data_aggregated_sample.json", "rb"),
#     purpose='assistants'
# )
# vin_data_to_pdf_assistant = client.beta.assistants.create(
#     instructions="Process the uploaded JSON file and generate a PDF based on the data. Display nested data structures in different sections within the pdfs.",
#     name="vin_data_to_pdf_assistant",
#     model="gpt-4-turbo-preview",
#     tools=[{"type": "code_interpreter"}],
#     file_ids=[file.id]
# )
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Generate a PDF that summarizes the safety ratings, recall information, and vehicle details from the provided JSON data.",
#             # Assuming file.id is the ID of your uploaded JSON file
#             "file_ids": [file.id]
#         }
#     ],
# )

# thread_message = client.beta.threads.messages.create(
#     thread.id,
#     role="user",
#     content="Generate a PDF that summarizes the safety ratings, recall information, and vehicle details from the provided JSON data.",
#     file_ids=[file.id]  # Include the JSON file ID here
# )

# message_files = client.beta.threads.messages.files.list(
#     thread_id=thread.id,
#     message_id=thread_message.id
# )

# output_pdf_file = client.files.retrieve("file-WZ33muOPAQxfTdAhjOmur8Xp")
# content = client.files.content("file-WZ33muOPAQxfTdAhjOmur8Xp")
