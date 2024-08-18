from fasthtml.common import *

app = FastHTML(hdrs=picolink)
db = database('data/santa.db')


@app.get("/")
def get_homepage():
    return Titled(
        "Casias Secret Santa",
        Card(
            Div(
                P("hello", style="text-align: center;")
            )
        ),
        A("Past assignments", href='/assignments', title="past assignments")
    )

@app.get("/assignments")
def get_assignments():
    results = db.query(
        """
        select 
            u1.name as gifter, 
            u2.name as giftee, 
            year 
        from 
            SecretSantaAssignments s 
            join users u1 on s.gifter_id = u1.id 
            join users u2 on s.giftee_id = u2.id
        order by year desc
        """
        )
    rows = [
        Tr(
            *[Td(value) for value in result.values()]
        )
        for result in results
        ]
    head = Thead(
        *[Th(column) for column in ("gifter", "giftee", "year")],
        cls="bg-purple/10")
    return Titled("Past Secret Santa Asignments",
        Table(
                head,
                *rows,
                style='margin-left: auto; margin-right:auto'
        )
    )

serve()