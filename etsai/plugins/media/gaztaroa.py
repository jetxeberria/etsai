from icalendar import Calendar, Event
from datetime import datetime, date
import pytz

# Timezone information
timezone = pytz.timezone('Europe/Madrid')


def main():
    data = _read_data()
    _create_calendar(data)


def _read_data():
    # Sample data (your data from the previous dataframe)
    data = {
        'Fecha': [
            '21/22 SEPTIEMBRE/IRAILA', '6 OCTUBRE/URRIA', '20 OCTUBRE/URRIA',
            '10 NOVIEMBRE/AZAROA', '24 NOVIEMBRE/AZAROA', '15 DICIEMBRE/ABENDUA',
            '12 ENERO/URTARRILA', '26 ENERO/URTARRILA', '9 FEBRERO/OTSAILA',
            '23 FEBRERO/OTSAILA', '9 MARZO/MARTXOA', '23 MARZO/MARTXOA',
            '6 ABRIL/APIRILA', '17/21 ABRIL/APIRILA', '10 MAYO/MAIATZA',
            '24/25 MAYO/MAIATZA', '8 JUNIO/EKAINA', '22 JUNIO/EKAINA'
        ],
        'Lugar': [
            'TRAVESÍA SANSANET-BISAURIN (2669m)-Lizara-Sansanet', 'TRAVESÍA GABARDITO-SESQUES (2355m)-Selva de Oza',
            'ANAYET (2574m) desde Canal Roya', 'EZKAURRE TXIKI (1763 m) desde Zuriza/Belabarce',
            'TXIPETA ALTO (2175m) desde Zuriza', 'PRÁCTICAS DE ESCALADA Y RAPEL',
            'PUERTO DE CORONAS - BELBÚN O BORREGUIL (1423 m) - LEIRE', 'PRÁCTICAS INVERNALES',
            'LAKARTXELA (1979m) desde venta Juan Pito', 'CIRCULAR PUNTA ALTA DE NAPAZAL (2363m) - BERNERA (2432m) desde Lizara',
            'PUNTA AGÜERRI (2447m) desde Gabardito', 'PEYREGET (2487m) desde el Portalet',
            'IRUMUGARRIETA (1431m) desde Gainzta', 'Aste Santua / Semana Santa REFUGIO GERBER',
            'CIRCULAR POR JAKIZKELLE. Vía de los Colores, pasando por la gruta de Akarragí',
            'PICO MARBORÉ (3248m) desde la pradera de Ordesa', 'CIRCULAR SOBRARCAL (2257m)- MALLO DE ACHERITO (2374m) desde La Mina(Selva de Oza)',
            'FINALISTA: OJOS DE LUMBIER + COMIDA'
        ]
    }


def _create_calendar(data):
    # Creating a new calendar
    cal = Calendar()
    cal.add('prodid', '-//Gaztaroa Menditaldea Calendar All-Day Events//')
    cal.add('version', '2.0')
    # Adding events to the calendar as all-day events
    for index, date_str in enumerate(data['Fecha']):
        event = Event()
        start_date, end_date = parse_dates_corrected(date_str)
        event.add('summary', data['Lugar'][index])
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('dtstamp', datetime.now(tz=timezone))
        event.add('location', data['Lugar'][index])
        event.add('description', "Organized by Gaztaroa Menditaldea")

        # Mark the event as all-day
        event.add('X-MICROSOFT-CDO-ALLDAYEVENT', 'TRUE')
        event.add('TRANSP', 'TRANSPARENT')

        cal.add_component(event)

    # Save the calendar as .ics file
    with open('gaztaroa_menditaldea_all_day_calendar.ics', 'wb') as f:
        f.write(cal.to_ical())

    print("Calendar saved as 'gaztaroa_menditaldea_all_day_calendar.ics'")
    return cal


def parse_dates_corrected(date_str):
    """
    Function to parse dates and add the correct year
    Handle both single day or ranged events in format '21-22 SEPTIEMBRE/IRAILA'
    """
    day_range, month = date_str.split()
    if '/' in day_range:
        start_day, end_day = map(int, day_range.split('/'))
    else:
        start_day = end_day = int(day_range)
    month = month.split('/')[1].upper()
    month_map = {
        'IRAILA': 9,
        'URRIA': 10,
        'AZAROA': 11,
        'ABENDUA': 12,
        'URTARRILA': 1,
        'OTSAILA': 2,
        'MARTXOA': 3,
        'APIRILA': 4,
        'MAIATZA': 5,
        'EKAINA': 6
    }

    month_number = month_map[month]
    year = correct_year(date_str)

    start_date = date(year, month_number, start_day)
    end_date = date(year, month_number, end_day + 1)
    return start_date, end_date


def correct_year(date_str):
    """
    Correct year function based on the month of the text.
    September to December months are of the year 2024,
    while January to June months are of the year 2025.
    """
    if any(month in date_str for month in ['IRAILA', 'URRIA', 'AZAROA', 'ABENDUA']):
        return 2024
    else:
        return 2025


if __name__ == "__main__":
    main()
