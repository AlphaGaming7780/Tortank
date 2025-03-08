import threading
from flask import Flask, jsonify, render_template, request
from TortankWebServer.TortankLib.Tortank import Tortank

tortank : Tortank = Tortank()
app = Flask("TortankWebServer", static_url_path='')

waterLevel = [0, 0, 0]

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/GetUpdatedValue', methods=["GET"])
def SendGetUpdatedValue():
    rep = jsonify(
        {
            "WaterLevel": waterLevel, 
            "MotorSpeed": [
                tortank.GetMotor1Speed(), 
                tortank.GetMotor2Speed()
            ]
        }
    )
    rep.status_code = 200
    return rep

@app.route('/GetWaterLevel', methods=["GET"])
def SendWaterLevel():
    rep = jsonify(waterLevel)
    rep.status_code = 200
    return rep

@app.route('/GetMotorSpeed', methods=["GET"])
def SendMotorSpeed():
    rep = jsonify( 
        [ 
            tortank.GetMotor1Speed(), 
            tortank.GetMotor2Speed() 
        ] 
    )
    rep.status_code = 200
    return rep

def main():
    webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=False, use_reloader=False))
    # webServerThread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    webServerThread.start()
    # app.run(use_reloader=True)

    # tortank.SetMotor1Speed(1)
    # tortank.SetMotor2Speed(1)

    while(True):

        waterLevel[0] = tortank.GetWaterLevelCuve1()
        waterLevel[1] = tortank.GetWaterLevelCuve2()
        waterLevel[2] = tortank.GetWaterLevelCuve3()

        # waterLevel[0] = 0.5
        # waterLevel[1] = 0.025
        # waterLevel[2] = 0.975

        print(waterLevel)

        waterLevelMax = max(waterLevel)
        voltageMax = max( tortank.cuve1.voltage, tortank.cuve2.voltage, tortank.cuve3.voltage )

        if( waterLevelMax >= tortank.TORTANK_WATER_LEVEL_MAX or voltageMax >= 5 ) :
            tortank.SetMotor1Speed(0)
            tortank.SetMotor2Speed(0)
        pass

if __name__ == "__main__":
    main()