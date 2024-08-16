from fasthtml.common import *

app = FastHTMLWithLiveReload()

db = database('data/santa.db')


@app.get("/")
def get_homepage():
    return Titled(
        "Casias Secret Santa",
        Card(
            Div(
                P("hello", style="text-align: center;")
            )
        )
    )

@app.get("/assignments")
def get_assignments():
    rows = db.query(
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
    return Ul(
        *[Li(
            P(f"Gifter: {row['gifter']}"),
            P(f"Giftee: {row['giftee']}"),
            P(f"Year: {row['year']}")
        ) for row in rows]
    )

serve()