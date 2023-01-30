# ChatGPT skill

When in doubt, ask chatgpt

You need to configure an api_key, get it at https://beta.openai.com/account/api-keys


## About 

ChatGPT skill

Capabilities:
- Remembers what user said earlier in the conversation
- Allows user to provide follow-up corrections
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings you can tweak some parameters for chatGPT


- `key` - your api_key to access OpenAI
- `initial_prompt` - can be used to create a "persona", give a personality to chatGPT
- `memory` - remember previous conversations (since loading), default `true`
- TODO - all request params will be exposed in the future, default values are
      `engine="davinci", temperature=0.85, 
      top_p=1, frequency_penalty=0,
      presence_penalty=0.7, best_of=2, 
      max_tokens=100`


The default initial prompt is

```
The assistant is helpful, creative, clever, and very friendly.
```

Check out [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) for ideas


## Examples 

* "Explain quantum computing in simple terms"
* "Got any creative ideas for a 10 year old’s birthday?"
