# ChatGPT Fallback Skill

When in doubt, ask ChatGPT, powered by [OpenAI Solver](https://github.com/OpenVoiceOS/ovos-solver-plugin-openai-persona).

You need to configure a `key`, get it at https://platform.openai.com/api-keys

Or use a LocalAI (see example below)


## About

Capabilities:

- Remembers what user said earlier in the conversation
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings (`.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json`) you can tweak some parameters for chatGPT.
- `key` - your api_key to access OpenAI
- `persona` - can be used to create a "persona", give a personality to chatGPT
- `model` - LLM model to use, eg `gpt-3.5-turbo`, see all options [here](https://platform.openai.com/docs/models)
- `api_url: <your_local_LocalAI_server_url>` - an optional setting. For the use of OpenAI / ChatGPT it is not necessary. For the use of a LocalAI server instead of OpenAI, the URL can be pointed to an alternative/local server. When using LocalAI, the "key" can be anything, but it has to exist. Read more about it in the OVOS technical manual, page [persona server](https://openvoiceos.github.io/ovos-technical-manual/persona_server/#compatible-projects)
- `memory_enable` - true or false
- `memory_size` - default = 15


The default persona is `helpful, creative, clever, and very friendly.`

### Example for use with OpenAI/ ChatGPT:

`cat ~/.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json`

```
{
  "key": "sk-XXXYYYZZZAAABBB123",
  "model": "gpt-3.5-turbo",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor",
  "enable_memory": true,
  "memory_size": 15,
  "__mycroft_skill_firstrun": false
}
```

### Example for use with LocalAI:
`cat ~/.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json`

```
{
  "api_url": "https://llama.smartgic.io/v1",
  "key": "sk-xxx",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor",
  "enable_memory": true,
  "memory_size": 15,
  "__mycroft_skill_firstrun": false
}
```


## Examples

- "Explain quantum computing in simple terms"
- "Got any creative ideas for a 10 year old’s birthday?"
