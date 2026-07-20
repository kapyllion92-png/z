from fastapi import FastAPI

from app.services.scanner_engine import get_signals


app = FastAPI()



@app.get("/")
def home():

    return {

        "status":
            "LIVE",

        "service":
            "Bybit Pro Terminal X"

    }





@app.get("/signals")
def signals():


    try:


        data = get_signals()



        if data is None:

            data = []



        return {


            "status":

                "LIVE",



            "count":

                len(data),



            "signals":

                data



        }



    except Exception as e:


        return {


            "status":

                "ERROR",



            "count":

                0,



            "signals":

                [],



            "error":

                str(e)

        }
