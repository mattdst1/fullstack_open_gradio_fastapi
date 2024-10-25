import gradio as gr
import pandas as pd


def persons_component(persons: list[dict]) -> gr.Markdown:
    # persons_string = ""
    # for person in persons:
    #     person_name = person["name"]
    #     person_number = person["number"]
    #     persons_string += f"- {person_name} {person_number}\n"

    if persons:
        df = pd.DataFrame(persons)

    else:
        df = pd.DataFrame(columns=["name", "number"])

    return gr.Markdown(df.to_markdown(index=False))


def handle_submit(name_list: list[dict], name: str, number: str):
    names = [d["name"] for d in name_list]
    if name not in names:
        name_object = {"name": name, "number": number}
        name_list.append(name_object)
    else:
        index = names.index(name)
        name_object = {"name": name, "number": number}
        name_list[index] = name_object
    return name_list, "", ""


def handle_filter(name_filter: str, name_list: list[dict]):

    if name_filter == "":
        return name_list

    else:
        return [d for d in name_list if name_filter.lower() in d["name"].lower()]


def person_form():
    name = gr.Text(label="Name")
    number = gr.Text(label="Number")
    btn_submit = gr.Button("submit")
    return name, number, btn_submit


def name_search_bar():
    name_filter = gr.Text("", label="Name")
    return name_filter


with gr.Blocks() as demo:
    # state
    persons = gr.State([{"name": "Matthew", "number": "12345"}])

    gr.Markdown("# Phonebook")

    with gr.Accordion("New contact"):
        name, number, btn_submit = person_form()

    with gr.Accordion("Search contact"):
        name_filter = name_search_bar()

    with gr.Accordion("Numbers"):
        persons_string = persons_component(persons.value)

    btn_submit.click(
        lambda name, number, names: handle_submit(
            name_list=names, name=name, number=number
        ),
        inputs=[name, number, persons],
        outputs=[persons, name, number],
        show_progress="hidden",
    )

    @gr.on(
        persons.change,
        inputs=[persons],
        outputs=[persons_string],
        show_progress="hidden",
    )
    def handle_persons_update(persons: list[dict]) -> gr.Markdown:
        return persons_component(persons)

    @gr.on(
        name_filter.change,
        inputs=[name_filter, persons],
        outputs=[persons_string],
        show_progress="hidden",
    )
    def handle_filter_update(name_filter: str, name_list: list[dict]):
        found_objects = handle_filter(name_filter=name_filter, name_list=name_list)
        return persons_component(found_objects)


if __name__ == "__main__":
    demo.launch()
