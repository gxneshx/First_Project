from openai import OpenAI
import httpx as httpx, base64


class ChatGptService:
    client: OpenAI = None
    message_list: list = None

    def __init__(self, token):
        token = "sk-proj-" + token[:3:-1] if token.startswith('gpt:') else token
        self.client = OpenAI(
            http_client=httpx.Client(),
            api_key=token)
        self.message_list = []

    # The function to fetch text from an audio file
    async def speech_to_text(self, path, client) -> str:
        audio_file = open(path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcription

    # The function to convert text to audio
    async def text_to_speech(self, text: str, client) -> None:
        # path = Path(__file__).parent / "answer.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file("answer.mp3")

    async def recognize_image(self, path, client) -> str:
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        base64_image = encode_image(path)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Що на цьому зображенні?",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    async def send_message_list(self) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # gpt-4o,  gpt-4-turbo,  gpt-3.5-turbo,  gpt-4o-mini - the best for transcriptions
            messages=self.message_list,
            max_tokens=3000,
            temperature=0.9
        )
        message = completion.choices[0].message
        self.message_list.append(message)
        return message.content

    def set_prompt(self, prompt_text: str) -> None:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})

    async def add_message(self, message_text: str) -> str:
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()
