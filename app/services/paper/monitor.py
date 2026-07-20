from app.services.paper.engine import PaperTradingEngine


class PositionMonitor:


    def __init__(self):

        self.engine = PaperTradingEngine()



    def check(self, price):

        result = self.engine.check_position(
            price
        )


        if result["status"] == "CLOSED":

            print()

            print("=== POSITION CLOSED ===")

            print(result)


        elif result["status"] == "OPEN":

            print()

            print("=== POSITION ACTIVE ===")

            print(result)


        else:

            print("NO OPEN POSITION")


        return result
