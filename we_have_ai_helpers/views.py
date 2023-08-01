
from django.shortcuts import render
from os import listdir
from we_have_ai_helpers.webscraper import scrape_and_download_pdfs
from django.core.files.storage import default_storage

def list_pdfs(request):
    # Get a list of all pdf files
    pdf_files = [f for f in default_storage.listdir('scraped_pdfs')[1]]

    # Render the 'list_pdfs.html' template and pass the pdf files as context
    return render(request, 'we_have_ai_helpers/10_list_federal_reserve_loan_officer_survey_data.html', {'pdf_files': pdf_files})
