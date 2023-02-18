import asyncio


def timeout(sec, handler):
    def decorator(func):
        async def wrappers(*args, **kwargs):
            state = kwargs["state"]
            await func(args[0], state)
            current_state = await state.get_state()
            await asyncio.sleep(sec)
            if current_state == await state.get_state():
                await state.reset_state()
                await handler(*args, state)
        return wrappers
    return decorator
