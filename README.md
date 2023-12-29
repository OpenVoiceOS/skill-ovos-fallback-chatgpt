# ChatGPT Fallback Skill

When in doubt, ask ChatGPT, powered by [OpenAI Solver](https://github.com/OpenVoiceOS/ovos-solver-plugin-openai-persona).

You need to configure a `key`, get it at https://platform.openai.com/api-keys

## About

Capabilities:

- Remembers what user said earlier in the conversation
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings you can tweak some parameters for chatGPT.

- `key` - your api_key to access OpenAI
- `persona` - can be used to create a "persona", give a personality to chatGPT
- `model` - LLM model to use, eg `gpt-3.5-turbo`, see all options [here](https://platform.openai.com/docs/models)

The default persona is `helpful, creative, clever, and very friendly.`

```shell
mkdir -p ~/.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos
cat <<EOF>~/.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json
{
  "key": "sk-XXXYYYZZZAAABBB123",
  "model": "gpt-3.5-turbo",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor",
  "__mycroft_skill_firstrun": false
}
EOF
```

## Examples

- "Explain quantum computing in simple terms"
- "Got any creative ideas for a 10 year old’s birthday?"
