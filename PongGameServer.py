from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
import random

app = FastAPI()

class PongGame:
    def __init__(self):
        self.ball_x = 400
        self.ball_y = 300
        self.ball_dx = 5
        self.ball_dy = 5
        self.paddle1_y = 250  # ผู้เล่น 1 (ซ้าย)
        self.paddle2_y = 250  # ผู้เล่น 2 (ขวา)
        self.score1 = 0
        self.score2 = 0

    def update(self):
        # อัปเดตตำแหน่งลูกบอล
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # ชนขอบบน-ล่าง
        if self.ball_y <= 0 or self.ball_y >= 600:
            self.ball_dy *= -1

        # ชนไม้ซ้าย
        if self.ball_x <= 20 and self.paddle1_y <= self.ball_y <= self.paddle1_y + 100:
            self.ball_dx *= -1
            self.ball_x = 21
        # ชนไม้ขวา
        elif self.ball_x >= 780 and self.paddle2_y <= self.ball_y <= self.paddle2_y + 100:
            self.ball_dx *= -1
            self.ball_x = 779

        # ทำคะแนน
        if self.ball_x < 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball_x > 800:
            self.score1 += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball_x = 400
        self.ball_y = 300
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = random.choice([-5, 5])

game = PongGame()

@app.websocket("/ws/pong")
async def pong_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Task สำหรับ Game Loop
    async def game_loop():
        while True:
            game.update()
            await websocket.send_text(json.dumps({
                "ball_x": game.ball_x, "ball_y": game.ball_y,
                "paddle1_y": game.paddle1_y, "paddle2_y": game.paddle2_y,
                "score1": game.score1, "score2": game.score2
            }))
            await asyncio.sleep(1/60) # 60 FPS

    loop_task = asyncio.create_task(game_loop())

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # รับตำแหน่งไม้จาก Client
            if message.get("type") == "move":
                if message["player"] == 1:
                    game.paddle1_y = message["y"]
                elif message["player"] == 2:
                    game.paddle2_y = message["y"]
    except WebSocketDisconnect:
        loop_task.cancel()
        print("Pong Client Disconnected")