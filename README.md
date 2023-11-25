# ChatGPT Fallback Skill

When in doubt, ask chatgpt, powered by [OpenAI Solver](https://github.com/OpenVoiceOS/ovos-solver-plugin-openai-persona)

You need to configure an api_key, get it at https://beta.openai.com/account/api-keys


## About 

Capabilities:
- Remembers what user said earlier in the conversation
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings you can tweak some parameters for chatGPT


- `key` - your api_key to access OpenAI
- `persona` - can be used to create a "persona", give a personality to chatGPT
- `model` - LLM model to use, eg `"gpt-3.5-turbo", see all options [here](https://platform.openai.com/docs/models)

The default persona is `helpful, creative, clever, and very friendly.`


## Examples 

* "Explain quantum computing in simple terms"
* "Got any creative ideas for a 10 year old’s birthday?"
