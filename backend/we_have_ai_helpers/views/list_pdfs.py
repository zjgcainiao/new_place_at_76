from .base import render, default_storage


def list_pdfs(request):
    # Get a list of all pdf files. add if f to eclude empty ones
    pdf_files = [default_storage.url('scraped_pdfs/' + f)
                 for f in default_storage.listdir('scraped_pdfs')[1] if f]

    # Render the 'list_pdfs.html' template and pass the pdf files as context
    return render(request, 'we_have_ai_helpers/10_list_federal_reserve_loan_officer_survey_data.html', {'pdf_files': pdf_files})
