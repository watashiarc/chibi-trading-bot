import requests

import time
from io import StringIO
import pandas as pd


def get_sqz_metrics_report(): 
    t = time.time() * 1000
    url = 'https://squeezemetrics.com/monitor/static/DIX.csv?_t=' + str(t)
    r = requests.get(url)
    sqz_csv = StringIO(r.content.decode('utf-8'))
    sqz_df = pd.read_csv(sqz_csv, sep=",")
    sqz_df = sqz_df.sort_values(by='date', ascending=False)

    sqz_today = sqz_df.iloc[0]
    sqz_yesterday = sqz_df.iloc[1]
    sqz_day_before_yest = sqz_df.iloc[2]

    # Get SPX change values
    spx_today_change = "{:.2%}".format((sqz_today['price'] - sqz_yesterday['price']) / sqz_yesterday['price'])
    spx_yesterday_change = "{:.2%}".format((sqz_yesterday['price'] - sqz_day_before_yest['price']) / sqz_day_before_yest['price'])

    # Get DIX values
    dix_today_percent = "{:.2%}".format(sqz_today['dix'])
    dix_yesterday_percent = "{:.2%}".format(sqz_yesterday['dix'])
    dix_day_before_yest_percent = "{:.2%}".format(sqz_day_before_yest['dix'])

    # Get GEX values
    gex_today = "{:,}".format(sqz_today['gex'])
    gex_yesterday = "{:,}".format(sqz_yesterday['gex'])
    gex_day_before_yest = "{:,}".format(sqz_day_before_yest['gex'])

    report = (
        "```"
        f"\n{sqz_yesterday['date']}"
        "\nSPX"
        f"\n{sqz_day_before_yest['price']} --> {sqz_yesterday['price']} ({spx_yesterday_change})"
        "\nDIX"
        f"\n{dix_day_before_yest_percent} --> {dix_yesterday_percent}"
        "\nGEX" 
        f"\n{gex_day_before_yest} --> {gex_yesterday}"
        "\n```"
        "\n```"
        f"\n{sqz_today['date']}"
        "\nSPX"
        f"\n{sqz_yesterday['price']} --> {sqz_today['price']} ({spx_today_change})"
        "\nDIX"
        f"\n{dix_yesterday_percent} --> {dix_today_percent}"
        "\nGEX" 
        f"\n{gex_yesterday} --> {gex_today}"
        "\n```"
    )

    return report