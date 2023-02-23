import openai

def GetResponse(prompt, addedContext = "", AddAtTheStart = True):
    openAIKey = ""

    openai.api_key = openAIKey

    model_engine = "text-davinci-003"
    print("in function")
    # If context, add it
    if addedContext != "":
        print("adding context")
        if AddAtTheStart:
            prompt = addedContext + prompt
        else:
            prompt = prompt + addedContext

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