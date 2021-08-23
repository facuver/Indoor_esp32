import ujson
import ntptime
import utime

default = {
    "AP_password": "test1234",
    "AP_essid": "iSpindel_Repeater",
    "update_interval": "600",
    "ubidots_token": "",
    "STA_essid": "",
    "STA_password": "",
}
automation_defaults = {
    "ligth": {"status": 0, "time_on": 0, "time_off": 0, "time": 0},
    "pump": 0,
    "humidity": 0,
    "humidity_target": 60,
    "soil_target": 0,
    "soil_humidity": 0,
    "water_reserve": 0,
    "temp": 0,
    "fans": {"status": 0, "duty": 0},
}


def read_configs() -> dict:
    try:
        with open("config.json", "r") as f:
            conf = ujson.load(f)
    except Exception as e:
        print("Error: ", e)
        return default

    return conf


def update_configs(conf: dict) -> dict:
    with open("config.json", "w") as f:
        ujson.dump(conf, f)
    return conf


def read_automation():
    try:
        with open("automation.json", "r") as f:
            auto = ujson.load(f)
    except Exception as e:
        print("Error: ", e)
        return automation_defaults

    return auto


def update_automation(auto):
    print(auto)
    with open("automation.json", "w") as f:
        ujson.dump(auto, f)
    return auto


def log(msg):
    try:
        with open("log.txt", "a") as f:
            time = utime.localtime(ntptime.time() - 10800)
            time = "{}/{}/{} {}:{}:{}".format(
                time[2], time[1], time[0], time[3], time[4], time[5]
            )
            f.write("[{}] {} \n".format(time, msg))
    except Exception as e:
        print(e)


configs = read_configs()
automation = read_automation()


ip = "192.168.4.1"
