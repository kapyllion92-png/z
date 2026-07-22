from app.services.simulation.paper_trader import PaperTrader


trader = PaperTrader()


def simulate_trade(trade):

    position = trader.open_trade(

        side=trade["side"],

        qty=trade["qty"],

        entry=trade["price"],

        stop_loss=trade["stop_loss"],

        take_profit=trade["take_profit"]

    )


    print()

    print("=== PAPER TRADE OPENED ===")

    print(position)



    return trader
