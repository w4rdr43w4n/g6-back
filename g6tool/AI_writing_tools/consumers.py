from channels.generic.websocket import JsonWebsocketConsumer
from .Utils.ai_utils import Wiki, GPT
from .pricing import Credit


class ArticleConsumer(JsonWebsocketConsumer):
    def connect(self):
        print("********* connected to wiki ***********")
        self.accept()

    def disconnect(self, code):
        print("********* wiki is closed ***********")
        return super().disconnect(code)

    def receive_json(self, request):
        # from .models import WikiModel

        action = request.get("action")
        properties = request.get("properties")

        if action == "rewrite_page":
            try:
                page_id = properties["page_id"]
                lang = properties["lang"]
                page_preproc = {"type": "not exist"}
                page = Wiki.get_page(page_id, lang=lang)
                page_preproc = GPT.preproc_wiki_page(page)
            except Exception as e:
                self.send_json(
                    {"type": "error", "chunk": str(e.args), "status": False})

            for item in page_preproc:
                type_ = item["type"]

                match type_:
                    case "section":
                        subsec = False
                        current_section = item["chunk"]
                        item["status"] = True
                        self.send_json(item)
                        print(item)
                    case "sub_section":
                        subsec = True
                        current_subsec = item["chunk"]
                        item["status"] = True
                        self.send_json(item)
                        print(item)
                if type_ == "content":
                    try:
                        completion = GPT.rewrite_wiki_section(
                            content=item["chunk"], language=lang
                        )
                        generated = ""
                        for chunk in completion:
                            finish_reason = chunk["choices"][0]["finish_reason"]
                            if finish_reason is None:
                                generated = (
                                    generated +
                                    chunk["choices"][0]["delta"]["content"]
                                )
                                self.send_json(
                                    {
                                        "type": "content",
                                        "chunk": chunk["choices"][0]["delta"][
                                            "content"
                                        ],
                                        "status": True,
                                    }
                                )
                        # WikiModel.objects.create(
                        #     language=lang,
                        #     page_id=page_id,
                        #     section_id=current_section + " _ " + current_subsec
                        #     if subsec
                        #     else current_section,
                        #     original=item["chunk"],
                        #     generated=generated,
                        #     model="gpt-3.5-16k",
                        # )
                        subsec = False
                    except Exception as e:
                        self.send_json(
                            {"type": "error", "chunk": str(e), "status": False}
                        )
            self.send_json({"status": False})

        if action == "complete_paragraph":
            try:
                completion = GPT.paragraph_completion(
                    prompt=properties["prompt"],
                    title=properties["title"],
                    section=properties.pop("section", None),
                    sub_section=properties.pop("sub_section", None),
                    description=properties.pop("describtion", None),
                    sentence=properties.pop("sentence", False),
                    language=properties["lang"],
                )
                completion_tokens = 0
                for chunk in completion:
                    finish_reason = chunk["choices"][0]["finish_reason"]
                    if finish_reason is None:
                        completion_tokens += 1
                        self.send_json(
                            {
                                "type": "content",
                                "chunk": chunk["choices"][0]["delta"]["content"],
                                "status": True,
                            }
                        )
            except Exception as e:
                self.send_json(
                    {"type": "error", "chunk": str(e), "status": False})
        if action == "rewrite_wiki_section":
            """
            {
                'action':"rewrite_wiki_section",
                "properties":{
                    "section":"",
                    "sub_section":"",
                    "content":"",
                    "lang":""
                }
            }
            """
            try:
                content = properties["content"]
                lang = properties["lang"]
            except KeyError:
                print("eroor 1")
                self.send_json(
                    {"type": "error",
                        "chunk": f"please provide ({e})", "status": False}
                )
            try:
                completion = GPT.rewrite_wiki_section(
                    content=content,
                    language=lang
                )
                content_tokens = GPT.gpt3_tokens_calc(content)
                completion_tokens = 0
                generated = ""
                for chunk in completion:
                    finish_reason = chunk["choices"][0]["finish_reason"]
                    if finish_reason is None:
                        completion_tokens += 1
                        content = chunk["choices"][0]["delta"]["content"]
                        generated = generated + content
                        self.send_json(
                            {
                                "type": "content",
                                "chunk": chunk["choices"][0]["delta"]["content"],
                                "status": True,
                            }
                        )
                total_tokens = content_tokens + completion_tokens
                used_credits = Credit.calc(
                    operation=Credit.Operation.rewrite_wiki_section,
                    n_tokens=total_tokens
                )
                # WikiModel.objects.create(
                # insert code later
                # )
            except Exception as e:
                print("eroor 3")
                print(e)
                self.send_json(
                    {"type": "error", "chunk": str(e), "status": False})
            self.send_json({"status": False})

        if action == "improve_text":
            try:
                messages_data = GPT.improvement_messages(
                    text=properties["text"],
                    lang=properties["lang"],
                    improve=properties["improvements"],
                    instruction=properties.pop("instruction", None),
                )
                messages = messages_data["messages"]
                prompt_tokens = messages_data["tokens"]
            except ValueError as e:
                self.send_json({"type": "error", "chunk": e, "status": False})
            try:
                improved = GPT.improvement(messages=messages)
                generated = ""
                completion_tokens = 0
                for chunk in improved:
                    finish_reason = chunk["choices"][0]["finish_reason"]
                    if finish_reason is None:
                        completion_tokens += 1
                        content = chunk["choices"][0]["delta"]["content"]
                        generated = generated + content
                        self.send_json(
                            {
                                "type": "content",
                                "chunk": content,
                                "status": True,
                            }
                        )
                total_tokens = prompt_tokens + completion_tokens
                # used_credits = Credit.calc(
                #     operation=Credit.Operation.improvement,
                #     # n_tokens=
                # )
            except Exception as e:
                self.send_json(
                    {"type": "error", "chunk": str(e), "status": False})


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, request):
        # from .models import WikiModel
        messages = request.get("messages")
        model = request.get("model")
        model = "gpt_3"
        # model = "gpt_4"
        try:
            messages = [
                {"role": message[0], "content": message[1]} for message in messages
            ]
            if len(messages) > 3:
                messages = messages[:3]
            messages.append(
                {
                    "role": "system",
                    "content": f"ChatG6, this is your name, and you are a chatbot for the G6Tool website, which provides Wikipedia search and tools for writers to improve productivity.\n\
                        Finaly support your answers with references on the web and links ,bookes",
                },
            )
            messages = messages[::-1]
            prompt_tokens = GPT.gpt3_tokens_calc(
                messages,
                chat=True
            )
            model = GPT.Models.gpt_35_1106
            response = GPT.chat(
                model=model,
                messages=messages,
            )
            completion_tokens = 0
            for chunk in response:
                finish_reason = chunk["choices"][0]["finish_reason"]
                if finish_reason is None:
                    completion_tokens += 1
                    self.send_json(
                        {
                            "type": "content",
                            "chunk": chunk["choices"][0]["delta"]["content"],
                            "status": True,
                        }
                    )
            total_tokens = prompt_tokens + completion_tokens
            used_credits = Credit.calc(
                model=model,
                operation=Credit.Operation.chat,
                n_tokens=total_tokens
            )
        except Exception as e:
            self.send_json({"type": "error", "chunk": str(e), "status": False})
        self.send_json({"status": False})
