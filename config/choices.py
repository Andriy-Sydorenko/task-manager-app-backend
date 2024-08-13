from django.db import models


class OpenAIEngines(models.TextChoices):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    TEXT_DAVINCI_3 = "text-davinci-003"
    TEXT_CURIE_1 = "text-curie-001"
    TEXT_BABBAGE_001 = "text-babbage-001"
    TEXT_ADA_001 = "text-ada-001"
