import requests
import json
import csv
from datetime import datetime
import os

def fetch_and_write_data():
    url = 'https://www.s-bahn-stuttgart.de/service/dbmsg/s-stuttgart/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if not os.path.exists('data'):
        os.makedirs('data')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = f'data/s_bahn_stuttgart_daten_{timestamp}.csv'

    messages = data.get('messages', [])

    fieldnames = [
        'ID',
        'Überschrift',               # 'head'
        'Kurztext',                  # 'lead'
        'Text',                      # 'text'
        'Linien',                    # 'lineNames'
        'Startdatum',                # 'datetime_from'
        'Enddatum',                  # 'datetime_to'
        'Quelle',                    # 'source'
        'Anhänge',                   # 'attachments'
        'Links',                     # 'links'
        'Bild',                      # 'image'
        'Kategorien',                # 'chip'
        'Nachrichtentypen',          # 'msgTypes'
        'Zeitstempel',               # 'constructionInfoTimestamp'
        'Betroffene Haltestellen',   # 'segmentStops'
        'Aktualisierungszeit',       # 'timestamp' (neues Feld)
    ]

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        # Schreiben der Header
        writer.writeheader()

        for message in messages:
            row = {}

            row['ID'] = message.get('id', '')
            row['Überschrift'] = message.get('head', '')
            row['Kurztext'] = message.get('lead', '')
            row['Quelle'] = message.get('source', '')
            row['Bild'] = message.get('image', '')
            row['Zeitstempel'] = message.get('constructionInfoTimestamp', '')

            text_list = message.get('text', [])
            row['Text'] = ' '.join(text_list)

            # 'lineNames' ist eine Liste von Liniennamen
            line_names = message.get('lineNames', [])
            row['Linien'] = ', '.join(line_names)

            datetime_entries = message.get('datetime', [])
            if datetime_entries:
                # Wir nehmen die ersten Werte
                dt = datetime_entries[0]
                row['Startdatum'] = dt.get('dateFrom', '')
                row['Enddatum'] = dt.get('dateTo', '')
            else:
                row['Startdatum'] = ''
                row['Enddatum'] = ''

            attachments = message.get('attachments', [])
            attachment_labels = [att.get('label', '') for att in attachments]
            row['Anhänge'] = '; '.join(attachment_labels)

            links = message.get('links', [])
            link_labels = [link.get('label', '') for link in links]
            row['Links'] = '; '.join(link_labels)

            chips = message.get('chip', [])
            row['Kategorien'] = ', '.join(chips)

            msg_types = message.get('msgTypes', [])
            row['Nachrichtentypen'] = ', '.join(msg_types)

            segment_stops = message.get('segmentStops', [])
            row['Betroffene Haltestellen'] = ', '.join(segment_stops)

            row['Aktualisierungszeit'] = datetime.now().isoformat()

            writer.writerow(row)

if __name__ == '__main__':
    fetch_and_write_data()
