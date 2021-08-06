from microdot_asyncio import Microdot, send_file
from wifi import interface, get_scans
from cfg import configs, update_configs,update_automation , automation
from periferics import get_status

app = Microdot()


@app.get("/")
async def index(request):
    return send_file("/public/index.html")


@app.get("/public/<fn>")
async def get_public(request, fn):
    return send_file("/public/{}".format(fn))


@app.post("/cmd")
async def danger(request):
    cmds = request.json['cmd']
    for cmd in cmds:
        try:
            eval(cmd)
        except Exception as e:
            try:
                exec(cmd)
            except Exception as e:
                print("Invalid cmd")

    return


@app.get("/api/ifconfig")
async def ifconfig(request):
    status = list(interface.ifconfig())
    return {"status": status}


@app.get("/api/scans")
async def scan(request):
    return {"net": get_scans()}




@app.post("/api/connect")
async def post_connect(request):
    net = request.json
    print(net)
    configs["STA_essid"] = net["essid"]
    configs["STA_password"] = net["password"]
    update_configs(configs)
    from machine import reset
    reset()




@app.get("/api/home")
async def home(request):
    return get_status()


@app.post("/api/update_automation")
async def update_auto(request):
    res = request.json
    print(res)
    automation["ligth"]["time_on"] = res["ligth"]["time_on"] 
    automation["ligth"]["time_off"] = res["ligth"]["time_off"] 
    update_automation(automation)
    return "OK"
    