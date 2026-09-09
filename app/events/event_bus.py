import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Callable
from typing import Dict
from typing import List



class EventBus:

    def __init__(self):

        self.handlers: Dict[str, List[Callable]] = defaultdict(list)

    # =========================
    # REGISTER HANDLER
    # =========================

    def subscribe( self, event_name: str, handler: Callable ):

        self.handlers[event_name].append(handler)



    # =========================
    # PUBLISH EVENT
    # =========================

    async def publish( self, event_name: str, payload: dict ):

        print('+++\n' *5)
        print("We are into EventBus puplish method")
        print("event_name", event_name)
        print("self.handlers", self.handlers)
        print('+++\n' *5)
        if event_name not in self.handlers:
            return

        event = {
            "event": event_name,
            "timestamp": datetime.utcnow().isoformat(),
            **payload
        }

        tasks = []


        for handler in self.handlers[event_name]:
            tasks.append(self._safe_execute( handler, event ))

        print('+++\n' *5)
        print("We are into EventBus puplish method")
        print("Tasks", tasks)
        print('+++\n' *5)
        await asyncio.gather(*tasks)

    # =========================
    # SAFE HANDLER EXECUTION
    # =========================

    async def _safe_execute(
        self,
        handler,
        payload
    ):

        try:

            await handler(payload)

        except Exception as e:

            print(
                f"Event handler failed "
                f"{handler.__name__}: {e}"
            )


event_bus = EventBus()