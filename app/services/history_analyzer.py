import json
import os


class HistoryAnalyzer:


    def __init__(self):

        self.file = "app/data/history.json"


        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f
                )



    def save_pattern(self, data):


        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            history = json.load(f)



        history.append(data)



        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )




    def compare(self, current):


        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            history = json.load(f)



        if len(history) == 0:

            return {

                "совпадений":0,

                "вероятность":0,

                "вывод":"Недостаточно истории"

            }



        matches = 0

        wins = 0



        for item in history:


            score = 0



            if item.get("тренд") == current.get("тренд"):

                score += 1



            if item.get("rsi_zone") == current.get("rsi_zone"):

                score += 1



            if item.get("объём") == current.get("объём"):

                score += 1



            if score >= 2:

                matches += 1



                if item.get("результат") == "PROFIT":

                    wins += 1




        if matches == 0:

            probability = 0

        else:

            probability = round(
                wins / matches * 100,
                2
            )



        return {


            "совпадений":

                matches,


            "побед":

                wins,


            "вероятность":

                probability,


            "вывод":

                "Хорошее совпадение"
                if probability >= 65
                else
                "Слабое совпадение"

        }
