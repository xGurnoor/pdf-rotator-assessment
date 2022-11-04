# Made for an assessment

## Dependencies
- flask
- PyPDF2
- Requests

## Installation
```bash
git clone https://github.com/xGurnoor/pdf-rotator-assessment.git
cd pdf-rotator-assessment
python3 server.js
```

## Routes
- /
- /rotate

##### /: GET - Landing page
\
##### /rotate?pdf_path=&page_number=&=angle: POST - Route for rotating the PDF page; returns a URL for produced PDF page \

#### Params
##### pdf_path - URL to download PDF from
##### page_number - the number of the page to rotate
##### angle - the angle to rotate the page by; should be multiple of 90

#### Returns
##### The URL where the produced PDF lives
