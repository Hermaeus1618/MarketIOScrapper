import asyncio
import pandas as pd

from marketiolib import SyncMarketIOCookie, AsyncMarketIOPatternWrapper

HEADER={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
COOKIE=SyncMarketIOCookie(HEADER)

RESULT=asyncio.run(AsyncMarketIOPatternWrapper(HEADER, COOKIE))
RESULT=[R for R in RESULT if len(R)>0]

DF=pd.concat(RESULT)

TYPELIST=pd.Series(DF["TYPE"]).unique().tolist()
with pd.ExcelWriter("Pattern.xlsx") as WRITER:
    for TYPE in TYPELIST:
        DF[DF["TYPE"]==TYPE].drop(["TYPE"], axis=1).to_excel(WRITER, sheet_name=TYPE, index=False)
        WRITER.book.sheetnames[TYPE].autofit()
