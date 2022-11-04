from flask import Flask, request
from PyPDF2 import PdfReader, PdfWriter
from uuid import uuid4

import io, requests 

app = Flask(__name__)

@app.get('/')
def hello():
    return 'Hello! Use <a href="/rotate">/rotate</a> route to roate some pages.<br><br><strong><u>POST</u> /rotate</strong>/<br>Required parameters:<br>file_path: publicly accessibly file path<br>page_number: the number of page to rotate<br>angle: a multiple of 90, the angle to rotate page by<br><strong>RETURNS</strong>:<br>a publicly accessible URL of the produced PDF'

@app.post('/rotate')
def test():
    
    query_params = request.args
    required_params = ['file_path', 'angle', 'page_number']
    
    # check if required paramters were provided
    for x in required_params:
        if x not in query_params.keys():
            return f"{x} parameter not found!"
    
    # extracting required data
    file_path = query_params['file_path']
    angle = query_params['angle']
    page_number = query_params['page_number']
    
    # validate page number
    try:
        page_number = int(page_number) 
        if page_number == 0:
            return 'page_number must be greater than 0!'
        page_number = page_number - 1
    except ValueError:
        return 'page_number must be an integer!'

    # converting angle to a number and checking if its a multiple of 90
    try:
        angle = int(angle)
    except ValueError:
        return 'angle should be a number and a multiple of 90 (90, 180, 270)!'
    if angle % 90 != 0:
        return 'angle should be a number and a multiple of 90 (90, 180, 270)!'


    # download the file into a BytesIO object to make manipulation easier without making a mess with files (not production-friendly)
    resp = requests.get(file_path)
    obj = io.BytesIO(resp.content)

    # setup PDF reader and writer classes
    reader = PdfReader(obj)
    writer = PdfWriter()

    total_num = len(reader.pages)

    # check if page_number is greater than actual number of pages
    if page_number > total_num:
        return f'page_number ({page_number}) greater than total number of pages ({total_num})! '

    # add pages to writer
    for x in reader.pages:
        writer.add_page(x)

    # rotate the page
    writer.pages[page_number].rotate(angle)

    # generate (barely) unique ID for the file name
    file_id = uuid4().hex[:10]

    with open(f'static/{file_id}.pdf', 'wb') as fp:
        writer.write(fp)

    
    return f'Completed succesfully! See the file <a href="http://localhost:8000/static/{file_id}.pdf">here</a>'


app.run(port=8000)