import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import functions_framework
import flask_cors


SPREADSHEET_ID = "1sMwuifM7WVBTtb_e_owyoOruDHtAQ18PgO5cFx9Cb00"
CELL_RANGE = "Main!C:O"


def get_scores():
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=CELL_RANGE)
            .execute()
        )
        values = result.get("values", [])
        return values
    except HttpError as err:
        print(err)
        return None


@functions_framework.http
@flask_cors.cross_origin()
def main(request):
    scores = get_scores()
    if scores is None:
        scores = []
    scores = scores[:1] + sorted(
        scores[1:],
        reverse=True,
        key=lambda row: float(row[1]))
    return scores
