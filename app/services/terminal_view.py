class TerminalView:


    def show_signals(self, signals):


        print()

        print("================================")

        print("     TOP-10 БУДУЩИХ СДЕЛОК")

        print("================================")


        if not signals:

            print()

            print("Сигналов нет")

            return



        for index, signal in enumerate(
            signals,
            start=1
        ):


            print()

            print(
                f"#{index} {signal.get('монета')}"
            )


            print(
                "Направление:",
                signal.get("направление")
            )


            print(
                "Стратегия:",
                signal.get("стратегия")
            )


            print(
                "Сила:",
                signal.get("итоговая_оценка"),
                "/100"
            )


            print(
                "Потенциал:",
                signal.get("ожидаемый_профит"),
                "%"
            )


            print()

            print("Почему:")


            for reason in signal.get(
                "причины",
                []
            ):

                print(
                    "✓",
                    reason
                )


            print()

            print(
                "Статус:",
                signal.get(
                    "статус",
                    "НАБЛЮДЕНИЕ"
                )
            )

            print("--------------------------------")
