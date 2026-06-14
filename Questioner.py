from abc import ABC, abstractmethod
import numpy as np
from utils import GeminiLLM, ClientBasedLLM
from retrying import retry
import time
import re


_GEMINI_ASK_QUESTION_PROMPT_CONCLUSION = (
    "An oracle has a fixed target image and has given you this description of the object in the target image: {TASK_DESCRIPTION}. "
    "You are given the above image, which may or may not picturing the same object as the target image owned by the oracle. Your goal is to decide whether the "
    "image that you see corresponds to the same image target image owned by the oracle. "
    "Use, to guide your decision, the description of the object, the give image, and, if they exists, the questions that you previously asked to the oracle "
    "and the associated answers. Provide a reasoning about your conclusion, or why you are uncertain and asked a question. "
    "If you are sure that the two image match, return the score 2, if you are sure that they don't match, return "
    "the score 0. If you are unsure either way, return the score 1 and ask an informative question to the oracle about what it might appears in the target image, "
    "to dispel your doubts. You can always trust the oracle's answers and the initial description. Do not ask questions that can be directly answered by "
    "reading the initial description, or questions about the image that you are provided. Be careful: the target image and the given image might differ only in some small details, "
    "like the color of the object, its texture, or the presence of other objects. For example, the target image might picture a bed with a blue comforter, "
    "and the given image a bed with a red comforter, or a blue bed but with a white comforter. "
    "The image might have distortions or digital artifacts: *NEVER* mention them in the question. Prefer asking question if the description is very generic. "
    "Strictly follow this output format: "
    "<motivation>Your reasoning here (under 60 words, do NOT use double quotes \")</motivation><score>0, 1, or 2</score><question>Your question or '' (if score is not 1)</question>"
)


_FOLLOW_TEMPLATE_PROMPT = "Strictly follow this output format: <motivation>Your reasoning here</motivation><score>0, 1, or 2</score><question>Your question or None (if score is not 1)</question>"


def _validate_observation(observation):
    assert isinstance(observation["image"], np.ndarray) and (
        not observation["answer"] or isinstance(observation["answer"], str)
    ), (
        "Wrong observation format: it must be a dictionary with keys 'image' and 'answer', where 'answer' is a numpy array and 'answer' is either a string or None"
    )
    assert (
        len(observation["image"].shape) == 3 and observation["image"].shape[2] == 3
    ), "Wrong image format: must be a numpy array of shape (H,W,3) --- an rgb image."


class QuestionerInterface(ABC):
    """Abstract Questioner class. Your questioner should inherit from this."""

    def __init__(self, info, *args):
        self.info = info  # required info like the task description

    @abstractmethod
    def ask_or_conclude(self, observation):
        # TODO: this is what you have to implement
        pass

    def add_answer(self, answer):
        self.answers.append(answer)

    def reset_questions(self):
        self.questions = []
        self.answers = []

    def reset_time(self):
        self.time_required = 0


class QuestionerGemini(QuestionerInterface):
    """Questioner example: a wrapper over the Gemini API, keeping track of previous interactions"""

    def __init__(self, info, client: GeminiLLM):
        super().__init__(info)
        self.client = client
        self.questions = []
        self.reasonings = []
        self.answers = []
        self.time_required = 0
        self.n_questions = 0

    @retry(
        stop_max_attempt_number=5,
        wait_exponential_multiplier=2000,
        wait_exponential_max=60000,
    )
    def ask_or_conclude(self, observation):
        _validate_observation(observation)
        start_time = time.time()
        prev_questions = ""
        if len(self.questions) > 0:
            prev_questions = "\nPreviously you asked the following questions, which received the associated answers:\n"
            for j, q in enumerate(self.questions[-16:]):
                prev_questions += f"'{q} <|answer|>{self.answers[j]}<|answer|>'\n"
        else:
            prev_questions = "\nThere are no previous questions or answers.\n"
        # Failsafe
        if len(self.questions) >= 16:
            return dict(question=None, conclusion=0, reasoning="")

        prompt_to_use = _GEMINI_ASK_QUESTION_PROMPT_CONCLUSION
        prompt_to_use = (
            prompt_to_use.format(TASK_DESCRIPTION=self.info["task_description"])
            + prev_questions
            + _FOLLOW_TEMPLATE_PROMPT
        )
        # Ask API to ask a question or conclude
        response = self.client.ask(
            prompt=prompt_to_use,
            images=[observation["image"]],
        )

        end_time = time.time()
        self.time_required += end_time - start_time
        try:
            question = re.findall("<question>(.*?)<\\/question>", response)[0]
            reasoning = (
                re.findall(
                    "<motivation>(.*?)<\\/motivation>",
                    response,
                )[0]
                .removeprefix("<motivation>")
                .removesuffix("</motivation>")
            )
            self.reasonings.append(reasoning)

            if len(question) > 0 and question.lower() != "none" and question != "''":
                question = question.removeprefix("<question>").removesuffix(
                    "</question>"
                )
                self.questions.append(question)
                self.n_questions += 1
                # When it asks a question, it is uncertain so the conclusion is None and the question is filled out
                return dict(question=question, conclusion=None, reasoning=reasoning)
            score = (
                re.findall("<score>[\\d]+<\\/score>", response)[0]
                .removeprefix("<score>")
                .removesuffix("</score>")
            )
            # We have mapped 2 to certainty of being a match (therefore the conclusion will be true/1), with no question
            # and 0 to certainty of being NOT a match (therefore the conclusion will be false/0), with no question
            if int(score) == 2:
                return dict(question=None, conclusion=1, reasoning=reasoning)
            elif int(score) == 0:
                return dict(question=None, conclusion=0, reasoning=reasoning)
            else:
                raise ValueError
        except Exception as e:
            print(e)
            raise


class QuestionerLocal(QuestionerInterface):
    def __init__(self, info, client: ClientBasedLLM):
        super().__init__(info)
        self.client = client
        self.questions = []
        self.reasonings = []
        self.answers = []
        self.time_required = 0
        self.n_questions = 0

    @retry(
        stop_max_attempt_number=5,
        wait_exponential_multiplier=2000,
        wait_exponential_max=60000,
    )
    def ask_or_conclude(self, observation):
        _validate_observation(observation)
        start_time = time.time()

        # Define `prompt_to_use and other stuff here
        prompt_to_use = "TODO"  # TODO
        # ...

        response = self.client.ask(
            prompt=prompt_to_use,
            images=[observation["image"]],
        )

        end_time = time.time()

        # Parse and return a question or a conclusion


class YourQuestioner(QuestionerInterface):
    def __init__(self, info, *args):
        super().__init__(info)
        # TODO

    def ask_or_conclude(self, observation):
        _validate_observation(observation)
        # TODO
        ## Return either (if uncertain whether the observation corresponds to the target description or not)
        # return dict(question=question, conclusion=None, reasoning=reasoning)
        ## if certain that is a match
        # return dict(question=None, conclusion=1, reasoning=reasoning)
        ## or if certaint that is NOT a match
        # return dict(question=None, conclusion=0, reasoning=reasoning)
