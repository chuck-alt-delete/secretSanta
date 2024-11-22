from fasthtml.common import *
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastHTML(
    hdrs=picolink, 
    debug=True
    )
db = database('data/santa.db')


def navbar():
    return Nav(
        Div(
            A("Home", href='/'),
            A("See Past Assignments", href='/assignments'),
            A("New Assignment", href='/new-assignment'),
            A("Send Emails", href='/send-email')

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

    query = "SELECT * FROM assignments"
    conditions = []
    params = []

    if gifter:
        conditions.append("gifter like ?")
        params.append(gifter)
    
    if giftee:
        conditions.append("giftee like ?")
        params.append(giftee)
    
    if year:
        conditions.append("year = ?")
        params.append(year)

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
        *[Th(column) for column in ("gifter", "giftee", "year")]
        )
    return Table(
                head,
                *rows,
                style='margin-left: auto; margin-right:auto'
        )


@app.get("/assignments")
def get_assignments(gifter:str|None=None, giftee:str|None=None, year:int|None=None):

    return Titled(
        "Past Secret Santa Assignments",
        navbar(),
        Card(
            Form(
                Input(id='gifter', placeholder='gifter'),
                Input(id='giftee', placeholder='giftee'),
                Input(id='year', placeholder='year'),
                Button('submit'),
                action=f'/assignments', method='get')
        ),
        assignment_table(gifter, giftee, year)
    )

@app.get("/new-assignment")
def get_new_assignment():
    return Titled(
        "Create New Secret Santa Assignment",
        navbar(),
        Card(
            Form(
                Input(id="year", placeholder="Enter year", type="number", name="year", required=True),
                Button("Create Assignments", type="submit"),
                action="/new-assignment", method="post"
            )
        )
    )

@app.post("/new-assignment")
def post_new_assignment(year: int):

    # Fetch all users and their restrictions
    users = db.query("SELECT id, name FROM Users")

    # Combine restrictions:
    # 1. Permanent restrictions from UserRestrictions (year IS NULL)
    # 2. Last year's assignments from SecretSantaAssignments
    restrictions = db.query(
        """
        SELECT user_id, restricted_user_id
        from (
            SELECT user_id, restricted_user_id
                FROM UserRestrictions
                WHERE year IS NULL
        union 
            SELECT gifter_id AS user_id, giftee_id AS restricted_user_id
            FROM SecretSantaAssignments
            WHERE year = ?
        )
        """,
        (year - 1,)
    )

    
    # Prepare data structures for assignment
    user_ids = [user["id"] for user in users]
    random.shuffle(user_ids)
    restricted = {r["user_id"]: r["restricted_user_id"] for r in restrictions}
    
    # Generate valid assignments
    assignments = {}
    attempts = 0
    max_attempts = 100  # Limit retries
    while attempts < max_attempts:
        random.shuffle(user_ids)
        if is_valid_assignment(user_ids, restricted):
            assignments = {gifter: giftee for gifter, giftee in zip(user_ids, user_ids[1:] + user_ids[:1])}
            break
        attempts += 1
    
    if not assignments:
        return Titled(
            "Create New Secret Santa Assignment",
            navbar(),
            Card(P("Failed to generate valid assignments after multiple attempts."))
        )
    
    # Save assignments in the database
    for gifter_id, giftee_id in assignments.items():
        db.t.SecretSantaAssignments.insert(giftee_id=giftee_id, gifter_id=gifter_id, year=year)

    
    return Titled(
        "Create New Secret Santa Assignment",
        navbar(),
        Card(P(f"Assignments created successfully for the year {year}!"))
    )
@app.get("/send-email")
def get_send_email():
    default_body = """
Hi {gifter},

You are the Secret Santa for {giftee} this year!

Happy gifting!
"""
    return Titled(
        "Send Secret Santa Emails",
        navbar(),
        Card(
            Form(
                Input(id="year", placeholder="Enter year", type="number", name="year", required=True),
                Textarea(
                    id="email_body", 
                    name="email_body", 
                    placeholder="Enter the email body here...",
                    required=True,
                    value=default_body,
                    style="width: 100%; height: 200px;"
                ),
                Div(
                    Label("Dry Run:"),
                    Input(id="dry_run", name="dry_run", type="checkbox", checked=True),
                    style="margin-top: 10px;"
                ),
                Button("Send Emails", type="submit"),
                action="/send-email", method="post"
            )
        )
    )

@app.post("/send-email")
def post_send_email(year: int, email_body: str, dry_run: bool = True):
    # Fetch assignments for the specified year
    assignments = db.query(
        """
        SELECT 
            gifter.id as gifter_id, gifter.name as gifter_name, gifter.email as gifter_email,
            giftee.name as giftee_name
        FROM SecretSantaAssignments
        JOIN Users gifter ON SecretSantaAssignments.gifter_id = gifter.id
        JOIN Users giftee ON SecretSantaAssignments.giftee_id = giftee.id
        WHERE year = ?
        """,
        (year,)
    )
    
    if not assignments:
        return Titled(
            "Send Secret Santa Emails",
            navbar(),
            Card(P(f"No assignments found for the year {year}."))
        )
    
    # Dry run: Send a single email to the sender with all assignments
    if dry_run:
        with open("santaDataSecrets", "r") as secret:
            secrets = dict(line.strip().split("=") for line in secret)
            sender_email = secrets["email"]

        body = "Secret Santa Assignments:\n\n"
        for assignment in assignments:
            body += f"{assignment['gifter_name']} -> {assignment['giftee_name']}\n"

        send_email(
            sender_email,  # To sender_email
            "Santa Admin",  # Gifter (Admin)
            "Santa Assignments",  # Giftee (Placeholder)
            year,
            body
        )

        return Titled(
            "Send Secret Santa Emails",
            navbar(),
            Card(P("Dry run successful! All assignments sent to the sender's email."))
        )
    else:
        # Regular email sending
        for assignment in assignments:
            customized_body = email_body.format(
                gifter=assignment["gifter_name"],
                giftee=assignment["giftee_name"]
            )
            send_email(
                assignment["gifter_email"],
                assignment["gifter_name"],
                assignment["giftee_name"],
                year,
                customized_body
            )
    
    return Titled(
        "Send Secret Santa Emails",
        navbar(),
        Card(P(f"Emails sent successfully for the year {year}!"))
    )

def is_valid_assignment(user_ids, restricted):
    for gifter_id, giftee_id in zip(user_ids, user_ids[1:] + user_ids[:1]):
        if giftee_id == gifter_id or restricted.get(gifter_id) == giftee_id:
            return False
    return True

def send_email(email, gifter, giftee, year, email_body):

    # Load email credentials
    with open("santaDataSecrets", "r") as secret:
        secrets = dict(line.strip().split("=") for line in secret)
        sender_email = secrets["email"]
        sender_password = secrets["password"]

    # Configure SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create email
    subject = f"Casias Family Christmas Secret Santa {year}"
    body = email_body  # Use the custom body passed to the function
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    server.sendmail(sender_email, email, message.as_string())
    server.quit()


@app.get("/favicon.ico")
def get_favicon():
    return FileResponse('./static/favicon.png')

serve()