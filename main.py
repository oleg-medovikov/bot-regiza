"""
Этот бот написан для выгрузки случаев токсилогических
отравлений. Передача формы №58
от МО в РПН и ЦГИЭ
Автор: Медовиков Олег
2023
"""

import warnings
import asyncio

from disp import dp, on_startup
from shed import scheduler

warnings.filterwarnings("ignore")


async def main():
    await asyncio.gather(
        on_startup(dp),
        scheduler(),
        )


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            break
        except:
            continue
