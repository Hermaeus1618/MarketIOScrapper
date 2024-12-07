import io
import httpx
import asyncio
import numpy as np
import pandas as pd

from urllib import parse

PATTERNLIST=[
    "screen=double_bottom&picker=traditional_patterns&flexible=event;patterns;double_bottom",
    "screen=double_top&picker=traditional_patterns&flexible=event;patterns;double_top",
    "screen=triple_bottom&picker=traditional_patterns&flexible=event;patterns;triple_bottom",
    "screen=triple_top&picker=traditional_patterns&flexible=event;patterns;triple_top",
    "screen=head_and_shoulders&picker=traditional_patterns&flexible=event;patterns;head_shoulders",
    "screen=inverted_head_and_shoulders&picker=traditional_patterns&flexible=event;patterns;inv_head_shoulders",
    "screen=ascending_triangle&picker=traditional_patterns&flexible=event;patterns;asc_triangle",
    "screen=descending_triangle&picker=traditional_patterns&flexible=event;patterns;desc_triangle",
    "screen=pennant&picker=traditional_patterns&flexible=event;patterns;pennant",
    "screen=flag&picker=traditional_patterns&flexible=event;patterns;flag",
    "screen=bearish_flag&picker=traditional_patterns&flexible=event;patterns;flag_bearish",
    "screen=channel&picker=traditional_patterns&flexible=event;patterns;channel",
    "screen=channel_up&picker=traditional_patterns&flexible=event;patterns;channel_up",
    "screen=channel_down&picker=traditional_patterns&flexible=event;patterns;channel_down",
    "screen=cup_and_handle&picker=traditional_patterns&flexible=event;patterns;cup_handle",
    "screen=diamond&picker=traditional_patterns&flexible=event;patterns;diamond",
    "screen=white_body&picker=candlesticks&flexible=event;cdlmisc;cdl_wb",
    "screen=black_body&picker=candlesticks&flexible=event;cdlmisc;cdl_bb",
    "screen=long_white_line&picker=candlesticks&flexible=event;cdlbull;cdl_lowl",
    "screen=hammer&picker=candlesticks&flexible=event;cdlbull;cdl_ham",
    "screen=piercing_line&picker=candlesticks&flexible=event;cdlbull;cdl_pil",
    "screen=bullish_engulfing_lines&picker=candlesticks&flexible=event;cdlbull;cdl_buel",
    "screen=morning_star&picker=candlesticks&flexible=event;cdlbull;cdl_mors",
    "screen=bullish_doji_star&picker=candlesticks&flexible=event;cdlbull;cdl_budjs",
    "screen=bullish_kicker&picker=candlesticks&flexible=event;cdlbull;cdl_buki",
    "screen=bullish_harami&picker=candlesticks&flexible=event;cdlbull;cdl_buha",
    "screen=dragonfly_doji&picker=candlesticks&flexible=event;cdlmisc;cdl_drdj",
    "screen=abandoned_baby_bottom&picker=candlesticks&flexible=event;cdlmisc;cdl_abbb",
    "screen=bullish_counter_attack&picker=candlesticks&flexible=event;cdlbull;cdl_buca",
    "screen=bullish_three_white_soldiers&picker=candlesticks&flexible=event;cdlbull;cdl_bu3ws",
    "screen=bullish_advance_block&picker=candlesticks&flexible=event;cdlbull;cdl_buab",
    "screen=long_black_line&picker=candlesticks&flexible=event;cdlbear;cdl_lobl",
    "screen=hanging_man&picker=candlesticks&flexible=event;cdlbear;cdl_hama",
    "screen=dark_cloud_cover&picker=candlesticks&flexible=event;cdlbear;cdl_dacc",
    "screen=bearish_engulfing_lines&picker=candlesticks&flexible=event;cdlbear;cdl_beel",
    "screen=evening_star&picker=candlesticks&flexible=event;cdlbear;cdl_evst",
    "screen=doji_star&picker=candlesticks&flexible=event;cdlbear;cdl_djst",
    "screen=bearish_kicker&picker=candlesticks&flexible=event;cdlbear;cdl_bek",
    "screen=bearish_harami&picker=candlesticks&flexible=event;cdlbear;cdl_beh",
    "screen=shooting_star&picker=candlesticks&flexible=event;cdlbear;cdl_shst",
    "screen=gravestone_doji&picker=candlesticks&flexible=event;cdlmisc;cdl_grdj",
    "screen=abandoned_baby_top&picker=candlesticks&flexible=event;cdlmisc;cdl_abbt",
    "screen=bearish_counter_attack&picker=candlesticks&flexible=event;cdlbear;cdl_beca",
    "screen=bearish_three_white_soldiers&picker=candlesticks&flexible=event;cdlbear;cdl_be3ws",
    "screen=bearish_advance_block&picker=candlesticks&flexible=event;cdlbear;cdl_beab",
    "screen=bullish_marubozu&picker=candlesticks&flexible=event;cdlbull;cdl_buma",
    "screen=bullish_hikkake&picker=candlesticks&flexible=event;cdlbull;cdl_buhi",
    "screen=pivot_point_bullish_reversal&picker=reversals&flexible=event;rev;rev_ppbu",
    "screen=pivot_point_bearish_reversal&picker=reversals&flexible=event;rev;rev_ppbe",
    "screen=pivot_point_bullish_reversal_x2&picker=reversals&flexible=event;rev;rev_ppbu2",
    "screen=pivot_point_bearish_reversal_x2&picker=reversals&flexible=event;rev;rev_ppbe2",
    "screen=bullish_key_reversal&picker=reversals&flexible=event;rev;rev_keybu",
    "screen=bearish_key_reversal&picker=reversals&flexible=event;rev;rev_keybe",
    "screen=bullish_island_reversal&picker=reversals&flexible=event;rev;rev_isbu",
    "screen=bearish_island_reversal&picker=reversals&flexible=event;rev;rev_isbe",
    "screen=bullish_hook_reversal&picker=reversals&flexible=event;rev;rev_hobu",
    "screen=bearish_hook_reversal&picker=reversals&flexible=event;rev;rev_hobe",
    "screen=closing_price_bullish_reversal&picker=reversals&flexible=event;rev;rev_cbu",
    "screen=closing_price_bearish_reversal&picker=reversals&flexible=event;rev;rev_cbe",
    "screen=obullish_reversal&picker=reversals&flexible=event;rev;rev_ocbu",
    "screen=obearish_reversal&picker=reversals&flexible=event;rev;rev_ocbe",
    "screen=heikin_ashi_new_green_candle&picker=heikin_ashi&flexible=series;ha;newgreen",
    "screen=heikin_ashi_new_red_candle&picker=heikin_ashi&flexible=series;ha;newred",
    "screen=heikin_ashi_long_green_candle&picker=heikin_ashi&flexible=series;ha;longgreen",
    "screen=heikin_ashi_long_red_candle&picker=heikin_ashi&flexible=series;ha;longred",
    "screen=heikin_ashi_green_trend&picker=heikin_ashi&flexible=series;ha;greentrend",
    "screen=heikin_ashi_red_trend&picker=heikin_ashi&flexible=series;ha;redtrend",
    "screen=heikin_ashi_candle_without_wick&picker=heikin_ashi&flexible=series;ha;nowick",
    "screen=heikin_ashi_candle_without_tail&picker=heikin_ashi&flexible=series;ha;notail",
    "screen=heikin_ashi_long_wick_candle&picker=heikin_ashi&flexible=series;ha;longwick",
    "screen=heikin_ashi_long_tail_candle&picker=heikin_ashi&flexible=series;ha;longtail",
    "screen=heikin_ashi_crossed_above_sma7&picker=heikin_ashi&flexible=price;haprice;ca;sma;7",
    "screen=heikin_ashi_crossed_above_sma50&picker=heikin_ashi&flexible=price;haprice;ca;sma;50",
    "screen=heikin_ashi_crossed_above_sma200&picker=heikin_ashi&flexible=price;haprice;ca;sma;200",
    "screen=heikin_ashi_crossed_below_sma7&picker=heikin_ashi&flexible=price;haprice;cb;sma;7",
    "screen=heikin_ashi_crossed_below_sma50&picker=heikin_ashi&flexible=price;haprice;cb;sma;50",
    "screen=heikin_ashi_crossed_below_sma200&picker=heikin_ashi&flexible=price;haprice;cb;sma;200",
    "screen=renko_white_trend&picker=renko_chart_patterns&technicals=4003",
    "screen=renko_black_trend&picker=renko_chart_patterns&technicals=4007",
    "screen=renko_turnaround_white_brick&picker=renko_chart_patterns&technicals=4001",
    "screen=renko_turnaround_black_brick&picker=renko_chart_patterns&technicals=4005",
    "screen=renko_double_top&picker=renko_chart_patterns&technicals=4011",
    "screen=renko_double_bottom&picker=renko_chart_patterns&technicals=4009",
    "screen=renko_head_and_shoulders&picker=renko_chart_patterns&technicals=4013",
    "screen=renko_inverted_head_and_shoulders&picker=renko_chart_patterns&technicals=4015",
    "screen=renko_triple_bottom&picker=renko_chart_patterns&technicals=4017",
    "screen=renko_triple_top&picker=renko_chart_patterns&technicals=4019",
    "screen=renko_ascending_triangle_breakout&picker=renko_chart_patterns&technicals=4021",
    "screen=renko_descending_triangle_breakout&picker=renko_chart_patterns&technicals=4023",
    "screen=renko_symmetrical_triangle_bullish_breakout&picker=renko_chart_patterns&technicals=4025",
    "screen=renko_symmetrical_triangle_bearish_breakout&picker=renko_chart_patterns&technicals=4027",
    "screen=pf_buy&picker=point_and_figure_patterns&technicals=1201",
    "screen=pf_sell&picker=point_and_figure_patterns&technicals=1203",
    "screen=double_bottom&picker=point_and_figure_patterns&technicals=1205",
    "screen=double_top&picker=point_and_figure_patterns&technicals=1207",
    "screen=triple_bottom&picker=point_and_figure_patterns&technicals=1209",
    "screen=triple_top&picker=point_and_figure_patterns&technicals=1211",
    "screen=bullish_catapult&picker=point_and_figure_patterns&technicals=1213",
    "screen=bearish_catapult&picker=point_and_figure_patterns&technicals=1215",
    "screen=inverted_head_and_shoulders&picker=point_and_figure_patterns&technicals=1217",
    "screen=head_and_shoulders&picker=point_and_figure_patterns&technicals=1219",
    "screen=ascending_triangle_breakout&picker=point_and_figure_patterns&technicals=1221",
    "screen=descending_triangle_breakout&picker=point_and_figure_patterns&technicals=1223",
    "screen=symmetrical_triangle_bullish_breakout&picker=point_and_figure_patterns&technicals=1225",
    "screen=symmetrical_triangle_bearish_breakout&picker=point_and_figure_patterns&technicals=1227",
    "screen=long_tail_down_reversal&picker=point_and_figure_patterns&technicals=1229",
    "screen=long_tail_up_reversal&picker=point_and_figure_patterns&technicals=1231",
    "screen=bear_trap&picker=point_and_figure_patterns&technicals=1233",
    "screen=bull_trap&picker=point_and_figure_patterns&technicals=1235",
    "screen=zigzg10_double_bottom&picker=zigzag_patterns&technicals=8901",
    "screen=zigzg10_double_top&picker=zigzag_patterns&technicals=8903",
    "screen=zigzg10_triple_bottom&picker=zigzag_patterns&technicals=8905",
    "screen=zigzg10_triple_top&picker=zigzag_patterns&technicals=8907",
    "screen=zigzg10_head_and_shoulders&picker=zigzag_patterns&technicals=8909",
    "screen=zigzg10_inverted_head_and_shoulders&picker=zigzag_patterns&technicals=8911",
    "screen=zigzg10_ascending_triangle&picker=zigzag_patterns&technicals=8913",
    "screen=zigzg10_descending_triangle&picker=zigzag_patterns&technicals=8915",
    "screen=zigzg10_ascending_triangle_breakout&picker=zigzag_patterns&technicals=8917",
    "screen=zigzg10_descending_triangle_breakout&picker=zigzag_patterns&technicals=8919",
    "screen=elliot_5_upward_impulses_and_3_correction_waves_pattern&picker=zigzag_patterns&technicals=8921",
    "screen=elliot_5_downward_impulses_and_3_correction_waves_pattern&picker=zigzag_patterns&technicals=8923",
    "screen=elliot_5_upward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8925",
    "screen=elliot_5_downward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8927",
    "screen=elliot_4_upward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8929",
    "screen=elliot_4_downward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8931",
    "screen=elliot_3_upward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8933",
    "screen=elliot_3_downward_impulse_waves_pattern&picker=zigzag_patterns&technicals=8935",
    "screen=inside_day&picker=toby_crabel&flexible=event;crabel;inside_day",
    "screen=narrow_range&picker=toby_crabel&flexible=event;crabel;narrow_range",
    "screen=wide_spread&picker=toby_crabel&flexible=event;crabel;wide_spread",
    "screen=nr4&picker=toby_crabel&flexible=event;crabel;nr4",
    "screen=nr7&picker=toby_crabel&flexible=event;crabel;nr7",
    "screen=ws4&picker=toby_crabel&flexible=event;crabel;ws4",
    "screen=ws7&picker=toby_crabel&flexible=event;crabel;ws7",
    "screen=2bar_nr&picker=toby_crabel&flexible=event;crabel;c2bar_nr",
    "screen=3bar_nr&picker=toby_crabel&flexible=event;crabel;c3bar_nr",
    "screen=upthrust&picker=toby_crabel&flexible=event;crabel;upthrust",
    "screen=spring&picker=toby_crabel&flexible=event;crabel;spring",
    "screen=bull_hook&picker=toby_crabel&flexible=event;crabel;bull_hook",
    "screen=bear_hook&picker=toby_crabel&flexible=event;crabel;bear_hook"
]

def SyncMarketIOCookie(HEADER) -> dict[str, str]:
    URL=fr"https://www.marketinout.com"
    RESULT=httpx.get(URL, headers=HEADER)
    COOKIE={C[0]:C[1] for C in RESULT.cookies.items()}

    return COOKIE

async def AsyncMarketIOPattern(CLIENT, SEMAPHORE, PATTERN) -> pd.DataFrame:
    URL=fr"https://www.marketinout.com/stock-screener/stocks.php?{PATTERN}&view=tech&exch=15"
    PATTERNNAME="".join(parse.parse_qs(PATTERN)["screen"][0].title().split("_"))
    PATTERNTYPE="".join(parse.parse_qs(PATTERN)["picker"][0].title().split("_"))
    async with SEMAPHORE:
        RESULT=await CLIENT.get(URL)
    
    print(PATTERNTYPE, PATTERNNAME)

    DF=pd.read_html(io.BytesIO(RESULT.content), match="Symbol")[0].iloc[:-3]
    if(len(DF)==0):
        DF=pd.DataFrame(columns=['SYMBOL', "PATTERN", 'LTP', 'CHANGE', 'RSI14', 'ATR14'])
        return DF
    DF["Symbol"]=DF["Symbol"].str.split(".").str[0]
    DF["Pattern"]=PATTERNNAME
    DF["Type"]=PATTERNTYPE
    DF=DF[["Symbol", "Pattern", "Last", "Open", "High", "Low", "Change", "RSI(14)", "ATR(14)", "Type"]]
    DF[["Last", "Open", "High", "Low", "Change", "RSI(14)", "ATR(14)"]]=DF[["Last", "Open", "High", "Low", "Change", "RSI(14)", "ATR(14)"]].astype(np.float64)
    DF.columns=['SYMBOL', "PATTERN", 'LTP', "OPEN", "HIGH", "LOW", 'CHANGE', 'RSI14', 'ATR14', 'TYPE']

    return DF

async def AsyncMarketIOPatternWrapper(HEADER, COOKIE) -> pd.DataFrame:
    CLIENT=httpx.AsyncClient(headers=HEADER, cookies=COOKIE)
    SEMAPHORE=asyncio.Semaphore(7)

    APOOL=[asyncio.create_task(AsyncMarketIOPattern(CLIENT, SEMAPHORE, PATTERN)) for PATTERN in PATTERNLIST]

    RESULT=await asyncio.gather(*APOOL)

    return RESULT

if __name__=="__main__":
    print("\x1b[31m\x1b[1mYou wouldn't do that, Specifically!\x1b[0m")