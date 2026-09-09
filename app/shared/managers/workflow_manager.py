from app.events.event_bus import event_bus


class WorkflowManager:

    @staticmethod
    async def publish(
        event_type,
        payload
    ):  


        print('+++\n' *5)
        print("We are into WorkflowManager", event_type)
        print(payload)
        print('+++\n' *5)

        await event_bus.publish(
            event_type,
            payload
        )