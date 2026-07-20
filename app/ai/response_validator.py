from __future__ import annotations


class ResponseValidator:
    """
    Valida e normaliza as respostas produzidas pelo Qwen.

    Garante que cada prompt retorne sempre a estrutura esperada.
    """

    DEFAULTS = {
        "header": {},
        "employees": {"employees": []},
        "activities": {"activities": []},
        "observations": {"observacoes": []},
        "signatures": {"assinaturas": []},
        "attendance": {"employees": []},
        "photos": {"photos": []},
        "captions": {"captions": []},
        "layout": {"layout": "unknown"},
        "document": {},
    }

    def validate(self, prompt: str, data):

        if data is None:
            return self.DEFAULTS.get(prompt, {})

        if isinstance(data, list):

            if prompt == "employees":
                return {"employees": data}

            if prompt == "activities":
                return {"activities": data}

            return {"items": data}

        if not isinstance(data, dict):
            return self.DEFAULTS.get(prompt, {})

        if prompt == "employees":
            data.setdefault("employees", [])

        elif prompt == "activities":
            data.setdefault("activities", [])

        elif prompt == "observations":
            data.setdefault("observacoes", [])

        elif prompt == "signatures":
            data.setdefault("assinaturas", [])

        elif prompt == "attendance":
            data.setdefault("employees", [])

        elif prompt == "photos":
            data.setdefault("photos", [])

        elif prompt == "captions":
            data.setdefault("captions", [])

        elif prompt == "layout":
            data.setdefault("layout", "unknown")

        return data