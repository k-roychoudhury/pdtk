r""" test.scripts.test_async_network_interface module """


# importing standard modules ==================================================
import asyncio, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# importing third-party modules ===============================================
import aiohttp


# importing custom modules ====================================================
from py_google_patents.network import AsyncNetworkInterface


# main ========================================================================
async def main() -> None:

    async with aiohttp.ClientSession() as session:

        google_network_client: AsyncNetworkInterface = \
            AsyncNetworkInterface(session)
        
        # result1 = await google_network_client.getResult(
        #     "patent/US9145048B2/en"
        # )
        result2 = await google_network_client.getParse(
            "(hybrid AND engine)"
        )

    # print(result1)
    print(result2.dict())

    return

    
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete( main() )
    