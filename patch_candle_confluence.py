from pathlib import Path

p = Path("app/services/smart_money/confluence_engine.py")

s = p.read_text(encoding="utf-8")


# добавляем получение candle модуля
if 'candle = modules.get("candle", {})' not in s:

    s = s.replace(
        'volume = modules.get("volume", {})',
        'volume = modules.get("volume", {})\n        candle = modules.get("candle", {})'
    )


# добавляем блок свечного анализа
marker = """
        # ==========================
        # DIRECTION
        # ==========================
"""

block = """
        # ==========================
        # CANDLE PATTERNS
        # ==========================

        if candle.get("bullish_engulfing"):

            score += 15
            reasons.append(
                "BULLISH ENGULFING"
            )


        if candle.get("bearish_engulfing"):

            score += 15
            reasons.append(
                "BEARISH ENGULFING"
            )


        if candle.get("hammer"):

            score += 10
            reasons.append(
                "HAMMER"
            )


        if candle.get("shooting_star"):

            score += 10
            reasons.append(
                "SHOOTING STAR"
            )


        if candle.get("bullish_pin_bar"):

            score += 10
            reasons.append(
                "BULLISH PIN BAR"
            )


        if candle.get("bearish_pin_bar"):

            score += 10
            reasons.append(
                "BEARISH PIN BAR"
            )


        if candle.get("morning_star"):

            score += 15
            reasons.append(
                "MORNING STAR"
            )


        if candle.get("evening_star"):

            score += 15
            reasons.append(
                "EVENING STAR"
            )


        if candle.get("three_white_soldiers"):

            score += 20
            reasons.append(
                "THREE WHITE SOLDIERS"
            )


        if candle.get("three_black_crows"):

            score += 20
            reasons.append(
                "THREE BLACK CROWS"
            )


        if candle.get("inside_bar"):

            score += 5
            reasons.append(
                "INSIDE BAR"
            )


        if candle.get("outside_bar"):

            score += 10
            reasons.append(
                "OUTSIDE BAR"
            )


        if candle.get("body_strength") == "STRONG":

            score += 5
            reasons.append(
                "STRONG BODY"
            )


"""

if "CANDLE PATTERNS" not in s:

    s = s.replace(
        marker,
        block + marker
    )


p.write_text(s, encoding="utf-8")

print("CANDLE CONFLUENCE V1 PATCH OK")
