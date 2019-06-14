from influxdb import InfluxDBClient
import json, argparse, os, yaml

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='directory storing data')
    parser.add_argument('influxdb_yml', help='YAML file of configurations for InfluxDB')
    args = parser.parse_args()

    SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
    config_file = SCRIPT_PATH + "/" + args.influxdb_yml 
    conf = yaml.load(stream=open(config_file).read(), Loader=yaml.SafeLoader)

    points = []
    for data_file in os.listdir(args.data_dir):
        with open(args.data_dir + os.sep + data_file, 'r') as f:
            data_list = json.load(f)
            for data in data_list:
                point = {}
                point["measurement"] = "mitemp"
                point["tags"] = {}
                point["tags"]["mac"] = data["mac"]
                point["time"] = data["time"]
                point["fields"] = {}
                point["fields"]["temperature"] = data["temperature"]
                point["fields"]["humidity"] = data["humidity"]
                point["fields"]["battery"] = data["battery"]
                points.append(point)

    client = InfluxDBClient(host=conf['INFLUX_DB']['HOST'], \
                            port=conf['INFLUX_DB']['PORT'], \
                            username=conf['INFLUX_DB']['USERNAME'], \
                            password=conf['INFLUX_DB']['PASSWORD'], \
                            database=conf['INFLUX_DB']['DATABASE'])
    client.write_points(points)

if __name__ == '__main__':
    main()
