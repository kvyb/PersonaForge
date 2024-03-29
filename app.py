#!/usr/bin/env python3
import argparse
import logging
import typing as t
import gradio as gr

from gradio_ui import build_gradio_ui_for
from parsing import parse_messages_from_str
from prompting import build_prompt_for
from utils import clear_stdout

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# For UI debugging purposes.
DONT_USE_MODEL = False


def main(model_name: t.Optional[str]):

    if model_name and not DONT_USE_MODEL:
        from model import build_model_and_tokenizer_for, run_raw_inference
        model, tokenizer = build_model_and_tokenizer_for(model_name)
    else:
        model, tokenizer = None, None
    
    def inference_fn(history: t.List[str], user_input: str,
                     generation_settings: t.Dict[str, t.Any],
                     *char_settings: t.Any) -> str:
        if DONT_USE_MODEL:
            return "Mock response for UI tests."
        
        
        # Brittle. Comes from the order defined in gradio_ui.py.
        [
            char_name,
            _user_name,
            char_persona,
            char_greeting,
            world_scenario,
            example_dialogue,
        ] = char_settings

        # If we're just starting the conversation and the character has a greeting
        # configured, return that instead. This is a workaround for the fact that
        # Gradio assumed that a chatbot cannot possibly start a conversation, so we
        # can't just have the greeting there automatically, it needs to be in
        # response to a user message.
        if len(history) == 0 and char_greeting is not None:
            return f"{char_name}: {char_greeting}"

        prompt = build_prompt_for(history=history,
                                  user_message=user_input,
                                  char_name=char_name,
                                  char_persona=char_persona,
                                  example_dialogue=example_dialogue,
                                  world_scenario=world_scenario)

        if model and tokenizer:
            model_output = run_raw_inference(model, tokenizer, prompt,
                                             user_input, **generation_settings)
        else:
            raise Exception(
                "Not using local inference, but no Kobold instance URL was"
                " given. Nowhere to perform inference on.")

        generated_messages = parse_messages_from_str(model_output,
                                                     ["You", char_name])
        logger.debug("Parsed model response is: `%s`", generated_messages)
        bot_message = generated_messages[0]
        return bot_message
    ui = build_gradio_ui_for(inference_fn)
    # Auth does not work on http?? TODO: open an issue on github regardign auth on VM's exposed to internet
    # ui.queue(concurrency_count=2).launch(auth=[("admin","password"),("user","password")], server_name="10.186.0.4")
    # Set server_name to 0.0.0.0 or server internal IP
    ui.queue(concurrency_count=2).launch(server_name="10.186.0.4")

if __name__ == "__main__":
    main(model_name='PygmalionAI/pygmalion-6b')
