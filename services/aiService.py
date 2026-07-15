import requests
import json

class DebateConductor:
    def __init__(self):
        # We enforce local Ollama default port for maximum data privacy
        self.ollama_url = "http://localhost:11434/api/generate"
        self.debate_history = []
        #  Select a lightweight model like 'mistral' or 'llama3)'
        self.model = "mistral"

    def _format_history(self):
        """
        Turns self.debate_history (a list of {speaker, text} dicts) into a
        plain-text transcript that we can drop into a prompt. This is the
        "context memory" mechanism: instead of resetting the conversation
        every call, each agent sees everything said so far and is
        instructed to rebut it directly.
        """
        if not self.debate_history:
            return "(No arguments have been made yet. You are opening the debate.)"
 
        lines = []
        for turn in self.debate_history:
            lines.append(f"{turn['speaker']}: {turn['text']}")
        return "\n".join(lines)
    
    def _call_ollama(self, system_prompt, user_prompt):
        """
        Sends a single generation request to the local Ollama server.
        We use stream=False so Ollama returns one complete JSON object
        instead of newline-delimited JSON chunks -- this keeps parsing
        simple and avoids having to stitch together partial tokens, which
        matters more for a debate transcript (needs to be complete before
        we hand it to the ML judge) than it does for a live-typing UI.
        """
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "options": {
                # Slightly higher temperature keeps the debate from
                # sounding robotic/repetitive turn after turn.
                "temperature": 0.8
            },
        }
 
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            return (
                "[ERROR] Could not reach Ollama at "
                f"{self.ollama_url}. Is 'ollama serve' running and have "
                f"you pulled the '{self.model}' model?"
            )
        except requests.exceptions.Timeout:
            return "[ERROR] Ollama took too long to respond (timeout)."
        except requests.exceptions.HTTPError as e:
            return f"[ERROR] Ollama returned an HTTP error: {e}"
 
        try:
            data = response.json()
        except json.JSONDecodeError:
            return "[ERROR] Ollama response was not valid JSON."
 
        # Ollama's /api/generate puts the completion text in "response"
        text = data.get("response", "").strip()
        if not text:
            return "[ERROR] Ollama returned an empty response."
 
        return text

    def generate_agent_a_response(self, topic):
        """
        Agent A fiercely DEFENDS the topic.
        """
        system_prompt = (
            "You are Agent A, a sharp, confident debater who ALWAYS argues "
            f"IN FAVOR of the motion: '{topic}'. You are persuasive, "
            "assertive, and back claims with concrete reasoning or "
            "examples. You directly rebut the previous speaker's points "
            "by name before making your own. Keep responses to 2-4 "
            "sentences -- punchy, not rambling."
        )

        user_prompt = (
            f"Debate topic: {topic}\n\n"
            f"Transcript so far:\n{self._format_history()}\n\n"
            "It is now your turn. Respond as Agent A, defending the topic "
            "and countering whatever Agent B just argued (if anything)."
        )

        reply = self._call_ollama(system_prompt, user_prompt)
        self.debate_history.append({"speaker": "Agent A", "text": reply})
        return reply

    def generate_agent_b_response(self, topic):
        """
        Agent B fiercely CHALLENGES the topic.
        """

        system_prompt = (
            "You are Agent B, a skeptical, incisive debater who ALWAYS "
            f"argues AGAINST the motion: '{topic}'. You look for flaws, "
            "risks, and counterexamples in your opponent's reasoning. You "
            "directly rebut the previous speaker's points by name before "
            "making your own. Keep responses to 2-4 sentences -- punchy, "
            "not rambling."
        )
 
        user_prompt = (
            f"Debate topic: {topic}\n\n"
            f"Transcript so far:\n{self._format_history()}\n\n"
            "It is now your turn. Respond as Agent B, challenging the "
            "topic and countering whatever Agent A just argued."
        )
 
        reply = self._call_ollama(system_prompt, user_prompt)
        self.debate_history.append({"speaker": "Agent B", "text": reply})
        return reply
    
    def reset(self): # Optionally, we can add a reset method to clear the debate history
        """
        Clears the debate history so a new debate can start fresh.
        """
        self.debate_history = []
