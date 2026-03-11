from fastapi import APIRouter, WebSocket
import asyncio

router = APIRouter()

@router.websocket("/ws/terminal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # This is a placeholder for a real terminal process
    process = await asyncio.create_subprocess_shell(
        "bash",
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def read_from_socket():
        while True:
            data = await websocket.receive_text()
            if process.stdin:
                process.stdin.write(data.encode())
                await process.stdin.drain()

    async def write_to_socket():
        while True:
            if process.stdout:
                data = await process.stdout.read(1024)
                if data:
                    await websocket.send_text(data.decode())
            if process.stderr:
                data = await process.stderr.read(1024)
                if data:
                    await websocket.send_text(data.decode())
            await asyncio.sleep(0.01)

    read_task = asyncio.create_task(read_from_socket())
    write_task = asyncio.create_task(write_to_socket())

    try:
        await asyncio.gather(read_task, write_task)
    except Exception as e:
        print(f"Terminal WebSocket error: {e}")
    finally:
        read_task.cancel()
        write_task.cancel()
        process.kill()
        await process.wait()
        await websocket.close()
