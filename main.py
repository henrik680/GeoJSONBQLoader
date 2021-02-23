
#!/usr/bin/env python3
# See: https://medium.com/@lakshmanok/how-to-load-geojson-files-into-bigquery-gis-9dc009802fb4

import json, logging, argparse
import geojson

logging.getLogger().setLevel(logging.INFO)


def process_file(input_file, output_file):
    with open(input_file, 'r') as ifp:
        with open(output_file, 'w') as ofp:
            features = json.load(ifp)['features']
            # new-line-separated JSON
            schema = None
            for obj in features:
                props = obj['properties']  # a dictionary
                props['geometry'] = json.dumps(obj['geometry'])  # make the geometry a string
                p = geojson.Point((props['geo_point_2d'][0], props['geo_point_2d'][1]))
                props['geo_point_2d'] = geojson.dumps(p)
                json.dump(props, fp=ofp)
                print('', file=ofp)  # newline
                if schema is None:
                    schema = []
                    for key, value in props.items():
                        if key == 'geometry':
                            schema.append('geometry:GEOGRAPHY')
                        elif key == 'geo_point_2d':
                            schema.append('geo_point_2d:GEOGRAPHY')
                        elif isinstance(value, str):
                            schema.append(key)
                        else:
                            schema.append('{}:{}'.format(key,
                                                         'int64' if isinstance(value, int) else 'float64'))
                    schema = ','.join(schema)
            print('Schema: ', schema)


if __name__ == '__main__':
    logging.info("Starting GeoJSONBQLoader")
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='path to input file')
    parser.add_argument('--outfile', help='path to output file')
    args = parser.parse_args()
    # logging.info('run(...): data=' + args.data)
    process_file(args.infile, args.outfile)

    #logging.info('run(...): requestr={}'.format(request))

