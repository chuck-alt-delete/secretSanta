from fasthtml.common import *

app = FastHTML(
    hdrs=picolink, 
    debug=True
    )
db = database('data/santa.db')


def navbar():
    return Nav(
        Div(
            A("Home", href='/'),
            A("Assignments", href='/assignments')
        )
    )

@app.get("/")
def get_homepage():
    return Titled(
        "Casias Secret Santa",
        navbar(),
        Card(
            Div(
                P("Welcome to the Casias family Secret Santa site!", style='text-align: center')
            )
        )
    )

def assignment_table(gifter:str|None = None, giftee:str|None = None, year:int|None = None) -> Table:
    # Base query
    query = "SELECT * FROM assignments"
    conditions = []
    params = []

    # Add conditions based on which parameters are provided
    if gifter:
        conditions.append("gifter like ?")
        params.append(gifter)
    
    if giftee:
        conditions.append("giftee like ?")
        params.append(giftee)
    
    if year:
        conditions.append("year = ?")
        params.append(year)

    # If there are any conditions, append them to the query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    results = db.query(query, params)

    rows = [
        Tr(
            *[Td(value) for value in result.values()]
        )
        for result in results
        ]
    head = Thead(
        *[Th(column) for column in ("gifter", "giftee", "year")])
    return Table(
                head,
                *rows,
                style='margin-left: auto; margin-right:auto'
        )


@app.get("/assignments")
def get_assignments(gifter:str|None=None, giftee:str|None=None, year:int|None=None):

    frm = Card(
            Form(
                Input(id='gifter', placeholder='gifter'),
                Input(id='giftee', placeholder='giftee'),
                Input(id='year', placeholder='year'),
                Button('submit'),
                action=f'/assignments', method='get')
        )

    return Titled(
        "Past Secret Santa Assignments",
        navbar(),
        frm,
        assignment_table(gifter, giftee, year)
    )

@app.get("/favicon.ico")
def get_favicon():
    return FileResponse('./static/favicon.png')

serve()