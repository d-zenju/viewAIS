# coding: utf-8
import folium
import argparse
import json

def main():
    parser = argparse.ArgumentParser (
        prog='AIS Viewer',
        usage='AISデータ表示プログラム',
        description='python3 app.py -i [AIS_JSON_TYPES_FILEPATH] ...',
        epilog='Copyright 2018 Daisuke Zenju',
        add_help=True
        )

    parser.add_argument('-i', '--input', help='Input JSON Types Filepath')
    parser.add_argument('-t', '--time', help='Set Time (ISO8601)')
    args = parser.parse_args()

    if args.input:
        input_jsn_type_filepath = args.input
        jsn_f = open(input_jsn_type_filepath, 'r')
        jsn = json.load(jsn_f)
        jsn_f.close()

        time_list = list(jsn['123'].keys())

        if args.time:
            if args.time in time_list:
                smap = folium.Map(
                    location=[35.316, 139.780],
                    zoom_start=10,
                    tiles='OpenStreetMap'
                    )
                
                for data in jsn['123'][args.time]:
                    msg = 'MMSI : ' + str(data['mmsi']) + '<br />'\
                        + 'Lat, Lon : ' + str(data['y']) + ', ' + str(data['x']) + '<br />'\
                        + 'NAV Status : ' + data['nav_status_text'] + '<br />'\
                        + 'SOG, COG : ' + str(data['sog']) + ', ' + str(data['cog']) + '<br />'\
                        + 'HDG : ' + str(data['true_heading']) + '<br />'\
                        + 'Timestamp : ' + data['utc']
                    folium.Marker(
                        [data['y'], data['x']],
                        popup=msg
                    ).add_to(smap)
            smap.save('./map.html')
                

        else:
            print('Start: ' + time_list[0] + ', End: ' + time_list[-1])


if __name__ == '__main__':
    main()