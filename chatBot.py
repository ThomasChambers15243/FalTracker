import openai
import consts

# https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md

### Gets a response from from openAI with a given promt. Includes moderation. Context can be given at the front or end of the promt.
### Returns a string of the response
def GetResponse(prompt, addedContext = "", AddAtTheStart = True):
    openai.api_key = consts.openAIKey

    model_engine = "text-davinci-003"
    print("in function")
    # If context, add it
    if addedContext != "":
        print("adding context")
        if AddAtTheStart:
            prompt = addedContext + prompt
        else:
            prompt = prompt + addedContext

    # Moderate input
    moderatedPrompt = openai.Moderation.create(
        input = prompt
    )

    if moderatedPrompt["results"][0].flagged == True:
        return "You prompt has flagged the Bot's moderation filter.\n" \
               "If this seems wrong, please try rephrasing the question.\n" \
               "If it isn't wrong...come on, be nicer"

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("Got response")
    # Get response
    response = completion.choices[0].text

    return response